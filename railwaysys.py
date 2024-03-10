import mysql.connector as mc    
import datetime as d
import time
import random
from email_validator import validate_email,EmailNotValidError
#add your own mysql host,user,password,database
mydb = mc.connect(
  host = "localhost",
  user = "root",
  password = "dark",
  database = 'railway')
cursorobject = mydb.cursor()
todaydate = d.date.today()
date = d.datetime.now()
def login():
    global userid
    username = input("Enter your username:")
    password = input("Enter your password:")
    mycmd = "SELECT* FROM LOGIN WHERE USERNAME='{}' AND PASSWORD='{}'".format(username,password)
    cursorobject.execute(mycmd)
    data = cursorobject.fetchall()
    if data == []:
        verification = False
    elif data[0][0] == username and data[0][1] == password:
        verification = True
    else:
        verification = False
    if verification == True :
        print("LOGIN SUCCESSFUL")
        userid = data[0][2]
        print("AUTO LOGIN(automatically logs in the next time you use the program)")
        autolog = input("DO YOU WANT TO ENABLE AUTO LOG IN (Y/N)?:")
        if autolog.upper() == "Y":
            mycmd = "INSERT INTO AUTOLOGIN VALUES('{}','{}',{})".format(username,password,userid)
            cursorobject.execute(mycmd)
            mydb.commit()
        return username,password,userid
    if verification == False:
        print("INCORRECT USERNAME OR PASSWORD")
        print("PRESS 1 to try to log in again")
        print("PRESS 2 to register")
        print("PRESS 3 to exit")
        choice1 = int(input("Enter your choice:"))
    if choice1 == 1 :
        login()
    elif choice1 == 2 :
        username,password,userid=register()
        return username,password,userid
    elif choice1 == 3 :
       quit()
def register():
    username = input("Enter your username:")
    time.sleep(1)
    password = input("Enter your password(max 10 characters):")
    time.sleep(1)
    passwordcheck = input("Enter your password again:")
    if password == passwordcheck and len(password)<11:
        pass
    else:
        time.sleep(1)
        print("PASSWORDS DO NOT MATCH")
        print("PLEASE ENTER SAME PASSWORD TWICE")
        register()
    print("NOW PLEASE ENTER YOUR DETAILS")
    dob = input("Enter your date of birth(YYYY-MM-DD):")
    age = date.year-int(dob[:4])
    if age<18:
        print("YOU MUST BE ATLEAST 18 TO BE ELIGIBLE TO HAVE AN ACCOUNT")
        return "failure"
    elif age>18:
        pass
    email = input("Enter you email:")
    condition = True
    while condition == True:
     try:
        condition = False
        emailverification = validate_email(email)
        email = emailverification.email
        break
     except EmailNotValidError as errormsg:
        print(str(errormsg))
        print("please enter an proper email")
        condition = True
     email = input("Enter a valid email:")
    phoneno = int(input("Enter your phone no:"))
    while len(str(phoneno)) != 10:
        print("Enter a valid mobile number")
        phoneno = int(input("Enter your valid phone no:"))
    userid = random.randint(100,999)
    mycmd1 = "select userid from userinfo"
    cursorobject.execute(mycmd1)
    data = cursorobject.fetchall()
    l=[]
    for i in data:
      l.append(i[0])
    while userid in l:
      userid=random.randint(100,999)
    mycmd = "INSERT INTO login VALUES('{}','{}',{})".format(username,password,userid)
    cursorobject.execute(mycmd)
    mydb.commit()
    mycmd2 = "insert into userinfo values({},'{}','{}','{}','{}',{})".format(userid,username,password,dob,email,phoneno)
    cursorobject.execute(mycmd2)
    mydb.commit()
    return username,password,userid
