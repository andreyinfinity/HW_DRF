import stripe
from config.settings import STRIPE_KEY
from lms.models import Course, Lesson
from payment.models import Payments
from users.models import User

stripe.api_key = STRIPE_KEY


def create_stripe_product(product_type: str, product_name: str) -> str:
    """Функция создания продукта в Stripe"""
    stripe_product = stripe.Product.create(
        name=product_name,
        metadata={"product_type": product_type}
    )
    return stripe_product.id


def create_stripe_price(stripe_product_id: str, product_price: int) -> str:
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
    return session.url, session.id


def create_payment(payment: dict) -> dict:
    """
    Функция создания платежа в Stripe.
    На вход передается JSON
    {'product_type': 'course or lesson',
    'product_id: 'pk',
    'user_id': 'pk'}
    """
    product_type = payment['product_type']
    product_id = int(payment['product_id'])
    user_id = int(payment['user_id'])
    user = User.objects.get(pk=user_id)

    if product_type == "course":
        product = Course.objects.filter(pk=product_id).first()
        if product:
            product_stripe_id = create_stripe_product(product_type="course", product_name=product.name)
            price_stripe_id = create_stripe_price(product_stripe_id, product.price)
            payment_stripe_url, session_stripe_id = create_stripe_session(price_stripe_id)

            Payments.objects.create(
                user=user,
                paid_course=product,
                payment_amount=product.price,
                payment_method='transfer',
                product=product_stripe_id,
                transaction_id=session_stripe_id,
                transaction_link=payment_stripe_url,
                status='unpaid'
            )
    elif product_type == "lesson":
        product = Lesson.objects.filter(pk=product_id).first()
        if product:
            product_stripe_id = create_stripe_product(product_type="lesson", product_name=product.name)
            price_stripe_id = create_stripe_price(product_stripe_id, product.price)
            payment_stripe_url, session_stripe_id = create_stripe_session(price_stripe_id)

            Payments.objects.create(
                user=user,
                paid_lesson=product,
                payment_amount=product.price,
                payment_method='transfer',
                product=product_stripe_id,
                transaction_id=session_stripe_id,
                transaction_link=payment_stripe_url,
                status='unpaid'
            )
    return {'payment_stripe_url': payment_stripe_url}


def check_payment_status(payment: dict):
    """
    Функция проверки платежа в Stripe.
    На вход передается JSON
    {'product_type': 'course or lesson',
    'product_id: 'pk',
    'user_id': 'pk'}
    """
    product_type = payment['product_type']
    product_id = int(payment['product_id'])
    user_id = int(payment['user_id'])
    if product_type == 'course':
        payment = Payments.objects.filter(user_id=user_id, paid_course_id=product_id).first()
        session = stripe.checkout.Session.retrieve(id=payment.transaction_id)
        if session.payment_status == 'paid':
            payment.status = 'paid'
            payment.save()
            return {"Статус оплаты": "успешно"}
        return {"Статус оплаты": "не оплачено", "Ссылка на оплату": session.url}
    elif product_type == 'lesson':
        payment = Payments.objects.filter(user_id=user_id, paid_lesson_id=product_id).first()
        session = stripe.checkout.Session.retrieve(id=payment.transaction_id)
        if session.payment_status == 'paid':
            payment.status = 'paid'
            payment.save()
            return {"Статус оплаты": "успешно"}
        return {"Статус оплаты": "не оплачено", "Ссылка на оплату": session.url}
