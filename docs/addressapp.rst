==========
Address
==========
1. **METHOD:**
GET:
::
	api/v1/addresses

    - This method list all the address related to district ,municipality and ward:


==========
Geography
==========
1. **URL:**
::

    Get and Post:api/v1/geography

    Put : api/v1/geography/<geography_id>



2. **METHOD:**
GET:
::

    - This method list all the Geography:


3. **METHOD:**
POST:
::

- This Method is used for adding a Geography:

**Body_Content**


- district: ChoiceField(required)
- municipality: ChoiceField(required)
- ward: PositiveIntegerField()


4. **Put:**
POST:
::

- This Method is used for updating a geography:



==============
Activitie
==============
1. **URL:**
::

    Get:api/v1/events

2. **METHOD:**
GET:
::

    - This method list all the activitie:




==============
ActivitieArea
==============
1. **URL:**
::

    Get and Post:api/v1/activities

    Put : api/v1/activities/<activities_id>

    - activities_id: CharField (activities_id as a parameter)


2. **METHOD:**
GET:
::

    - This method list all the activitiearea:


3. **METHOD:**
POST:
::

- This Method is used for adding a activitiearea:

**Body_Content**


- activity id : ForeignKey(required) ie Activity id
- name: String()


4. **Put:**
POST:
::

- This Method is used for updating a activities:


==========
Recall
==========
1. **METHOD:**
GET:
::
	api/v1/recalls/<geography_id>

    - This method list all the recall for the patients:
    - this screen should be show only when health post is click in acticities section:


