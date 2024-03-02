from celery import shared_task
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from lms.models import Subscribe


@shared_task
def send_notification(data: dict):
    """Функция отправки уведомлений при обновлении курса"""
    course_id = data.get("course")
    # Получение подписчиков курса
    subscribers = Subscribe.objects.filter(course=course_id)
    if subscribers:
        for subscriber in subscribers:
            to_email = subscriber.subscriber.email
            first_name = subscriber.subscriber.first_name
            course = subscriber.course.name
            mail_subject = f"Курс {course} был обновлен"
            message = f"Привет, {first_name}! Курс {course} был обновлен."
            send_mail(
                subject=mail_subject,
                message=message,
                recipient_list=[to_email],
                from_email=EMAIL_HOST_USER
            )
