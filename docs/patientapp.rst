==============================
View all Patients and Register
==============================

1. **URL:** `View all Patients and Register <http://localhost/api/v1/patients>`_
::

    http://localhost/api/v1/patients

2. **METHOD:**
GET:
::

    - This method list all the patients:

3. **METHOD:**
POST:
::

- This method is used to register a patients:

    **Body_Content**
- first_name: string(required)
- last_name: string(required)
- middle_name: string()
- gender: choicefield(required)
  male, female. other
- dob(date of birth): DateTimeField(required)
- phone(phone number):CharField(required)
- education : Charfield(required)
- author : ForeignRelationship()
- date : autofield()
- latitude: DecimalField(required)
- longitude: DecimalField(required)
- marital_status: choicefield(required)
- ward : PositiveIntegerField(required)
- city : CharField(required)
- state: CharField(required)
- country: CharField(required)
- street_address: CharField(required)
	(single , married)