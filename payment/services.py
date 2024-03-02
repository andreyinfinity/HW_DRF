import stripe

from config.settings import STRIPE_KEY
from payment.models import Payments

stripe.api_key = STRIPE_KEY


def create_stripe_product(product_name: str):
    """Функция создания продукта в Stripe"""
    stripe_product = stripe.Product.create(name=product_name)
    return stripe_product.id


def create_stripe_price(stripe_product_id: str, product_price: int):
    """Функция создания цены в Stripe"""
    stripe_price = stripe.Price.create(
        currency='rub',
        unit_amount=product_price * 100,
        product=stripe_product_id
    )
    return stripe_price.id


def create_stripe_session(stripe_price_id: str, quantity: int = 1):
    """Функция создания сессии в Stripe"""
    success_url = f"http://localhost:8000/payment/success/"
    session = stripe.checkout.Session.create(
        success_url=success_url,
        line_items=[{"price": stripe_price_id, "quantity": quantity}],
        mode="payment",
    )
    return session


def create_stripe_payment(product):
    """Функция создания платежа в Stripe."""
    if not product.stripe_product:
        stripe_product = create_stripe_product(product.name)
        stripe_price = create_stripe_price(stripe_product, product.price)
    else:
        stripe_price = product.stripe_price
        stripe_product = product.stripe_product
    stripe_session = create_stripe_session(stripe_price)
    stripe_payment = {
        "stripe_product": stripe_product,
        "stripe_session_id": stripe_session.id,
        "stripe_payment_link": stripe_session.url,
        "amount": stripe_session.amount_total
    }
    return stripe_payment
