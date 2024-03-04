"""
views.py
Ajer Lodhi
Purpose: All our operations ot be performed on the image
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from io import BytesIO
from PIL import ImageOps
from django.http import JsonResponse
from PIL import Image, ImageOps
import base64
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import SuspiciousOperation
import math

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/layout.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )


def load_uploaded_image(request):
    uploaded_image = request.FILES['image']
    return Image.open(uploaded_image)

def load_processed_image_from_session(request):
    processed_image_base64 = request.session.get('processed_image', None)
    if processed_image_base64:
        processed_image_bytes = base64.b64decode(processed_image_base64)
        return Image.open(BytesIO(processed_image_bytes))
    return None

def flip_horizontal(image):
    return image.transpose(Image.FLIP_LEFT_RIGHT)

def flip_vertical(image):
    return image.transpose(Image.FLIP_TOP_BOTTOM)

def resize_image(image, percentage):
    width, height = image.size
    new_width = width * percentage // 100
    new_height = height * percentage // 100
    return image.resize((new_width, new_height))

def convert_to_grayscale(image):
    return ImageOps.grayscale(image)

def rotate_image(image, degrees):
    # Rotate the image
    rotated_image = image.rotate(degrees, expand=True, center=(image.width / 2, image.height / 2), resample=Image.BICUBIC)
    # Get the bounding box of the rotated image
    bbox = rotated_image.getbbox()
    # Crop the rotated image to fit within the bounding box
    cropped_image = rotated_image.crop(bbox)
    return cropped_image

def rotate_left(image):
    return image.rotate(90, expand=True)

def rotate_right(image):
    return image.rotate(-90, expand=True)

def create_thumbnail(image):
    thumbnail_size = (200, 200)  # Define the thumbnail size
    thumbnail = image.copy()
    thumbnail.thumbnail(thumbnail_size)
    return thumbnail


def download_image(image):
    output_buffer = BytesIO()
    image.save(output_buffer, format='PNG')
    output_buffer.seek(0)
    return output_buffer

def download_thumbnail(image):
    thumbnail = create_thumbnail(image)
    output_buffer = BytesIO()
    thumbnail.save(output_buffer, format='PNG')
    output_buffer.seek(0)
    return output_buffer

def reset_image_session(request):
    request.session.pop('processed_image', None)
    return JsonResponse({'status': 'success', 'message': 'Image reset successfully'})

def process_image(request):
    if request.method == 'POST':
        operation = request.POST.get('operation')
        
        if operation == 'reset_image':
            return reset_image_session(request)

        uploaded_image = load_uploaded_image(request)
        processed_image = load_processed_image_from_session(request) or uploaded_image

        if operation == 'flip_horizontal':
            processed_image = flip_horizontal(processed_image)
        elif operation == 'flip_vertical':
            processed_image = flip_vertical(processed_image)
        elif operation == 'resize':
            percentage = int(request.POST['percentage'])
            if percentage < -95 or percentage > 500:
                return JsonResponse({'status': 'error', 'message': 'Invalid size'})
                raise SuspiciousOperation('Invalid resize percentage')
            processed_image = resize_image(processed_image, percentage)
        elif operation == 'convert_to_grayscale':
            processed_image = convert_to_grayscale(processed_image)
        elif operation == 'rotate':
            degrees = int(request.POST['degrees'])
            processed_image = rotate_image(processed_image, -degrees)
        elif operation == 'rotate_left':
            processed_image = rotate_left(processed_image)
        elif operation == 'rotate_right':
            processed_image = rotate_right(processed_image)
        elif operation == 'create_thumbnail':
            # Create thumbnail
            thumbnail_image = create_thumbnail(processed_image)
            # Download thumbnail
            thumbnail_output_buffer = download_image(thumbnail_image)
            thumbnail_image_base64 = base64.b64encode(thumbnail_output_buffer.getvalue()).decode('utf-8')
            
            # Download processed image
            processed_output_buffer = download_image(processed_image)
            processed_image_base64 = base64.b64encode(processed_output_buffer.getvalue()).decode('utf-8')

            return JsonResponse({
                'status': 'success', 
                'message': 'Thumbnail created successfully', 
                'processed_image': processed_image_base64,
                'thumbnail_image': thumbnail_image_base64
            })
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid operation'})

        # Processed image for other operations
        output_buffer = download_image(processed_image)
        processed_image_base64 = base64.b64encode(output_buffer.getvalue()).decode('utf-8')
        request.session['processed_image'] = processed_image_base64

        return JsonResponse({'status': 'success', 'message': 'Image processed successfully', 'processed_image': processed_image_base64})

    return JsonResponse({'status': 'error', 'message': 'Method not allowed'})



