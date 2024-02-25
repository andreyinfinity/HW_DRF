import stripe
from config.settings import STRIPE_KEY
from payment.models import Payments

stripe.api_key = STRIPE_KEY


def buy_course(course, user):
    """Получение ссылки на оплату курса"""
    price_params = {
        'currency': 'rub',
        'unit_amount': course.price * 100,
        'product_data': {"name": course.name}
    }
    price = stripe.Price.create(**price_params)
    success_url = f"http://localhost:8000/success/"
    session = stripe.checkout.Session.create(
        success_url=success_url,
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
    )
    Payments.objects.create(
        user=user,
        paid_course=course,
        payment_amount=course.price,
        payment_method='transfer',
        transaction_id=session.id,
        status='unpaid'
    )
    return session.url
