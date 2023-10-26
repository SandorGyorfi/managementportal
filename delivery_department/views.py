from django.shortcuts import render, redirect, get_object_or_404
from .models import Delivery
from .forms import DeliveryForm
from django.contrib.auth.decorators import login_required
from datetime import date
from django.contrib import messages

# Create your views here.
@login_required(login_url='operator_login')
def view_deliveries(request):
    """
    Display all future deliveries, today's deliveries, and overdue deliveries.
    """

    all_future_deliveries = Delivery.objects.filter(delivery_date__gte=date.today()).exclude(status="Delivered")
    todays_deliveries = Delivery.objects.filter(delivery_date=date.today()).exclude(status="Delivered")
    overdue_deliveries = Delivery.objects.filter(delivery_date__lt=date.today()).exclude(status="Delivered")

    all_deliveries = list(overdue_deliveries) + sorted(list(all_future_deliveries), key=lambda x: x.delivery_date)
    
    just_logged_in = False
    if 'just_logged_in' in request.session:
        just_logged_in = True
        del request.session['just_logged_in']  

    return render(request, 'delivery_department/deliveries.html', {
        'all_deliveries': all_deliveries,
        'todays_deliveries': todays_deliveries,
        'today': date.today(),
        'just_logged_in': just_logged_in,
    })

@login_required(login_url='operator_login')
def update_delivery(request, delivery_id):
    """
    Update a specific delivery's details.
    """

    delivery = get_object_or_404(Delivery, id=delivery_id)
    customer = delivery.customer

    form = DeliveryForm(request.POST or None, instance=delivery)  

    if request.method == 'POST':
        if form.is_valid():
            delivery_instance = form.save(commit=False)
            delivery_instance.status = "Delivered"  
            delivery_instance.save()

            messages.success(request, 'Delivery Info Forwarded to Head Office Department!')

            return redirect('delivery_department:view_deliveries')
        

    return render(request, 'delivery_department/pickup_form.html', {'form': form, 'customer': customer})
