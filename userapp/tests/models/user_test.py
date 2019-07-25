# -*- coding:utf-8 -*-
import pytest
from mixer.backend.django  import mixer
from faker import Faker

from userapp.models import User

pytestmark = pytest.mark.django_db
fake = Faker()

class TestUserModel():

    def test_init(self):
        user_obj = mixer.blend(User)
        assert user_obj== User.objects.last(), "should create User instance"

    def test_str(self):
        user_obj = mixer.blend(User)
        assert str(user_obj) == user_obj.full_name, \
        "Should return the full_name"

    def test_full_name(self):
        user_obj = mixer.blend(User)
        if user_obj.middle_name is None:
            assert user_obj.full_name == '%s %s' %(str(user_obj.first_name),str(user_obj.last_name)),\
            'full name is matched'
        else:
            assert user_obj.full_name == '%s %s %s' %(str(user_obj.first_name),str(user_obj.middle_name),str(user_obj.last_name)),\
            'full name is matched'

    def test_staff_admin_superuser(self):
        user_obj = mixer.blend(User)
        assert user_obj.is_admin == False
        assert user_obj.is_staff == False
        assert user_obj.is_superuser == False
        assert user_obj.is_active == True
