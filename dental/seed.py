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
from addressapp.models import Address, District, Municipality ,Ward
import json
fake = Faker()

def seed(request):
	User.objects.create(username='abhiyantrik',email='prabin@abhiyantrik.com',password='dental123',first_name='admin',last_name='user',admin=True,staff=True)
	with open('./nepal.json') as write_file:
		data=json.load(write_file)
		for data_obj in data:
			district_obj1 = District.objects.create(name=data_obj['name'])
			for muncipality_obj in data_obj['municipalities']:
				muncipality_obj1 = Municipality.objects.create(district=district_obj1,name=muncipality_obj['name'],category=muncipality_obj['type'])
				for i in range(1,muncipality_obj['wards']+1):
					Ward.objects.create(municipality=muncipality_obj1,ward=i)
	return HttpResponse("it works")




# def productionseed(request):
# 	try:
# 		User.objects.create_superuser(email='info@abhiyantrik.com',password='dental123')
# 		User.objects.create(email='ram@gmail.com',password='dental123',first_name="Ram",last_name="Karki")
# 		User.objects.create(email='hari@gmail.com',password='dental123',first_name="Hari",last_name="Karki")
# 		User.objects.create(email='kabi@gmail.com',password='dental123',first_name="Kabi",last_name="Karki")
# 		User.objects.create(email='saurav@gmail.com',password='dental123',first_name="Saurav",last_name="Karki")
# 		User.objects.create(email='bimu@gmail.com',password='dental123',first_name="Bishal",last_name="Karki")


