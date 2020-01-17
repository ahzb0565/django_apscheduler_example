import logging
from apscheduler.events import EVENT_SCHEDULER_STARTED, EVENT_SCHEDULER_SHUTDOWN

logger = logging.getLogger(__name__)


def job_listener(event):
    if event.exception:
        logger.error('exception happens with job {}, exception={}'.format(event.job_id, event.exception))
    else:
        logger.info('Job {} executed successfully'.format(event.job_id))


def scheduler_listener(event):
    event_code = event.code
    if event_code == EVENT_SCHEDULER_STARTED:
        logger.info("Scheduler started!")
    elif event_code == EVENT_SCHEDULER_SHUTDOWN:
        logger.info("Scheduler shutdown!")
    else:
        logger.info('Scheduler event: {}'.format(event.__class__.__name__))
