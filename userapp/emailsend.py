from userapp.models import User
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from celery import shared_task

@shared_task
def emailsend(user_id,text_content,template_name,password):
	try:
		user=User.objects.get(id = user_id)
		from_email = settings.DEFAULT_FROM_EMAIL
		subject = 'Dental_Alert'
		recipients = [user.email]
		context = {
		'user': user.first_name,
		'password': password
		}
		html_content = render_to_string(template_name, context)
		email = EmailMultiAlternatives(subject, text_content,from_email, recipients)
		email.attach_alternative(html_content, "text/html")
		email.send()
	except  User.DoesNotExist:
		pass
