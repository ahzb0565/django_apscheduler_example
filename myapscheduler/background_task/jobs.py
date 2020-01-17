from datetime import datetime


class JobException(Exception):
    def __init__(self, message=None):
        super().__init__()
        self.message = message if message else "Job execute failed!"


def init_job_01():
    now = datetime.now()
    print('init_job_01: {}'.format(now))


def configurable_job_01():
    now = datetime.now()
    print('configurable job 01: {}'.format(now))


def exception_job():
    now = datetime.now()
    raise JobException('Job execute failed, job_id=exception_job, time={}'.format(now))
