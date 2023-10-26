from django.shortcuts import render, redirect
from .models import Payment
from .forms import PaymentForm
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from delivery_department.models import Delivery

import logging

# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY


logger = logging.getLogger(__name__)

@login_required(login_url='operator_login')
def view_payments(request):
    payments = Payment.objects.filter(status="Pending Payment")
    
    just_logged_in = request.session.get('just_logged_in', False)
    if just_logged_in:
        del request.session['just_logged_in']
    
    if request.session.pop('payment_processed', False):
        message = "Payment Processed"
    else:
        message = ""
    
    context = {
        'payments': payments, 
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
        'just_logged_in': just_logged_in,
        'message': message  
    }
    
    return render(request, 'financial_department/payments.html', context)
