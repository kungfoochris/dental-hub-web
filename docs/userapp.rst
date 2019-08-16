==============================
View all Appser and Register
==============================

1. **URL:** `View all Appuser and Register <http://api/v1/users>`_
::

    http://api/v1/users

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
- username: String(required)
- image: ImageField(required)
- password:CharField(required)


===============
ForgetPassword
===============
1. **URL:** `ForgetPassword <http://api/v1/users/forgetpassword>`_
::

    http://api/v1/users/forgetpassword


2. **METHOD:**
POST:
::

- This Method is used to request for forgetpassword:

**Body_Content**

- email: Email(required)



================
ResetPassword
================
1. **URL:** `Resetpassword <http://api/v1/users/resetpassword>`_
::

    http://api/v1/users/resetpassword


2. **METHOD:**
POST:
::

- This Method is used for reset a password:

**Body_Content**

- token: String(required)
- password: String(required)
- confirm_password: String(required)



=========
Profile
=========

1. **URL:** `profile of user <http://api/v1/profile>`_
::

    http://api/v1/profile

2. **METHOD:**
GET:
::

    - This method list the profilr of user:


==============
UpdateAppuser
==============

1. **URL:** `update user profile <http://api/v1/profile/update>`_
::

    http://api/v1/profile/update


2. **METHOD:**
POST:
::

- This method is used to update a profile of user:

    **Body_Content**
- image: ImageField(required)




===============
ChangePassword
===============

1. **URL:** `View all Appuser and Register <http://api/v1/users>`_
::

    http://api/v1/users/changepassword


3. **METHOD:**
POST:
::

- This method is used to change a password:

    **Body_Content**
- old_password: string(required)
- new_password: string(required)
- confirm_password: string(required)