def search():
    destination=input("Enter your destination:")
    departure=input("Enter your departure place:")
    cmd1="select* from trains"
    cursorobject.execute(cmd1)
    data=cursorobject.fetchall()
    data4=[["Trainid","Train name","Type","departure","Destination","Arrival","Halt time","Departs","Platform","Seats","Destination time"]]
    for i in data:
        trainname=i[1]
        cmd2="select tablename from traintablename where trainname='{}'".format(trainname)
        cursorobject.execute(cmd2)
        data1=cursorobject.fetchall()
        table=data1[0][0]
        cmd3="select* from "+table+"" 
        cursorobject.execute(cmd3)
        data2=cursorobject.fetchall()
        data3=[]
        for j in data2:
            data3.append(j[0])
        if destination in data3 and departure in data3:
           data5=data2[data3.index(departure)]
           data4.append([i[0],i[1],i[2],departure,destination,data5[1],data5[2],data5[3],data5[4],data5[5],data2[data3.index(destination)][1]])
    z=0
    print("   ",data4[0])
    for k in data4[1::]:
           z+=1
           print(z,")",k)
    choice1=int(input("ENTER YOUR CHOICE1:"))
    return choice1,data4
def trainbook():
    choice1,data=search()
    data1=data[choice1]
    print(data1)
    print("PRESS 1 to show trains timetable")
    print("PRESS 2 to book tickets")
    print("PRESS 3 to go to menu")
    print("PRESS 4 to quit")
    choice2=int(input("Enter your choice:"))
    mycmd2="SELECT TABLENAME FROM TRAINTABLENAME WHERE TRAINNAME = '{}'".format(data1[1])
    cursorobject.execute(mycmd2)
    data2=cursorobject.fetchall()
    table=data2[0][0]
    mycmd3="SELECT * FROM "+table+""
    cursorobject.execute(mycmd3)
    data3=cursorobject.fetchall()
    if choice2 == 1:
        print("****TIMETABLE FOR",data1[1],"****")
        print("STATION       ARRIVES    HALTTIME       DEPARTS    PLATFORM    SEATS")
        for i in data3:
            print(i)
        print("PRESS 1 to show trains timetable")
        print("PRESS 2 to book tickets")
        print("PRESS 3 to go to menu")
        print("PRESS 4 to quit")
        choice2=int(input("Enter your choice:"))
    if choice2 == 1:
        print("****TIMETABLE FOR",data1[1],"****")
        print("STATION       ARRIVES    HALTTIME       DEPARTS    PLATFORM    SEATS")
        for i in data3:
            print(i)
        print(data1)
    elif choice2 == 2 :
        print("BOOK TICKETS FOR",data1[1])
        no_of_tickets=int(input("Enter how many tickets to book:"))
        if data1[9] > no_of_tickets:
            print("Are you confirm to book",no_of_tickets," tickets for the following train",data1[1])
            ticket_confirm=input("ENTER (y/n)")
            date1=input("Enter the date for the train (YYYY-MM-DD):")
            if ticket_confirm.lower() == "y":
                l=[]
                cond=False
                for i in data3:
                    if i[0] == data1[3]:
                        cond = True
                    elif i[0] == data1[4]:
                        cond = False
                        break
                    if cond == True :
                        l.append(i[0])
                for i in l:
                   mycmd4="UPDATE "+table+" SET SEATS = SEATS-{} WHERE STATION ='{}'".format(no_of_tickets,i)
                   cursorobject.execute(mycmd4)
                   mydb.commit()
                lst=[]
                ticketid=random.randint(1100,1200)
                mycmd5="SELECT TICKETID FROM TICKETBOOKED"
                cursorobject.execute(mycmd5)
                data4=cursorobject.fetchall()
                for i in data4:
                    lst.append(i[0])
                count=len(lst)
                while len(lst) != no_of_tickets+count:
                    ticketid=random.randint(1100,1200)
                    if ticketid not in lst:
                        lst.append(ticketid)
                for i in lst[count::]:
                   mycmd4="INSERT INTO TICKETBOOKED VALUES({},{},'{}','{}','{}','{}',{})".format(i,data1[0],data1[1],data1[3],data1[4],date1,userid)
                   cursorobject.execute(mycmd4)
                   mydb.commit()
                print("TICKETS HAVE BEEN BOOKED")
                print("***RETURNING TO MENU***")
                menu()
            elif ticket_confirm.lower() == "n":
                print("TICKETS NOT BOOKED")
                print("***RETURNING TO MENU***")
                menu()
        elif choice2 == 3 :
            menu()
        elif choice2 == 4 :
            quit()
