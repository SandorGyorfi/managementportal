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