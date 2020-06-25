Encounterapp
=============


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
- encounter_type: ChoiceField(required)
  choice field are ({screeing:Checkup/Screeing,pain:Relief of pain,treatment plan: Continuation of treatment plan,other:Other Problem})
- other_detail: String()
- created_at: DateField(required)


4. **Put:**
POST:
::

- This Method is used for updating a encounter for patient:

- encounter_type: ChoiceField(required)
  choice field are ({screeing:Checkup/Screeing,pain:Relief of pain,treatment plan: Continuation of treatment plan,other:Other Problem})
- other_detail: String()
- updated_at: DateField(required)
- updated_by: Foreigne Key(User)


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
- blood_disorder: BooleanField()
- diabetes: BooleanField()
- liver_problem: BooleanField()
- rheumatic_fever: BooleanField()
- epilepsy_or_seizures:BooleanField()
- hepatitis_b_or_c: BooleanField()
- hiv:BooleanField()
- no_allergies:BooleanField()
- allergies: String()
- no_underlying_medical_condition:BoolenField()
- not_taking_any_medications: BoolenField()
- other: CharField()
- no_medications:BooleanField()
- medication:CharField()
- no_medication:BooleanField()
- encounter_id : Foreigne Key(Encounter)required
- created_at: DateField(required)



4. **METHOD:**
PUT:
::
    - This method is used to update the encounter history:

      **Body_Content**

- blood_disorder: BooleanField()
- diabetes: BooleanField()
- liver_problem: BooleanField()
- rheumatic_fever: BooleanField()
- epilepsy_or_seizures:BooleanField()
- hepatitis_b_or_c: BooleanField()
- hiv:BooleanField()
- no_allergies:BooleanField()
- allergies: String()
- no_underlying_medical_condition:BoolenField()
- not_taking_any_medications: BoolenField()
- other: CharField()
- no_medications:BooleanField()
- medication:CharField()
- no_medication:BooleanField()
- updated_at: DateField()



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
- created_at: DateField(required)

- encounter_id : Foreigne Key(Encounter)required

4. **METHOD:**
PUT:
::

- This Method is used to update a refer encounter:


**Body_Content**

- no_referal: BooleanField()
- health_post: BooleanField()
- dentist: BooleanField()
- physician: BooleanField()
- hygienist: BooleanField()
- other: CharField()
- updated_at: DateField()




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

- carries_risk: ChoiceField(required)
	choice field are (Low,High,Medium)
- decayed_primary_teeth: IntegerField(required)
- decayed_permanent_teeth: IntegerField(required)
- cavity_permanent_posterior_teeth: BooleanField()
- cavity_permanent_anterior_teeth: BooleanField()
- need_sealant: BooleanField()
- reversible_pulpitis: Bool:eanField()
- need_art_filling: BooleanField()
- need_extraction: BooleanField()
- need_sdf: BooleanField()
- high_blood_pressure:BooleanField()
- low_blood_pressure:BooleanField()
- thyroid_disorder:BooleanField()
- created_at: DateField(required)
- encounter_id : Foreigne Key(Encounter)required
- active_infection:BooleanField() 

4. **METHOD:**
PUT:
::


**Body_Content**

- carries_risk: ChoiceField(required)
  choice field are (Low,High,Medium)
- decayed_primary_teeth: IntegerField(required)
- decayed_permanent_teeth: IntegerField(required)
- cavity_permanent_posterior_teeth: BooleanField()
- cavity_permanent_anterior_teeth: BooleanField()
- need_sealant: BooleanField()
- reversible_pulpitis: Bool:eanField()
- need_art_filling: BooleanField()
- need_extraction: BooleanField()
- need_sdf: BooleanField()
- high_blood_pressure:BooleanField()
- low_blood_pressure:BooleanField()
- thyroid_disorder:BooleanField()
- updated_at: DateField()
- active_infection:BooleanField() 

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
    choice field are (SMART,SDF,SEAL,ART,'EXO','UNTR','NONE','SMART')
- tooth should be from 11 to 18 , 21 to 28 ,31 to 38, 41 to 48

- primary_teeth: ChoiceField()
    choice field are (SMART,SDF,SEAL,ART,'EXO','UNTR','NONE')
- primary_teeth should be from 51 to 55, 61 to 65 , 71 to 75 and 81 to 85


- fv_applied: BooleanField()
- treatment_plan_complete: BooleanField()
- note: TextField()
- sdf_whole_mouth:BoolenField()
- created_at: DateField(required)
- encounter_id : Foreigne Key(Encounter)required

4. **METHOD:**
PUT:
::

    - This method is used to update a screeing encounter:


- teeth: ChoiceField()
    choice field are (SMART,SDF,SEAL,ART,'EXO','UNTR','NONE','SMART')
- tooth should be from 11 to 18 , 21 to 28 ,31 to 38, 41 to 48

- primary_teeth: ChoiceField()
    choice field are (SMART,SDF,SEAL,ART,'EXO','UNTR','NONE')
- primary_teeth should be from 51 to 55, 61 to 65 , 71 to 75 and 81 to 85


- fv_applied: BooleanField()
- treatment_plan_complete: BooleanField()
- note: TextField()
- sdf_whole_mouth:BoolenField()
- updated_at: DateField()



=============
ModifyDelete:Mark for deletion
=============
1. **URL:**
::

    Get and Post:api/v1/modifydelete


2. **METHOD:**
POST:
::

- This Method is used for adding a status to the encounter:


**Body_Content**

- encounter: ForeignKey(required)
- reason_for_modification: TextField()
- reason_for_deletion: CharField()
- other_reason_for_deletion: ChoiceField()
- flag : ChoiceField()


**Response**

- For modify
::

    {
        "encounter": "26F7939BE14D4D31B1FB25F42824B618",
        "reason_for_modification": "i just want to",
        "reason_for_deletion": "accidental_entry",
        "flag": "modify"
    }


- For delete
::

    {
        "encounter": "26F7939BE14D4D31B1FB25F42824B618",
        "reason_for_deletion": "accidental_entry",
        "flag": "delete"
    }


**Unsuccessful Responses**

- For Modify
::

    - if delete request is sent and then user tries to send modification request to that encounter then
    **Response:**
    "You have sent delete request so you cannot send modify request."

    -if user has not response to previous modify request i.e. if modify_status is not modified then
    **Response:**
    "You cannot send modify request before you response to previous request."


- For Delete
::

    - if delete request is sent and then user again tries to send delete request
    **Response:**
    "You already have a delete request sent for this encounter."

    - if user choose reason_for_deletion  "other" and keep other_reason_for_deletion field empty
    **Response:**
    "You should enter the field either reason for deletion or other reason for deletion."








