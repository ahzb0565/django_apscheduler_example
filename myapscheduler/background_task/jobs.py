from datetime import datetime


def init_job_01():
    now = datetime.now()
    print('init_job_01: {}'.format(now))


def configurable_job_01():
    now = datetime.now()
    print('configurable job 01: {}'.format(now))
