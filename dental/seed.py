# from fcm_django.models import FCMDevice
from userapp.models import User
from patientapp.models import Patient
from addressapp.models import Geography,ActivityArea
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
		print("seed")
		# for i in range(1,10):
		# 	user=mixer.blend(User)
		# 	mixer.blend(Patient)
		# 	mixer.blend(ActivityArea)
		# 	mixer.blend(Geography)
	return HttpResponse("it works")



# def productionseed(request):
# 	try:
# 		User.objects.create_superuser(email='info@abhiyantrik.com',password='dental123')
# 		User.objects.create(email='ram@gmail.com',password='dental123',first_name="Ram",last_name="Karki")
# 		User.objects.create(email='hari@gmail.com',password='dental123',first_name="Hari",last_name="Karki")
# 		User.objects.create(email='kabi@gmail.com',password='dental123',first_name="Kabi",last_name="Karki")
# 		User.objects.create(email='saurav@gmail.com',password='dental123',first_name="Saurav",last_name="Karki")
# 		User.objects.create(email='bimu@gmail.com',password='dental123',first_name="Bishal",last_name="Karki")


