from datetime import date
tody_date = date.today()
def dobchange(bdate):
    t = str(bdate)
    year,month,day = t.split('-')
    print(month)
    print(day)
    if month == "01" and int(day) > 31:
        print("1st")
        dob = str(year) + "-" + month + "-" + "31"
    elif month == "02" and int(day) > 28:
        print("2nd")
        dob = str(year) + "-" + month + "-" + "28"

    elif month == "03" and int(day) > 31:
        print("3rd")
        dob = str(year) + "-" + month + "-" + "31"

    elif month == "04" and int(day) > 30:
        print("4th")
        dob = str(year) + "-" + month + "-" + "30"
    
    elif month == "05" and int(day) > 31:
        print("5th")
        dob = str(year) + "-" + month + "-" + "31"
    
    elif month == "06" and int(day) > 30:
        print("6th")
        dob = str(year) + "-" + month + "-" + "30"
    
    elif month == "07" and int(day) > 31:
        print("7th")
        dob = str(year) + "-" + month + "-" + "31"
    
    elif month == "08" and int(day) > 31:
        print("8th")
        dob = str(year) + "-" + month + "-" + "31"
    
    elif month == "09" and int(day) > 30:
        print("9th")
        dob = str(year) + "-" + month + "-" + "30"
    
    elif month == "10" and int(day) > 31:
        print("10th")
        dob = str(year) + "-" + month + "-" + "31"
    
    elif month == "11" and int(day) > 30:
        print("11th")
        dob = str(year) + "-" + month + "-" + "30"
    
    elif month == "12" and int(day) > 31:
        print("12th")
        dob = str(year) + "-" + month + "-" + "31"
    else:
        dob = bdate
    return dob

# print(dobchange(tody_date))