def cancel():
    data=viewtickets()
    lst=eval(input("Enter the list of tickets to be canceled ([1,2,3]):"))
    lst1=[]
    for i in lst:
       if str(data[i-1][5]) > str(date):
           data1=data[i-1]
           mycmd2="DELETE FROM TICKETBOOKED WHERE TICKETID = {}".format(data1[0])
           cursorobject.execute(mycmd2)
           mydb.commit()
       else:
            lst1.append(lst)
    if lst1 == [] :
        print("The selected tickets are cancelled")
    else:
        print("*******************************************************")
        for j in lst:
          print(data[j-1])
        print("The above tickets cannot be cancelled since its way past cancel time")
        print("(Ticket cannot be cancelled on the day of boarding")
    menu()
def viewtickets():
    print("***TICKETS***")
    mycmd2="SELECT * FROM TICKETBOOKED where userid = {}".format(userid)
    cursorobject.execute(mycmd2)
    data=cursorobject.fetchall()
    x=0
    if len(data) != 0 :
      print("  TICKETID,TRAINID,  TRAINNAME  ,   DEPATURE  ,    DESTINATION    ,    DATE    ")
      for i in data:
         x+=1
         print(x,")",i[0:5]+(str(i[5]),))
    else:
        print("NO TICKETS HAD BEEN BOOKED")
    return data
def profile():
    global username
    global password
    while True :
      print("*****PROFILE*****")
      print("PRESS 1 to view profile")
      print("PRESS 2 to view past travels")
      print("PRESS 3 to edit your profile")
      print("PRESS 4 to return to menu")
      choice1=int(input("Enter your choice:"))
      if choice1 == 1 :
        cmd1="SELECT * FROM USERINFO WHERE USERNAME = '{}'".format(username)
        cursorobject.execute(cmd1)
        data=cursorobject.fetchall()
        print("USERID  USERNAME    DOB           EMAIL                   PHONENO    ")
        print(" ",data[0][0],"  ",data[0][1],"  ",data[0][3]," ",data[0][4]," ",data[0][5]," ")
        profile()
      elif choice1 == 2 :
        mycmd2="SELECT * FROM TICKETBOOKED where userid = {}".format(userid)
        cursorobject.execute(mycmd2)
        data1=cursorobject.fetchall()
        if len(data1) != 0:
            for j in data1:
                print(j)
        else:
            print("NO PAST TRAVELS TO SHOW")
      elif choice1 == 3 :
        print("***EDIT PROFILE***")
        cmd1="SELECT * FROM USERINFO WHERE USERNAME = '{}'".format(username)
        cursorobject.execute(cmd1)
        data=cursorobject.fetchall()
        print("USERID  USERNAME    DOB           EMAIL                   PHONENO    ")
        print(" ",data[0][0],"  ",data[0][1],"  ",data[0][3]," ",data[0][4]," ",data[0][5]," ")
        print("What do u want to edit?")
        print("ENTER 1 to edit username")
        print("ENTER 2 to edit password")
        print("Enter 3 to edit DOB")
        print("ENTER 4 to edit email")
        print("ENTER 5 to edit phoneno")
        print("ENTER 6 TO RETURN TO PROFILe")
        choice2=int(input("ENTER YOUR CHOICE:"))
        if choice2 == 1 :
            username=input("Enter your new username:")
            cmd2="UPDATE USERINFO SET USERNAME = '{}' WHERE USERID = {}".format(username,data[0][0])
            cmd5="UPDATE LOGIN SET USERNAME = '{}' WHERE USERID = {}".format(username,data[0][0])
            cmd6="UPDATE AUTOLOGIN SET USERNAME = '{}' WHERE USERID = {}".format(username,data[0][0])
            cursorobject.execute(cmd2)
            mydb.commit()
            cursorobject.execute(cmd5)
            mydb.commit()
            cursorobject.execute(cmd6)
            mydb.commit()
            print("USERNAME SUCCESSFULLY UPDATED TO",username)
        elif choice2 == 2 :
            passwordold=input("ENTER YOUR OLD PASSWORD:")
            if password == passwordold:
                passwordnew = input("ENTER YOUR NEW PASSWORD:")
                passwordnew1 = input("ENTER YOUR NEW PASSWORD AGAIN:")
                if passwordnew == passwordnew1:
                    cmd2 = "UPDATE USERINFO SET PASSWORD ='{}' WHERE USERID = {}".format(passwordnew1,data[0][0])
                    cursorobject.execute(cmd2)
                    mydb.commit()
                    cmd3="UPDATE LOGIN SET PASSWORD = '{}' WHERE USERID = '{}'".format(passwordnew1,data[0][0])
                    cmd4="UPDATE AUTOLOGIN SET PASSWORD = '{}' WHERE USERID = '{}'".format(passwordnew1,data[0][0])
                    cursorobject.execute(cmd3)
                    mydb.commit()
                    cursorobject.execute(cmd4)
                    mydb.commit()
                    print("PASSWORD UPDATED SUCCESSFULLY")
                    password = passwordnew1
                else:
                    print("passwords do not match")
                    print("password updation failed")
            else:
                print("incorrect password")
                print("PASSWORD updation failed")
            profile()
        elif choice2 == 3 :
            dob=input("ENTER YOUR DATEOFBIRTH IN (YYYY-MM-DD) FORMAT:")
            cmd2 = "UPDATE USERINFO SET DOB = '{}' WHERE USERID = {}".format(dob,data[0][0])
            cursorobject.execute(cmd2)
            mydb.commit()
            print("DOB SUCCESSFULLY UPDATED TO",dob)
        elif choice2 == 4 :
            email = input("ENTER YOUR NEW EMAIL:")
            n=0
            try:
                emailverification = validate_email(email)
                email = emailverification.email
                n=0
            except EmailNotValidError as errormsg:
                print(str(errormsg))
                print("NOT A VALID EMAIL")
                print("email updation has failed")
                n=1
            if n == 0 :
                cmd2 = "UPDATE USERINFO SET EMAIL = '{}' WHERE USERID = {}".format(email,data[0][0])
                cursorobject.execute(cmd2)
                mydb.commit()
        elif choice2 == 5 :
            phoneno=int(input("ENTER YOUR NEW PHONENO:"))
            if len(str(phoneno)) != 10:
                print("INVALID PHONENO")
                print("PHONENO UPDATION HAS FAILED")
            else:
                cmd2="UPDATE USERINFO SET PHONENO = {} WHERE USERID = {}".format(phoneno,data[0][0])
                cursorobject.execute(cmd2)
                mydb.commit()
                print("PHONENO UPDATED SUCCESSFULLY")
        elif choice1 == 6 :
            profile()
      elif choice1 == 4:
          menu()
