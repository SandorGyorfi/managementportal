from django.shortcuts import render, redirect
from .forms import CustomerForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from decouple import config  
from head_office.models import DepartmentUser

# Create your views here.

def operator_login(request):
    error = None
    if request.method == 'POST':
        department = request.POST.get('department')
        username = request.POST.get('username')
        pin = request.POST.get('password')

        DEPARTMENT_MAP = {
            "customer_service": (config('CS_OPERATOR_USERNAME', default=''), config('CS_OPERATOR_PIN', default='')),
            "financial_department": (config('FD_OPERATOR_USERNAME', default=''), config('FD_OPERATOR_PIN', default='')),
            "delivery_department": (config('DD_OPERATOR_USERNAME', default=''), config('DD_OPERATOR_PIN', default='')),
            "head_office": (config('HO_OPERATOR_USERNAME', default=''), config('HO_OPERATOR_PIN', default=''))
        }

        

        if department not in DEPARTMENT_MAP:
            error = 'Invalid department'
        elif username == DEPARTMENT_MAP[department][0] and pin == DEPARTMENT_MAP[department][1]:
            user, created = DepartmentUser.objects.get_or_create(username=username)
            if not created:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            if user.is_authenticated:
                request.session['just_logged_in'] = True  
                if department == 'financial_department':
                    return redirect('financial_department:view_payments')  
                elif department == 'customer_service':
                    return redirect('add_customer')
                elif department == 'delivery_department':
                    return redirect('delivery_department:view_deliveries')
                elif department == 'head_office':
                    return redirect('head_office:head_office')
            else:
                print("User is NOT authenticated!")
                error = 'Unable to authenticate user'
        else:
            error = 'Invalid credentials'

    return render(request, 'login.html', {'error': error})

@login_required(login_url='operator_login')
def add_customer(request):
    context = {}
    
    if request.session.pop('just_logged_in', False):
        context['just_logged_in'] = True

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            from financial_department.models import Payment
            Payment.objects.create(customer=customer, status="Pending Payment")
            context['message_display'] = True
            form = CustomerForm()  
        else:
            context['form'] = form
    else:
        form = CustomerForm()

    context['form'] = form
    return render(request, 'customer_service/add_customer.html', context)