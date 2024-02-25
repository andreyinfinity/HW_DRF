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
    success_url = f"http://localhost:8000/lms/success/"
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


def check_payment_status(user):
    """Проверка статуса платежей пользователя в системе Stripe"""
    payments = Payments.objects.filter(user=user, status='unpaid')
    orders = []
    unpaid = []
    for payment in payments:
        session = stripe.checkout.Session.retrieve(id=payment.transaction_id)
        if session.payment_status == 'paid':
            payment.status = 'paid'
            payment.save()
            orders.append(payment.paid_course.name)
        else:
            unpaid.append({"курс": payment.paid_course.name, "ссылка на оплату": session.url})

    return {"Успешная оплата": orders, "Не оплачено": unpaid}
