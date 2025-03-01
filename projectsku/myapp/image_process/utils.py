import uuid
import csv
import requests
from io import StringIO, BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def compress_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img_io = BytesIO()
        img.save(img_io, format='JPEG', quality=50)
        img_io.seek(0)
        filename = f'compressed/{uuid.uuid4()}.jpg'
        path = default_storage.save(filename, ContentFile(img_io.read()))
        return default_storage.url(path)
    return None
