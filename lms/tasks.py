from celery import shared_task
from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import EmailMessage

from lms.models import Subscribe


@shared_task
def send_notification(data: dict):
    course_id = data.get("course")
    lesson = data.get("name")
    subscribers = Subscribe.objects.filter(course=course_id)
    print(subscribers)

    for subscriber in subscribers:
        to_email = subscriber.subscriber.email
        first_name = subscriber.subscriber.first_name
        course = subscriber.course.name
        mail_subject = f"Курс {course} был обновлен"
        message = f"Привет, {first_name}! Курс {course} был обновлен."
        EmailMessage(subject=mail_subject, body=message, to=to_email, from_email=EMAIL_HOST_USER).send()
