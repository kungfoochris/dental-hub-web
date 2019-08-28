==========
Encounter
==========
1. **URL:**
::

    Get and Post:api/v1/patients/<patient_id>/encounters

    Put : api/v1/patients/<patient_id>/encounters/<encounter_id>

    - patient_id: CharField (patient_id as a parameter)
    - encounter_id:CharField (encounter_id ad a parameter)

2. **METHOD:**
GET:
::

    - This method list all the encounter patient:


3. **METHOD:**
POST:
::

- This Method is used for adding a encounter for patient:

**Body_Content**

- id : string()
- encounter_type: ChoiceField(required)
choice field are ({screeing:Checkup/Screeing,pain:Relief of pain,treatment plan: Continuation of treatment plan,other:Other Problem})
- other_detail: String()


4. **Put:**
POST:
::

- This Method is used for updating a encounter for patient:


==================
Encounter History
==================

1. **URL:**
::

    Get and Post : /api/v1/encounter/<encounter_id>/history
    Put: /api/v1/encounter/<encounter_id>/history/update

    - encounter_id: CharField(as a parameter)

2. **METHOD:**
GET:
::
    - This method list all the encounter history:

3. **METHOD:**
POST:
::

- This method is used to add a encounter of history:

    
    **Body_Content**
- bleeding: BooleanField()
- diabetes: BooleanField()
- fever: BooleanField()
- liver: BooleanField()
- seizures:BooleanField()
- hepatitis: BooleanField()
- hiv:BooleanField()
- no_allergies:BooleanField()
- allergies: String()
- no_underlying_medical:BoolenField()
- not_taking_medication: BoolenField()
- other: CharField()
- medication:CharField()
- no_medication:BooleanField()


4. **METHOD:**
PUT:
::
    - This method is used to update the encounter history:


=================
Encounter Refer
=================
1. **URL:**
::

    Get and Post : /api/v1/encounter/<encounter_id>refer
    Put : /api/v1/encounter/<encounter_id>refer/update

    - encounter_id: CharField(required) as a parameter


2. **METHOD:**
GET:
::

    - This method list all the encounter refer:

3. **METHOD:**
POST:
::

- This Method is used to add a refer:

**Body_Content**

- no_referal: BooleanField()
- health_post: BooleanField()
- dentist: BooleanField()
- physician: BooleanField()
- hygienist: BooleanField()
- other: CharField()
- time : timefield(),format:12:23:00 
- date : DateTimeField(required)

4. **METHOD:**
PUT:
::

- This Method is used to update a refer encounter:



====================
Encounter Screeing
====================
1. **URL:**
::

   Get and Post : /api/v1/encounter/<encounter_id>/screening
   Put : /api/v1/encounter/<encounter_id>/screening/update

   - encounter_id: CharField(as a parameter)

2. **METHOD:**
GET:
::

    - This method list all the encounter screeing:


3. **METHOD:**
POST:
::

- This Method is used for add a screeing encounter:

**Body_Content**

- caries_risk: ChoiceField(required)
	choice field are (Low,High,Medium)
- primary_teeth: IntegerField(required)
- permanent_teeth: IntegerField(required)
- postiror_teeth: BooleanField()
- anterior_teeth: BooleanField()
- need_sealant: BooleanField()
- reversible_pulpitis: Bool:eanField()
- art: BooleanField()
- extraction: BooleanField()
- need_sdf: BooleanField()
- blood_pressure:ChoiceField()
  choice field are (Low,High,Normal)

4. **METHOD:**
PUT:
::

    - This method is used to update a screeing encounter:




====================
Encounter Treatment
====================
1. **URL:**
::

   Get and Post : /api/v1/encounter/<encounter_id>/treatment
   Put : /api/v1/encounter/<encounter_id>/treatment/update

   - encounter_id: CharField(as a parameter)

2. **METHOD:**
GET:
::

    - This method list all the encounter treatment:


3. **METHOD:**
POST:
::

- This Method is used for add a treatment encounter:

**Body_Content**

- teeth: ChoiceField()
    choice field are (SMART,SDF,SEAL,ART,'EXO','UNTR','NONE')
- teeth should be from 1 to 32

- primary_teeth: ChoiceField()
    choice field are (SMART,SDF,SEAL,ART,'EXO','UNTR','NONE')
- primary_teeth should be from 1 to 20
- fluoride_varnish: BooleanField()
- treatment_complete: BooleanField()
- note: TextField()
- whole_mouth:BoolenField()

4. **METHOD:**
PUT:
::

    - This method is used to update a screeing encounter:





