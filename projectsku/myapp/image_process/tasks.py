from celery import shared_task
import csv
import requests
from django.core.files.storage import default_storage
from .models import ProcessingRequest, ImageData
from .utils import compress_image

def generate_csv(processing_request):
    file_path = f'processed_csvs/{processing_request.request_id}.csv'
    with default_storage.open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Serial Number", "Product Name", "Input Image Urls", "Output Image Urls"])
        
        images = ImageData.objects.filter(product__processing_request=processing_request)
        for index, product in enumerate(processing_request.product_set.all(), start=1):
            input_urls = []
            output_urls = []
            for image in images.filter(product=product):
                input_urls.append(image.input_url)
                output_urls.append(image.output_url)
            writer.writerow([index, product.name, ', '.join(input_urls), ', '.join(output_urls)])
    return file_path

@shared_task
def process_images(request_id):
    processing_request = ProcessingRequest.objects.get(request_id=request_id)
    processing_request.status = 'processing'
    processing_request.save()

    images = ImageData.objects.filter(product__processing_request=processing_request)
    for image in images:
        compressed_url = compress_image(image.input_url)
        if compressed_url:
            image.output_url = compressed_url
            image.save()
    
    processing_request.status = 'completed'
    processing_request.save()

    csv_path = generate_csv(processing_request)

    if processing_request.webhook_url:
        with default_storage.open(csv_path, 'rb') as csvfile:
            requests.post(
                processing_request.webhook_url, 
                files={'file': csvfile},
                data={'request_id': str(request_id), 'status': 'completed'}
            )
