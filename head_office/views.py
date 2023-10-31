from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from customer_service.models import Customer
from financial_department.models import Payment
from delivery_department.models import Delivery
from django.db.models import F
from datetime import date
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

# Create your views here.
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

def delete_payment(request, payment_id):
    if request.method == "POST":
        payment = get_object_or_404(Payment, id=payment_id)
        payment.delete()
    return redirect(reverse('view_head_office'))

def delete_delivery(request, delivery_id):
    if request.method == "POST":
        delivery = get_object_or_404(Delivery, id=delivery_id)
        delivery.delete()
    return redirect(reverse('view_head_office'))