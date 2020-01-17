import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_SCHEDULER_STARTED, EVENT_SCHEDULER_SHUTDOWN
from .jobs import init_job_01
from django_apscheduler.models import DjangoJob
from django_apscheduler.jobstores import register_events, DjangoJobStore
from .listeners import job_listener, scheduler_listener


logger = logging.getLogger(__name__)


# 初始化scheduler
DjangoJob.objects._ping_interval = 0
stores = {"default": DjangoJobStore()}
executors = {"default": ThreadPoolExecutor(20)}
job_defaults = {"coalesce": False, "max_instances": 1}

scheduler = BackgroundScheduler(jobstores=stores, executors=executors, job_defaults=job_defaults)
scheduler.add_listener(job_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
scheduler.add_listener(scheduler_listener, EVENT_SCHEDULER_STARTED | EVENT_SCHEDULER_SHUTDOWN)

register_events(scheduler)

scheduler.start()
