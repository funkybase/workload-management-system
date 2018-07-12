from backend import db
from sqlalchemy import inspect
import datetime

now = datetime.datetime.now()

pattern_activity = db.Table('pattern_activity',
        db.Column('pattern_id', db.Integer, db.ForeignKey('pattern.id'), primary_key=True),
        db.Column('activity_id', db.Integer,db.ForeignKey('activity.id'), primary_key=True)
        )

location_period = db.Table('location_period',
        db.Column('location_id', db.Integer, db.ForeignKey('location.id'), primary_key=True),
        db.Column('period_id', db.Integer, db.ForeignKey('period.id'), primary_key = True)
        )

class Pattern(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), nullable=False, index=True, unique=True)
    description = db.Column(db.String(64))
    long_description = db.Column(db.String(256))
    student_per_group = db.Column(db.Integer, nullable=False, default=15)
    hour_per_tutorial = db.Column(db.Integer, nullable=False, default=1)
    mode = db.Column(db.String(8), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False) 
    pattern_activity = db.relationship('Activity', secondary=pattern_activity, lazy='subquery', backref=db.backref('patterns', lazy=True))
    offerings = db.relationship('Offering', backref='pattern', lazy=True)
    
class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    hour = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(8), nullable=False)
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    patterns = db.relationship('Pattern', backref='location', lazy=True)
    period = db.relationship('Period', secondary=location_period, lazy='subquery', backref=db.backref('locations', lazy=True))
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

class Period(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), nullable=False)
    offerings = db.relationship('Offering', backref='period', lazy=True)
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), nullable=False, index=True)
    type = db.Column(db.String(16))
    name = db.Column(db.String(64), nullable=False)
    offerings = db.relationship('Offering', backref='unit', lazy=True)
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False, index=True)
    fraction = db.Column(db.Float, nullable=False)
    supervision = db.Column(db.Float, nullable=False, default=0)
    research = db.Column(db.Float, nullable=False, default=0)
    service = db.Column(db.Float, nullable=False, default=0)
    extra = db.Column(db.Float, nullable=False, default=0)
    service_description = db.Column(db.String(128))
    comments = db.Column(db.String(128))
    offerings = db.relationship('Offering', backref='UC', lazy=True)
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

class Offering(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    confirm = db.Column(db.Boolean, index=True, nullable=False, default=False)
    enrolment = db.Column(db.Integer, nullable=False, default=0)
    tutorial_to_staff = db.Column(db.Integer, nullable=False, default=0)
    tutorial_to_casual = db.Column(db.Integer, nullable=False, default=0)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'), nullable=False)
    pattern_id = db.Column(db.Integer, db.ForeignKey('pattern.id'), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id'))
    period_id = db.Column(db.Integer, db.ForeignKey('period.id'), nullable=False)
    #year = db.Column(db.Integer, default=now.year, nullable=False)
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }

