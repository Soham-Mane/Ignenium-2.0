from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from .models import merchant,merchant_service_details,customer
from rest_framework import generics
from .serializers import MerchantServiceDetailsSerializer
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.response import Response
from rest_framework.decorators import api_view
import razorpay
from django.conf import settings
import pyotp
import json
# Create your views here.

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


@csrf_exempt
def signup_merchant(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        if merchant.objects.filter(username=username).exists():
            return JsonResponse({"message": "Sign-up failed, username already exists"})
        
        new_merchant = merchant(
            username=username,
            password=make_password(password),
            email=email,
            gender=gender,
            age=age,    
            phone=phone,
            address=address
        )

        new_merchant.save()
        return JsonResponse({"success": "Sign-up successful"})
    else:
        return JsonResponse({"message": "Invalid request method"})
    
@csrf_exempt
def signup_customer(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        if merchant.objects.filter(username=username).exists():
            return JsonResponse({"message": "Sign-up failed, username already exists"})
        
        new_customer = customer(
            username=username,
            password=make_password(password),
            email=email,
            gender=gender,
            age=age,    
            phone=phone,
            address=address
        )

        new_customer.save()
        return JsonResponse({"success": "Sign-up successful"})
    else:
        return JsonResponse({"message": "Invalid request method"})

@csrf_exempt
def login_merchant(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            merchant_obj = merchant.objects.get(username=username)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Invalid username"}, status=400)
        
        if check_password(password, merchant_obj.password):
            return JsonResponse({"success": "Login successful"})
        else:
            return JsonResponse({"message": "Invalid password"}, status=400)

    return JsonResponse({"message": "Invalid request method"}, status=405)

@csrf_exempt
def login_customer(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            customer_obj = customer.objects.get(username=username)
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Invalid username"}, status=400)
        
        if check_password(password, customer_obj.password):
            return JsonResponse({"success": "Login successful"})
        else:
            return JsonResponse({"message": "Invalid password"}, status=400)

    return JsonResponse({"message": "Invalid request method"}, status=405)

@csrf_exempt
def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        secret = pyotp.random_base32()
        totp = pyotp.TOTP(secret, interval=90)
        otp_generated = totp.now()
        request.session['generated_otp'] = otp_generated
        subject = 'Two Step authentication'
        message = f'Your One Time Password is {otp_generated}.'
        email_from = 'from@yourdjangoapp.com'
        recipient = [f'{email}']
        send_mail( subject, message, email_from, recipient)
        return JsonResponse({"message": "OTP sent successfully"})
    else:
        return JsonResponse({"message": "OTP was not sent successfully"})
    

def verify_otp(request):
    if request.method == 'POST':
        if 'generated_otp' in request.session:
            generated_otp = request.session['generated_otp']
            entered_otp = request.POST.get('otp')  # Change this to match how you receive the entered OTP
        
        if entered_otp and entered_otp == generated_otp:
            # OTP verification successful
            return HttpResponse("OTP verification successful")
        else:
            # OTP verification failed
            return HttpResponse("OTP verification failed")
    else:
        return HttpResponse("No OTP generated")
    

@csrf_exempt
def create_merchant_service(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        category = request.POST.get('category')
        title = request.POST.get('title')
        charges = request.POST.get('charges')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        description = request.POST.get('description')

        # Handle image file upload
        image = request.FILES.get('image')

        merchant_service = merchant_service_details.objects.create(
            company_name=company_name,
            # category=category,
            title=title,
            charges=charges,
            start_time=start_time,
            end_time=end_time,
            description=description,
            image=image  # Assuming you've set the 'upload_to' parameter in your model
        )

        print(merchant_service)
        merchant_service.save()
        return JsonResponse({"success": "Sign-up successful"})

    else:
        return JsonResponse({"message": "Invalid request method"})
    


@api_view(['GET'])
def get_merchant_service_details(request):
    merchant_details = merchant_service_details.objects.all()
    serializer = MerchantServiceDetailsSerializer(merchant_details, many=True)
    return Response(serializer.data)


def service_data(request):
    if request.method == 'GET':
        data = merchant_service_details.objects.all()

        # Serialize the data using a custom serializer
        serialized_data = serialize_merchant_service_details(data)

        return JsonResponse({"data": serialized_data}, safe=False)
    else:
        return JsonResponse({"message": "Invalid request method"})
    
    
def serialize_merchant_service_details(queryset):
    # Serialize the data manually to handle TimeField and ImageField
    data = []
    for item in queryset:
        item_dict = {
            'model': 'shopapp.merchant_service_details',
            'pk': item.pk,
            'fields': {
                'company_name': item.company_name,
                'category': item.category,
                'title': item.title,
                'description': item.description,
                'charges': str(item.charges),  # Convert Decimal to string
                'start_time': item.start_time.strftime('%H:%M:%S'),  # Format TimeField as string
                'end_time': item.end_time.strftime('%H:%M:%S'),  # Format TimeField as string
                'image': item.image.url,  # Use the URL of the ImageField
                'rating': str(item.rating),  # Convert Decimal to string
            }
        }
        data.append(item_dict)

    # Serialize the data to JSON
    serialized_data = json.dumps(data, cls=DjangoJSONEncoder)
    return serialized_data

@csrf_exempt
def get_company_data(request, company_name):
    try:
        # Query the Service model to get data for the specified company name
        service_data = merchant_service_details.objects.filter(company_name=company_name).values()
        
        # Serialize the data as JSON
        data = list(service_data) 
        print(data) # Convert QuerySet to a list
        return JsonResponse(data, safe=False)
    except merchant_service_details.DoesNotExist:
        return JsonResponse({'error': 'Company not found'}, status=404)





