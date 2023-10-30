from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from customer_service.models import Customer
from financial_department.models import Payment
from delivery_department.models import Delivery
from django.db.models import F
from datetime import date
from django.contrib import messages
from decouple import config  
from head_office.models import DepartmentUser

@login_required(login_url='operator_login')
def view_head_office(request):
    pending_customers = Customer.objects.all()
    pending_payments = Payment.objects.filter(status="Pending Payment")
    out_for_deliveries = Delivery.objects.filter(status="Pending Delivery")
    overdue_deliveries = Delivery.objects.filter(delivery_date__lt=date.today()).exclude(status="Delivered")

    context = {
        'pending_customers': pending_customers,
        'pending_payments': pending_payments,
        'out_for_deliveries': out_for_deliveries,
        'overdue_deliveries': overdue_deliveries,
        'today': date.today(),
    }

    return render(request, 'head_office/head_office.html', context)

@login_required(login_url='operator_login')
def delete_order(request, customer_id):
    if request.method == 'POST':
        operator_name = request.POST.get('operator_name')
        pin_code = request.POST.get('pin_code')

        try:
            user = DepartmentUser.objects.get(username=operator_name)
            DEPARTMENT_MAP = {
                "customer_service": (config('CS_OPERATOR_USERNAME', default=''), config('CS_OPERATOR_PIN', default='')),
                "financial_department": (config('FD_OPERATOR_USERNAME', default=''), config('FD_OPERATOR_PIN', default='')),
                "delivery_department": (config('DD_OPERATOR_USERNAME', default=''), config('DD_OPERATOR_PIN', default='')),
                "head_office": (config('HO_OPERATOR_USERNAME', default=''), config('HO_OPERATOR_PIN', default=''))
            }
            
            correct_pin = DEPARTMENT_MAP.get("head_office")[1]

            if pin_code == correct_pin:
                customer = Customer.objects.get(id=customer_id)
                customer.delete()
                messages.success(request, 'Order successfully deleted!')
            else:
                messages.error(request, 'Incorrect pin code!')

        except DepartmentUser.DoesNotExist:
            messages.error(request, 'Invalid operator name')

        return redirect(reverse('head_office:view_head_office'))

    return redirect(reverse('head_office:view_head_office'))
