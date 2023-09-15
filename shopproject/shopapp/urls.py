from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup_merchant/', signup_merchant, name='signup_merchant'),
    path('signup_customer/', signup_customer, name='signup_customer'),
    path('login_merchant/', login_merchant, name='login_merchant'),
    path('login_customer/', login_customer, name='login_customer'), 
    path('send_otp/', send_otp, name='send_otp'), 
    path('verify_otp/', verify_otp, name='verify_otp'), 
    path('create_merchant_service/', create_merchant_service, name='create_merchant_service'),
    path('data/', service_data, name='service_data'),
    path('merchant-service-details/', get_merchant_service_details, name='merchant-service-details-list'),
    path('get_company_data/<str:company_name>/',get_company_data, name='get_company_data'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)