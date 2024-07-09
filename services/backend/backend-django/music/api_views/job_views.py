from appbackend.celery import get_task_info, revoke
from rest_framework.views import APIView
from django.http import JsonResponse


class JobView(APIView):
    def get(self, request, job_id):
        print(f"retreiving job{job_id}")
        job_status = get_task_info(job_id)
        return JsonResponse(job_status)

    def delete(self, request, job_id):
        """
        Cancel a Celery task given its task ID.
        """
        return JsonResponse(revoke(job_id))
