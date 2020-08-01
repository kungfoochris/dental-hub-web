Mark For deletion
====================



=================================
ModifyDelete:Mark for deletion
=================================
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
    "status": "success",
    "data": {
        "encounter": "26F7939BE14D4D31B1FB25F42824B618",
        "reason_for_modification": "i just want to",
        "flag": "modify"
    },
    "message": "Modify request successfully sent."
}

- For delete
::

    {
    "status": "success",
    "data": {
        "encounter": "26F7939BE14D4D31B1FB25F42824B618",
        "reason_for_deletion": "accidental_entry",
        "other_reason_for_deletion": "",
        "flag": "delete"
    },
    "message": "Delete request successfully sent."
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


======================
EncounterAdminStatus
======================
1. **URL:**
::

    Get and Put:api/v1/encounterstatus


2. **METHOD:**
PUT:
::

- This Method is used for updating a status to the encounter eg. approving the modify request 
- it can be done only by admin


**Body_Content**

- modify_status: ChoiceField()
- delete_status: ChoiceField()



**Response**

::

    {
        "modify_status": "pending",
        "delete_status": "",

    }



======================
EncounterFlagDead
======================
1. **URL:**
::

    Put:api/v1/flagdead/<id>


2. **METHOD:**
PUT:
::

- This Method is used for updating a status to the encounter either after user actually update the encounter or after the modify time is expired [after 7 days of approval of modify request]
- initially the modify_status has to be approved


**Body_Content**

- modify_status: ChoiceField()


**Response**

::

    {
        "modify_status": "modified",

    }



======================
Encounter Restore
======================

- It is used for restoring the deleted encounter from recycle bin

1. **URL:**
::

    Put:api/v1/encounterrestore/<encounter_id>


2. **METHOD:**
PUT:


**Body_Content**

- No parameters required


**Response**

::

    {
        'Encounter restored successfully.'

    }





======================
Recyclebin
======================

- this is the list of the encounters deleted

1. **URL:**
::

    Put:api/v1/recyclebin


2. **METHOD:**
GET:
::

    [
        {
            "id": "6113872899F1497280F38DC45AE37BC6",
            "geography": 2,
            "activity_area": 2,
            "patient": "0C13D64AD42442369E165A8350F36E07",
            "author": "E5B58A7CE5DE44F28BAE8C2E60AA4140",
            "date": "2020-08-01T15:00:21.819299+05:45",
            "encounter_type": "Checkup / Screening",
            "other_problem": "kk kk hunx",
            "created_at": "2020-08-01T14:09:00+05:45",
            "updated_by": "E5B58A7CE5DE44F28BAE8C2E60AA4140",
            "updated_at": "2020-08-01",
            "history": null,
            "screening": null,
            "treatment": null,
            "referral": null,
            "active": false,
            "request_counter": 2
        }
    ]



======================
Check Modify Expiry
======================

- here modification expiry date is checked and if found expired the flag is killed

1. **URL:**
::

    Post:api/v1/encounterrestore/<encounter_id>


2. **METHOD:**
POST:
::


**Body_Content**

- No parameters required


**Response**

::

    {
        'All the encounter flags with modify date expired are killed'

    }



======================
Check Restore Expiry
======================

- Here restoration expiry date is checked and if found expired then the encounter is removed from recyclebin

1. **URL:**
::

    Post:api/v1/checkrestoreexpiry


2. **METHOD:**
POST:



**Body_Content**

- No parameters required


**Response**

::

    {
        'All the encounter with restoration date expired are removed from recycle bin'

    }






