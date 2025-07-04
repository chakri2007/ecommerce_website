from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from django.core.exceptions import ValidationError
from django.conf import settings
from django.shortcuts import render
import bleach
import os
from supabase import create_client, Client
import uuid

# Create a Supabase client
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def validate_image(image):
    max_size = 5 * 1024 * 1024  # 5MB
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    ext = os.path.splitext(image.name)[1].lower()
    if image.size > max_size:
        raise ValidationError('Image size exceeds 5MB')
    if ext not in valid_extensions:
        raise ValidationError('Invalid image format')

@login_required
def add_product_page(request):
    if request.method == 'GET':
        return render(request, 'add_product.html')
    return JsonResponse({'message': 'Invalid method'}, status=405)

@login_required
@csrf_exempt
def add_selling_object(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        stock = request.POST.get('stock', 1)
        image = request.FILES.get('image')

        if not name or not price:
            return JsonResponse({'Warn': 'Name and price are required'}, status=400)

        try:
            price = float(price)
            stock = int(stock)
            if price <= 0 or stock < 0:
                return JsonResponse({'Warn': 'Price must be positive and stock cannot be negative'}, status=400)
        except (ValueError, TypeError):
            return JsonResponse({'Warn': 'Invalid price or stock value'}, status=400)

        image_url = None
        if image:
            try:
                validate_image(image)
                # Generate a unique filename
                unique_filename = f"{uuid.uuid4().hex}_{image.name}"
                # Upload to Supabase Storage
                supabase.storage.from_(settings.SUPABASE_BUCKET).upload(
                    path=unique_filename,
                    file=image.read(),
                    file_options={"content-type": image.content_type}
                )
                # Get the public URL
                image_url = supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(unique_filename)
            except ValidationError as e:
                return JsonResponse({'Warn': str(e)}, status=400)
            except Exception as e:
                return JsonResponse({'Error': f'Upload failed: {str(e)}'}, status=500)

        description = bleach.clean(description) if description else None

        product = Product(
            user=request.user,
            name=name,
            price=price,
            description=description,
            stock=stock,
            image_url=image_url  # store only the Supabase URL
        )
        product.save()

        return JsonResponse({
            'Success': 'Product added successfully',
            'product': {
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'description': product.description,
                'stock': product.stock,
                'image_url': image_url
            }
        }, status=201)

    return JsonResponse({'message': 'Invalid method'}, status=405)
