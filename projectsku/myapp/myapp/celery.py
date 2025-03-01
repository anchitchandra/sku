import os
from celery import Celery

# Set default Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myapp.settings")

app = Celery("myapp")

# Load Celery config from Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodiscover tasks in installed Django apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")