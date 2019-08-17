==============================
View all Patients and Register
==============================

1. **METHOD:**
GET:
::
	http://api/v1/patients

    - This method list all the patients:

2. **METHOD:**
GET:
::
	http://api/v1/patients/<geography_id>

    - This method list all the patients of the required geography area:
    - geography_id must be as a parameter

3. **METHOD:**
POST:
::
	http://api/v1/patients


- This method is used to register a patients:

    **Body_Content**

- id : string()
- geography_id: string(required)
- activityarea_id : string(required)
- first_name: string(required)
- last_name: string(required)
- middle_name: string()
- gender: choicefield(required)
  male, female. other
- dob(date of birth): DateTimeField(required)
- phone(phone number):CharField(required)
- author : ForeignRelationship()
- date : autofield()
- latitude: DecimalField(required)
- longitude: DecimalField(required)
- ward : foreignkey(required) 
- municipality : foreignkey(required)
- district: foreignkey(required)