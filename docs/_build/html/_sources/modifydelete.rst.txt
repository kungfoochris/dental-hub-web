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
- reason_for_deletion: Enum[ accidental_entry, duplicate_encounter,incorrect_patient,incorrect_user and other]
- other_reason_for_deletion: Text()
- flag : ChoiceField()




- if success:
**Response**
::

    {
        "message":"Your request sent successfully."
    }
    
    
- if fails:
**Response**
::
    

    - if user tries to send request for encounter that doesn't exists
    {
        "message":"Encounter doesn't exists."
    }
    - if active=False in encounter
    {
        "message":"This encounter has already been deleted."   
    }

     - if modify delete request has already been sent 3 times
    {
        "message":"Your request limit already reached."
    }

     - if currently flag='modify' or flag='delete'
    {
        "message":"You already have a request sent."
    }

     - if flag='modify' chosen and field reason_for_modification left empty
    {
        "message":"Please enter reason for modification." 
    }

     - if flag='delete' chosen and reason_for_deletion='other' but left other_reason_for_deletion empty
    {
        "message":"You should enter the field either reason for deletion or other reason for deletion." 
    }

   

**Unsuccessful Responses**

- For Modify
::

    - if delete request is sent and then user tries to send modification request to that encounter then
    **Response:**
    "message":"You have sent delete request so you cannot send modify request."

    -if user has not response to previous modify request i.e. if modify_status is not modified then
    **Response:**
    "message":"You cannot send modify request before you response to previous request."


- For Delete
::

    - if delete request is sent and then user again tries to send delete request
    **Response:**
    "message":"You already have a delete request sent for this encounter."

    - if user choose reason_for_deletion  "other" and keep other_reason_for_deletion field empty
    **Response:**
    "message":"You should enter the field either reason for deletion or other reason for deletion."


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


    -if initially  delete_status is pending and you pass delete_status='deleted'
        {
            "message":"Encounter deleted successfully."
        }



    -if initially  delete_status is pending and you pass delete_status='rejected'
        {
            "message":"Flag Delete request is rejected."
        }



    -if initially  modify_status is pending and you pass modify_status='approved'
        {
            "message":"Modification request approved."
        }


    -if initially  modify_status is pending and you pass modify_status='rejected'
        {
            "message":"Modification request rejected."
        }



    -if initially neither  modify_status is pending nor delete_status is 
        {
            "message":"Neither modify nor delete action performed"
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


    - if success i.e. if you pass modify_status='modified' from form
        {
            
            "message":"Encounter modified successfully and flag killed.",
        }
    
    - if fails: i.e. if you pass modify_status other than 'modified'
        {
            
            "message":"Only modify status equals to modified can kill tha flag."
        }


    - if fails: i.e. if initially the modify_status is not equals to 'approved'
        {
            
            "message":" modify status most be approved before killing flag."
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

    - if deleted encounter exists and flag with that encounter id and delete_status='deleted' and flag author is the login user

    {
        'messsage':'Encounter restored successfully.'

    }

    - if restoration time is expired
    {
        'message':"Restoration time expired."

    }

    - if flag doesnt exists
     {
        'message':"flag doesn't exists."

    }

    - if no encounter is found with that entered encounter id
    {
        'message':"No encounter deleted found."
    }





return Response({'messsage':'Encounter restored successfully.'}, status=200)
                return Response({'message':"Restoration time expired."}, status=400)
            return Response({"message":"flag doesn't exists"},status=400)
        return Response({'message':"No encounter deleted found."}, status=400)



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
        'message':'All the encounter with restoration date expired are removed from recycle bin'

    }






