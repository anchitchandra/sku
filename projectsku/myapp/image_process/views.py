import csv

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import ProcessingRequest, Product, ImageData
from .tasks import process_images

# API Views
@csrf_exempt
def upload_csv(request):
    if request.method == 'POST':
        file = request.FILES.get("file")
        webhook_url = request.POST.get('webhook_url')

        if not file:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        processing_request = ProcessingRequest.objects.create(webhook_url=webhook_url)
        decoded_file = file.read().decode("utf-8").splitlines()
        csv_reader = csv.reader(decoded_file, quotechar='"')

        try:
            next(csv_reader)  # Skip header row
        except StopIteration:
            return JsonResponse({"error": "CSV file has no data"}, status=400)
        
        for row in csv_reader:
            product = Product.objects.create(processing_request=processing_request, name=row[1])
            image_urls = row[2].split(',')
            for image_url in image_urls:
                ImageData.objects.create(product=product, input_url=image_url)

        process_images.delay(processing_request.request_id)
        return JsonResponse({'request_id': str(processing_request.request_id)}, status=202)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def get_status(request, request_id):
    processing_request = get_object_or_404(ProcessingRequest, request_id=request_id)
    return JsonResponse({'request_id': request_id, 'status': processing_request.status})