==============================
View all Appser and Register
==============================

1. **URL:** `View all Appuser and Register <http://localhost/api/v1/users>`_
::

    http://localhost/api/v1/users

2. **METHOD:**
GET:
::

    - This method list all the appuser:

3. **METHOD:**
POST:
::

- This method is used to register a appuser:

    **Body_Content**
- first_name: string(required)
- last_name: string(required)
- middle_name: string()
- email: EmailField(required)
- image: ImageField(required)
- password:CharField(required)








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





===============
ForgetPassword
===============
1. **URL:** `ForgetPassword <http://localhost/api/v1/users/forgetpassword>`_
::

    http://localhost/api/v1/users/forgetpassword


2. **METHOD:**
POST:
::

- This Method is used to request for forgetpassword:

**Body_Content**

- email: Email(required)



================
ResetPassword
================
1. **URL:** `Resetpassword <http://localhost/api/v1/users/resetpassword>`_
::

    http://localhost/api/v1/users/resetpassword


2. **METHOD:**
POST:
::

- This Method is used for reset a password:

**Body_Content**

- token: String(required)
- password: String(required)
- confirm_password: String(required)


