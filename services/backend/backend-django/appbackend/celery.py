import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend-django.appbackend.settings")

app = Celery("appbackend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


def get_task_info(task_id):
    """
    return task info for the given task_id
    """
    task_result = app.AsyncResult(task_id)
    return {
        "task_id": task_id,
        "task_status": task_result.status,  # PENDING means also "UNKNOWN"
        "task_result": task_result.get() if task_result.ready() else task_result.info,
    }


def revoke(task_id):
    """
    revoke given task_id
    """
    task_result = app.AsyncResult(task_id)
    task_result.revoke(terminate=True)
    task_result.forget()  # release resource
    return {"task_id": task_id, "task_status": "REVOKED"}


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


if __name__ == "__main__":
    app.start()
