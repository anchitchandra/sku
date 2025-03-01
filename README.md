# Image Processing System

## **Overview**
This system processes image data asynchronously from CSV files, compressing images by 50% and storing processed data in a database. The system provides APIs for:
- Uploading CSV files
- Checking processing status
- Triggering a webhook after processing

## **System Architecture Diagram**
[_(Draw.io)_](https://drive.google.com/file/d/16wjTHgShDuFxCljVq9VBEH5j04S6b8Xe/view?usp=sharing)

## **Components Description**
### **Image Processing Service Interaction**
- Uses Celery for asynchronous task execution.
- Compresses images by 50% and updates database records.

### **Webhook Handling**
- Sends a callback request with processing status and results.

### **Database Interaction**
- Stores processing requests, products, and image URLs.

### **API Endpoints**
- **Upload API**: Accepts CSV files and returns a unique request ID.
- **Status API**: Checks processing status using the request ID.

## **Database Schema**
### **Tables**
#### `ProcessingRequest`
- `id` (UUID, Primary Key)
- `webhook_url` (String)
- `status` (String: Pending, Processing, Completed)
- `created_at` (Timestamp)

#### `Product`
- `id` (UUID, Primary Key)
- `processing_request_id` (Foreign Key -> ProcessingRequest)
- `name` (String)

#### `ImageData`
- `id` (UUID, Primary Key)
- `product_id` (Foreign Key -> Product)
- `input_url` (String)
- `output_url` (String, Nullable)

## **API Documentation**
### **Upload API**
**Endpoint:** `POST /image_process/upload/`
**Request:**
```json
{
  "file": "CSV File",
  "webhook_url": "https://your-webhook.com"
}
```
**Response:**
```json
{
  "request_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

### **Status API**
**Endpoint:** `GET /image_process/status/{request_id}/`
**Response:**
```json
{
  "request_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "processing"
}
```

## **Asynchronous Workers Documentation**
### **process_images(request_id)**
- Fetch all images associated with the `request_id`.
- Compress each image and update `output_url`.
- Update the request status to `completed`.
- Trigger webhook if provided.

## **Postman Collection**
[_(postman collection link)_](https://sku-assignment.postman.co/workspace/sku-assignment-Workspace~941f1f68-a15c-4d93-9cc1-cbd0c43eca15/collection/26091733-0ee49088-449d-4a7a-9200-d8e2582090a7?action=share&creator=26091733)

## **Installation Steps**

- Clone the repository:

```
git clone https://github.com/your-repository.git

```
```
cd your-repository

```

- Install dependencies:

```
poetry install

```

- Apply database migrations:

```
poetry run python manage.py migrate

```

- Start Redis server (if not running):

```
redis-server

```

- Start Celery worker:

```
poetry run celery -A your_project worker --loglevel=info

```

- Start the Django server:

```
poetry run python manage.py runserver

```




