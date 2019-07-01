# from fcm_django.models import FCMDevice
from userapp.models import User
from patientapp.models import Patient
from django.http import HttpResponse
from django.db.models import Sum
from django.db.models import Count
from django_seed import Seed
from faker import Faker
from mixer.backend.django  import mixer
fake = Faker()

def seed(request):
	try:
		User.objects.create_superuser(email='admin@gmail.com',password='iam100good')
		print("create superuser")
	except:
		for i in range(1,10):
			user=mixer.blend(User)
			mixer.blend(Patient)
	return HttpResponse("it works")

