from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CheckoutForm
from essential.models import *
import stripe
from django.conf import settings
from payments import get_payment_model 

# Create your views here.

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

@login_required
def checkout(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    purchased = Purchase.objects.filter(utente_id=request.user.id, corso_id=course.id).exists()
    user = request.user

    if (user.id == course.user_id):
        message = "Il corso è di tua proprietà!"
        messages.warning(request, message)
        return redirect("essential:createdcourses")
    elif purchased:
        message = "Hai già acquistato questo corso!"
        messages.warning(request, message)
        return redirect("users:dashboard")
    
    Payment = get_payment_model()

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            payment = Payment.objects.create(
                variant='stripe',
                description=f'Acquisto del corso {course.title}',
                total=course.price,
                currency='EUR',
                delivery=0,
                tax=0,
                status='waiting',
                billing_first_name=request.user.first_name,
                billing_last_name=request.user.last_name,
                billing_email=request.user.email,
                customer_ip_address=request.META.get('REMOTE_ADDR', '')
            )

            payment_intent = stripe.PaymentIntent.create(
                amount=int(course.price * 100),  # Stripe richiede gli importi in centesimi
                currency='eur',
                metadata={'integration_check': 'accept_a_payment'},
            )

            context = {
                'form': form,
                'course': course,
                'stripe_public_key': settings.STRIPE_TEST_PUBLIC_KEY,
                'client_secret': payment_intent['client_secret'],
            }
            return render(request, 'checkout.html', context)
    else:
        form = CheckoutForm()

    return render(request, 'checkout.html', {'form': form, 'course': course})