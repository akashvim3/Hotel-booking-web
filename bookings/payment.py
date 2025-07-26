import stripe
from django.conf import settings

stripe.api_key = 'your-stripe-secret-key'  # Replace with your real Stripe secret key

def create_payment_intent(amount, currency='usd'):
    return stripe.PaymentIntent.create(
        amount=int(amount * 100),  # Stripe expects amount in cents
        currency=currency,
    )
