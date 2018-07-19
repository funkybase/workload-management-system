import os

import redis
from rq import Worker, Queue, Connection

listen = ['default']

if 'DYNO' in os.environ:

    redis_url = os.environ.get("REDIS_URL")

    conn = redis.from_url(redis_url)

else:

    conn = redis.Redis(host='redis-19299.c1.ap-southeast-1-1.ec2.cloud.redislabs.com', port='19299', password='5mMbjLljCmZo9WCAojO2zlc5E01pMZpd')

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
