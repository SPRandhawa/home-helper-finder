from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer

def register_customer_view(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            occupation = request.POST.get('occupation')
            age = request.POST.get('age')
            phone = request.POST.get('phone')
            gender = request.POST.get('gender')
            pincode = request.POST.get('pincode')
            address = request.POST.get('address')
            marital_status = request.POST.get('marital_status')
            children = request.POST.get('children', 0)
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Check if username or phone already exists
            if Customer.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken. Please choose another.')
                return render(request, 'accounts/register_customer.html')

            if Customer.objects.filter(phone=phone).exists():
                messages.error(request, 'Phone number already registered.')
                return render(request, 'accounts/register_customer.html')

            # Create customer instance
            customer = Customer(
                name=name,
                occupation=occupation,
                age=age,
                phone=phone,
                gender=gender,
                pincode=pincode,
                address=address,
                marital_status=marital_status,
                children=children,
                email=email,
                username=username,
                photo=request.FILES.get('photo'),
                latest_photo=request.FILES.get('latest_photo'),
                aadhaar_front=request.FILES.get('aadhaar_front'),
                aadhaar_back=request.FILES.get('aadhaar_back'),
            )
            customer.set_password(password)
            customer.save()

            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('/')  # Change this to your login or dashboard route later
            
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    return render(request, 'accounts/register_customer.html')
