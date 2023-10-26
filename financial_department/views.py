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

@login_required(login_url='operator_login')
def process_payment(request, payment_id):
    payment = Payment.objects.get(id=payment_id)
    message = ""

    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        
        if form.is_valid():
            amount_to_charge = 1000 
            try:
                stripe_charge = stripe.Charge.create(
                    amount=amount_to_charge,
                    currency='gbp',
                    description=f'Charge for {payment.customer.full_name}',
                    source='tok_visa'  
                )
                
                if stripe_charge.paid:
                   form.save()
                   payment.status = "Payment Processed"
                   payment.save()
                   Delivery.objects.create(customer=payment.customer, delivery_date=payment.customer.requested_delivery_date)
                   request.session['payment_processed'] = True  
                   logger.info(f"Successfully processed payment for {payment.customer.full_name}")
                   return redirect('financial_department:view_payments')
                else:
                    message = "Payment failed."
                    logger.warning(f"Payment failed for {payment.customer.full_name}")
            except stripe.error.StripeError as e:
                message = f"Error processing payment: {e}"
                logger.error(f"Stripe error for {payment.customer.full_name}: {e}")
    else:
        form = PaymentForm(instance=payment)
    
    context = {
        'form': form, 
        'message': message, 
        'payments': [payment],
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'financial_department/payments.html', context)