def logout():
    cmd1="DELETE FROM AUTOLOGIN"
    cursorobject.execute(cmd1)
    mydb.commit()
    print("Log Out successful")
    print("Terminating the program")
    quit()
def menu():
    print("****menu****")
    print("PRESS 1 TO book a rain")
    print("PRESS 2 to cancel ticket")
    print("PRESS 3 to view your tickets")
    print("PRESS 4 profile")
    print("PRESS 5 to log out")
    print("PRESS 6 to quit")
    choice1 = int(input("Enter your choice:"))
    if choice1 == 1 :
        trainbook()
    elif choice1 == 2 :
        cancel()
    elif choice1 == 3 :
        viewtickets()
        menu()
    elif choice1 == 4 :
        profile()
    elif choice1 == 5 :
        logout()
    elif choice1 == 6 :
        print("***program terminated***")
        quit()
print("wellcome")
mycmd1 = "SELECT* FROM AUTOLOGIN"
cursorobject.execute(mycmd1)
autolog = cursorobject.fetchall()
logged = False
if autolog != [] :
    username = autolog[0][0]
    password = autolog[0][1]
    userid = autolog[0][2]
    logged = True
elif autolog == [] :
    print("Do you want to log in or register?:")
    print("ENTER 1 TO LOGIN")
    print("ENTER 2 TO REGISTER")
    print("ENTER 3 TO QUIT")
    choice = int(input("Enter your choice:"))
    if choice == 1 :
       username,password,userid=login()
       logged = True
    elif choice == 2 :
       username,password,userid=register()
       logged = True
    elif choice == 3 :
        print("***program terminated***")
        quit()
if logged == True :
    menu()
mydb.close()
