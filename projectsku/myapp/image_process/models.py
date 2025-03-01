import uuid
from django.db import models

# Database Models
class ProcessingRequest(models.Model):
    request_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    webhook_url = models.URLField(null=True, blank=True)

class Product(models.Model):
    processing_request = models.ForeignKey(ProcessingRequest, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

class ImageData(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    input_url = models.URLField()
    output_url = models.URLField(null=True, blank=True)
