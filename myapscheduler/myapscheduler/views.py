import logging
from importlib import import_module
from inspect import isfunction
from background_task import scheduler
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


logger = logging.getLogger(__name__)


def get_job(job_name: str):
    try:
        attrs = import_module("background_task.jobs").__dict__
        obj = attrs.get(job_name)
        if obj and isfunction(obj):
            return obj
    except ModuleNotFoundError as e:
        logger.warning(str(e))


def serializer_cron_job(job):
    return {
        "id": job.id,
        "name": job.name,
        "executor": job.executor,
        "max_instances": job.max_instances,
        "misfire_grace_time": job.misfire_grace_time,
        "next_run_time": job.next_run_time,
        "trigger": {
            "type": 'cron',
            "fields": {
                field.name: ','.join([str(e) for e in field.expressions])
                for field in job.trigger.fields
            }
        }
    }


class Jobs(APIView):
    def get(self, request):
        jobs = scheduler.get_jobs()
        data = [serializer_cron_job(job) for job in jobs]
        return Response(data={'jobs': data}, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        try:
            job_name = data.pop('job')
        except KeyError:
            return Response(data={"error": '缺少参数`job`'}, status=status.HTTP_400_BAD_REQUEST)

        job = get_job(job_name)
        try:
            job = scheduler.add_job(job, id=job_name, trigger="cron", **data)
            return Response(data=serializer_cron_job(job), status=status.HTTP_201_CREATED)
        except Exception as ex:
            logger.error('添加任务失败，error={}'.format(ex), exc_info=True)
            return Response(data={"error": "添加任务失败"})


class Job(APIView):
    def get(self, request, job_id):
        try:
            job = scheduler.get_job(job_id=job_id)
            if not job:
                return Response(data={'details': "任务未找到"}, status=status.HTTP_404_NOT_FOUND)
            data = serializer_cron_job(job)
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(str(ex), exc_info=True)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, job_id):
        job = scheduler.get_job(job_id=job_id)
        if job:
            scheduler.remove_job(job_id=job_id)
        return Response(data=None, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, job_id):
        job = scheduler.get_job(job_id=job_id)
        if job:
            job = scheduler.reschedule_job(job_id=job_id, trigger="cron", **request.data)
        data = serializer_cron_job(job)
        return Response(data=data, status=status.HTTP_200_OK)


class JobAction(APIView):
    def get(self, request, job_id, action):
        if action == "pause":
            scheduler.pause_job(job_id=job_id)
        elif action == "resume":
            scheduler.resume_job(job_id=job_id)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)
