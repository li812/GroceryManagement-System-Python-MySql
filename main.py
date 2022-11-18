import math
import json
import os
from queue import Empty
import random
from datetime import datetime
from datetime import date
from os.path import exists
import mysql.connector
import matplotlib.pyplot as plt
import random
from tabulate import tabulate
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

############### MySql table Creation #####################

mydb=mysql.connector.connect(host ="localhost",user="root",password="")
mycursor=mydb.cursor()
mycursor.execute("create database if not exists gms")
mycursor.execute("use gms")
mycursor.execute("create table if not exists usertype(type_id INT NOT NULL AUTO_INCREMENT, type VARCHAR(10) NOT NULL , PRIMARY KEY (type_id))")
mycursor.execute("INSERT IGNORE INTO usertype(type_id, type) VALUES ('1', 'admin'), ('2', 'manager'), ('3', 'staff')")
mycursor.execute("create table if not exists login(login_id INT NOT NULL AUTO_INCREMENT, type_id INT NOT NULL , username VARCHAR(20) NOT NULL , password VARCHAR(20) NOT NULL , PRIMARY KEY (login_id), FOREIGN KEY (type_id) REFERENCES usertype(type_id))")
mycursor.execute("INSERT IGNORE INTO login(login_id, type_id, username, password) VALUES ('1', '1', 'admin', 'admin')")
mycursor.execute("create table if not exists manager(m_id INT NOT NULL AUTO_INCREMENT, login_id INT NOT NULL , f_name VARCHAR(50) NOT NULL , l_name VARCHAR(50) NOT NULL , email VARCHAR(50) NOT NULL ,phone_no VARCHAR(50) NOT NULL , address VARCHAR(150) NOT NULL ,city VARCHAR(50) NOT NULL, salary int, date varchar(50), PRIMARY KEY (m_id), FOREIGN KEY (login_id) REFERENCES login(login_id))")
mycursor.execute("create table if not exists staff(staff_id INT NOT NULL AUTO_INCREMENT, login_id INT NOT NULL , f_name VARCHAR(50) NOT NULL , l_name VARCHAR(50) NOT NULL , email VARCHAR(50) NOT NULL ,phone_no VARCHAR(50) NOT NULL , address VARCHAR(150) NOT NULL ,city VARCHAR(50) NOT NULL, salary int, date varchar(50), PRIMARY KEY (staff_id), FOREIGN KEY (login_id) REFERENCES login(login_id))")
mycursor.execute("create table if not exists suspended(s_id INT NOT NULL AUTO_INCREMENT, login_id INT NOT NULL, date varchar(12), PRIMARY KEY (s_id), FOREIGN KEY (login_id) REFERENCES login(login_id))")
mycursor.execute("create table if not exists catagory(c_id INT NOT NULL AUTO_INCREMENT, c_name VARCHAR(200), PRIMARY KEY (c_id), unique (c_name))")
mycursor.execute("create table if not exists items(item_id INT NOT NULL AUTO_INCREMENT, c_id int not null, item_name VARCHAR(200) NOT NULL, item_quantity int NOT NULL, item_price int NOT NULL , PRIMARY KEY (item_id), unique (item_name), FOREIGN KEY (c_id) REFERENCES catagory(c_id))")
mycursor.execute("create table if not exists customer(cus_id INT NOT NULL AUTO_INCREMENT, cus_name VARCHAR(200) NOT NULL, phone_no varchar(20) NOT NULL, city varchar(200) , date varchar(50) not null, PRIMARY KEY (cus_id), unique (phone_no))")
mydb.commit()

today = date.today()
stoday = str(today)


now = datetime.now()
current_time = now.strftime("%H:%M:%S")
stime=str(current_time)


def system_init():
    print("  ╭────────────────────────────────────────────────────────────────────────────────╮")
    print("  │                                                                                │")
    print("  │                                                                                │")
    print("  │                                                            @@@@@@@@@@@@        │")
    print("  │                                                           @@@@                 │  ╭─────────────────────────╮")
    print("  │                 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                  │  │Today's date:", stoday,"│")
    print("  │                .@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                   │  │Current Time:", stime,"  │")
    print("  │                 @@@@      @@@@      @@@@      @@@&      @@@@                   │  ╰─────────────────────────╯")
    print("  │                  @@@.      @@@      @@@@      @@@       @@@                    │  ╭───────────────────────╮")
    print("  │                  @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@(                    │  │ ▶︎ 1 • Login           │")
    print("  │                   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                     │  ├───────────────────────┤")
    print("  │                   @@@@     %@@@     @@@@     @@@      @@@                      │  │ ▶︎ 2 • Exit System     │")
    print("  │                    @@@@     @@@     @@@@    &@@@     @@@@                      │  ╰───────────────────────╯")
    print("  │                     @@@     @@@@    @@@@    @@@@     @@@                       │")
    print("  │                     @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                        │")
    print("  │                                                    @@@@                        │")
    print("  │                                                    @@@                         │")
    print("  │                      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%                         │")
    print("  │                       ... @@@................. @@@..                           │")
    print("  │                         @@@@@@@              @@@@@@@                           │")
    print("  │                          @@@@@                @@@@@                            │")
    print("  │                                                                                │")
    print("  │                                                                                │")
    print("  │                          Grocery  Management System                            │")
    print("  │                                                                                │")
    print("  ╰────────────────────────────────────────────────────────────────────────────────╯")

    user_choice = input("\n  ☞ Enter your command: ")

    try:
        user_choice=int(user_choice)

    except:
        pass



    if user_choice == 1:
        def login():
            username=input("▶︎ Username :")
            mycursor.execute("select username from login where username='"+username+"'")
            usn=mycursor.fetchone()
            if usn is not None:
                print("╭───────────────────────╮")
                print("│   VALID USERNAME..!   │")
                print("╰───────────────────────╯")
            elif usn is None:
                print("╭───────────────────────╮")
                print("│  INVALID USERNAME..!  │")
                print("╰───────────────────────╯")
                system_init()
            mycursor.execute("select login_id from login where username='"+username+"'")
            lix=mycursor.fetchone()
            li = str(lix[0])
            mycursor.execute("select s_id from suspended where login_id='"+li+"'")
            st=mycursor.fetchone()
            if st is not None:
                print("\nYour account has been freezed please contact bank for more information.\n")
                system_init()
            pwi=input("▶︎ Password :")
            mycursor.execute("select password from login where username='"+username+"'")
            pws=mycursor.fetchone()
            password=str(pws[0])
            if password==pwi:
                mycursor.execute("select type_id from login where password='"+pwi+"'")
                type=mycursor.fetchone()
                usertype = type[0]

################################################################################################

###########################################
###########################################
########### Functions of admin ###########

                def create_manager():
                    f_name = input("First Name :")
                    l_name =  input("Last Name :")
                    email = input("Email :")
                    username = input("Username :")
                    password= input("Password :")
                    phone_no = input("Phone Number :")
                    address = input("Address :")
                    city = input("City :")
                    today = date.today()
                    stoday= str(today)
                    salary = input("Salary :")
                    try:
                        mycursor.execute("insert into login(type_id,username,password) values('2','"+username+"','"+password+"')")
                        mydb.commit()
                        getid1="SELECT login_id FROM login WHERE username='"
                        getid2="';"
                        get_login_id = getid1+username+getid2
                        mycursor.execute(get_login_id)
                        data = mycursor.fetchone()
                        login_id = str(data[0])
                        sql = "INSERT INTO manager (login_id,f_name,l_name,email,phone_no,address,city,salary,date) VALUES (%s, %s, %s,%s, %s,%s, %s,%s,%s)"
                        val = (login_id,f_name,l_name,email,phone_no,address,city,salary,stoday)
                        try:
                            mycursor.execute(sql,val)
                            mydb.commit() 
                            print("╭──────────────────────────────────────╮")
                            print("│  Manager account created succesfully │")
                            print("╰──────────────────────────────────────╯")
                            admin()
                        except:
                            print("╭───────────────────────╮")
                            print("│  Something went wrong │")
                            print("╰───────────────────────╯")
                            admin()

                    except:
                        print("╭───────────────────────╮")
                        print("│  Something went wrong │")
                        print("╰───────────────────────╯")
                        admin()


                def manage_manager():
                    def show_manager():
                        mycursor.execute("SELECT m_id,f_name,l_name,phone_no,salary FROM manager;")
                        data = mycursor.fetchall()
                        h = ['Manager ID','First Name','Last Name','Phone Number','Salary']
                        print(tabulate(data,headers=h,tablefmt='psql'))
                        manage_manager()

                    def delete_manager():
                        mycursor.execute("SELECT m_id,f_name,l_name,phone_no,salary FROM manager;")
                        data = mycursor.fetchall()
                        h = ['Manager ID','First Name','Last Name','Phone Number','Salary']
                        print(tabulate(data,headers=h,tablefmt='psql'))
                        kill = input("Enter the Manager ID: ")
                        try:                                           
                            mycursor.execute("select login_id from manager where m_id='"+kill+"'")
                            data = mycursor.fetchone()
                            kill_id = str(data[0])
                            mycursor.execute("delete from manager where m_id='"+kill+"'")
                            mydb.commit()
                            mycursor.execute("delete from login where login_id='"+kill_id+"'")
                            mydb.commit()
                            print("╭──────────────────────────────────────────╮")
                            print("│   Manager account deleted successfully!  │")
                            print("╰──────────────────────────────────────────╯")                           
                            print("\n")
                        except TypeError:
                            print("╭──────────────────────────────────╮")
                            print("│ Please enter a valid Manager ID! │")
                            print("╰──────────────────────────────────╯")
                            manage_manager()

                        mycursor.execute("SELECT m_id,f_name,l_name,phone_no,salary FROM manager;")
                        data = mycursor.fetchall()
                        h = ['Manager ID','First Name','Last Name','Phone Number','Salary']
                        print(tabulate(data,headers=h,tablefmt='psql'))
                        manage_manager()

                    print("╭───────────────────────────────╮")
                    print("│ Welcome to Manager Management │")
                    print("╰───────────────────────────────╯")
                    print("╭──────────────────────────────────────╮")
                    print("│ ▶︎ 1 • Show Managers                  │")
                    print("├──────────────────────────────────────┤")
                    print("│ ▶︎ 2 • Delete Managers                │")
                    print("├──────────────────────────────────────┤")
                    print("│ ▶︎ 3 • Go Back                        │")
                    print("├──────────────────────────────────────┤")
                    print("│ ▶︎ 4 • Exit System                    │")
                    print("╰──────────────────────────────────────╯")

                    ach = input("\n  ☞ Enter your command: ")
                    try:
                        ach=int(ach)
                    except:
                        print("╭───────────────────────────────────╮")
                        print("│     Please enter valid command    │")
                        print("╰───────────────────────────────────╯")                                
                        admin()

                    if ach == 1:
                        show_manager()

                    if ach == 2:
                        delete_manager()
                    
                    
                    if ach == 3:
                        admin()

                    if ach == 4:
                        print("╭───────────────────────╮")
                        print("│    Exiting System..   │")
                        print("╰───────────────────────╯\n")
                        quit()

                    else:
                        print("╭───────────────────────────────────╮")
                        print("│     Please enter valid command    │")
                        print("╰───────────────────────────────────╯")
                        admin()
                    admin() 
                        
                def csv_manager():
                        sq="SELECT * FROM manager"                       
                        sql_query = pd.read_sql_query(sq,mydb)
                        df = pd.DataFrame(sql_query)
                        filenm=input("Enter file name:")
                        csvfile = filenm+".csv"
                        df.to_csv (csvfile, index = False)
                        admin()

####### End of Functions of admin #########
###########################################
###########################################

################################################################################################  

                if usertype == 1:
                    def admin():
                        print("╭───────────────────────╮")
                        print("│     Welcome Admin     │")
                        print("╰───────────────────────╯")
                        print("╭───────────────────────────────────────────╮")
                        print("│ ▶︎ 1 • Create new manager account          │")
                        print("├───────────────────────────────────────────┤")
                        print("│ ▶︎ 2 • Manage Managers                     │")
                        print("├───────────────────────────────────────────┤")
                        print("│ ▶︎ 3 • Export manager details toi csv      │")
                        print("├───────────────────────────────────────────┤")
                        print("│ ▶︎ 4 • Logout                              │")
                        print("├───────────────────────────────────────────┤")
                        print("│ ▶︎ 5 • Exit System                         │")
                        print("╰───────────────────────────────────────────╯")
                        ach = input("\n  ☞ Enter your command: ")
                        try:
                            ach=int(ach)
                        except:
                            print("╭───────────────────────────────────╮")
                            print("│     Please enter valid command    │")
                            print("╰───────────────────────────────────╯")                                
                            admin()

                        if ach == 1:
                            create_manager()

                        if ach == 2:
                            manage_manager()

                        if ach == 3:
                            csv_manager()
                        
                        
                        if ach == 4:
                            print("╭───────────────────────╮")
                            print("│     Signing out..     │")
                            print("╰───────────────────────╯\n")
                            login()

                        if ach == 5:
                            print("╭───────────────────────╮")
                            print("│    Exiting System..   │")
                            print("╰───────────────────────╯\n")
                            quit()

                        else:
                            print("╭───────────────────────────────────╮")
                            print("│     Please enter valid command    │")
                            print("╰───────────────────────────────────╯")
                            admin()

                    admin()


################################################################################################

###########################################
###########################################
########### Functions of Manager ###########

                def create_staff():
                    f_name = input("First Name :")
                    l_name =  input("Last Name :")
                    email = input("Email :")
                    username = input("Username :")
                    password= input("Password :")
                    phone_no = input("Phone Number :")
                    address = input("Address :")
                    city = input("City :")
                    today = date.today()
                    stoday= str(today)
                    salary = input("Salary :")
                    try:
                        mycursor.execute("insert into login(type_id,username,password) values('3','"+username+"','"+password+"')")
                        mydb.commit()
                        getid1="SELECT login_id FROM login WHERE username='"
                        getid2="';"
                        get_login_id = getid1+username+getid2
                        mycursor.execute(get_login_id)
                        data = mycursor.fetchone()
                        login_id = str(data[0])
                        sql = "INSERT INTO staff (login_id,f_name,l_name,email,phone_no,address,city,salary,date) VALUES (%s, %s, %s,%s, %s,%s, %s,%s,%s)"
                        val = (login_id,f_name,l_name,email,phone_no,address,city,salary,stoday)
                        try:
                            mycursor.execute(sql,val)
                            mydb.commit() 
                            print("╭────────────────────────────────────╮")
                            print("│  Staff account created succesfully │")
                            print("╰────────────────────────────────────╯")
                            manager()
                        except:
                            print("╭───────────────────────╮")
                            print("│  Something went wrong │")
                            print("╰───────────────────────╯")
                            manager()

                    except:
                        print("╭───────────────────────╮")
                        print("│  Something went wrong │")
                        print("╰───────────────────────╯")
                        manager()


                def manage_staff():
                    def show_staff():
                        mycursor.execute("SELECT staff_id,f_name,l_name,phone_no,salary,date FROM staff;")
                        data = mycursor.fetchall()
                        h = ['Staff ID','First Name','Last Name','Phone Number','Salary','Date']
                        print(tabulate(data,headers=h,tablefmt='psql'))
                        manage_staff()

                    def delete_staff():
                        mycursor.execute("SELECT staff_id,f_name,l_name,phone_no,salary FROM staff;")
                        data = mycursor.fetchall()
                        h = ['Staff ID','First Name','Last Name','Phone Number','Salary']
                        print(tabulate(data,headers=h,tablefmt='psql'))
                        kill = input("Enter the Staff ID: ")
                        try:                                           
                            mycursor.execute("select login_id from staff where staff_id='"+kill+"'")
                            data = mycursor.fetchone()
                            kill_id = str(data[0])
                            mycursor.execute("delete from staff where staff_id='"+kill+"'")
                            mydb.commit()
                            mycursor.execute("delete from login where login_id='"+kill_id+"'")
                            mydb.commit()
                            print("╭──────────────────────────────────────────╮")
                            print("│    Staff account deleted successfully!   │")
                            print("╰──────────────────────────────────────────╯")                           
                            print("\n")
                        except TypeError:
                            print("╭──────────────────────────────────╮")
                            print("│ Please enter a valid Staff ID!   │")
                            print("╰──────────────────────────────────╯")
                            manage_staff()

                        mycursor.execute("SELECT staff_id,f_name,l_name,phone_no,salary,date FROM staff;")
                        data = mycursor.fetchall()
                        h = ['Staff ID','First Name','Last Name','Phone Number','Salary','Date']
                        print(tabulate(data,headers=h,tablefmt='psql'))
                        manage_staff()

                    def csv_staff():
                        sq="SELECT * FROM staff"                       
                        sql_query = pd.read_sql_query(sq,mydb)
                        df = pd.DataFrame(sql_query)
                        filenm=input("Enter file name:")
                        csvfile = filenm+".csv"
                        df.to_csv (csvfile, index = False)
                        manage_staff()

                    print("╭───────────────────────────────╮")
                    print("│  Welcome to Staff Management  │")
                    print("╰───────────────────────────────╯")
                    print("╭───────────────────────────────────────────╮")
                    print("│ ▶︎ 1 • Show Staffs                         │")
                    print("├───────────────────────────────────────────┤")
                    print("│ ▶︎ 2 • Delete Staffs                       │")
                    print("├───────────────────────────────────────────┤")
                    print("│ ▶︎ 3 • Export staff details to CSV file    │")
                    print("├───────────────────────────────────────────┤")
                    print("│ ▶︎ 4 • Go Back                             │")
                    print("├───────────────────────────────────────────┤")
                    print("│ ▶︎ 5 • Exit System                         │")
                    print("╰───────────────────────────────────────────╯")

                    ach = input("\n  ☞ Enter your command: ")
                    try:
                        ach=int(ach)
                    except:
                        print("╭───────────────────────────────────╮")
                        print("│     Please enter valid command    │")
                        print("╰───────────────────────────────────╯")                                
                        manager()

                    if ach == 1:
                        show_staff()

                    if ach == 2:
                        delete_staff()

                    if ach == 3:
                        csv_staff()
                    
                    if ach == 4:
                        manager()

                    if ach == 5:
                        print("╭───────────────────────╮")
                        print("│    Exiting System..   │")
                        print("╰───────────────────────╯\n")
                        quit()

                    else:
                        print("╭───────────────────────────────────╮")
                        print("│     Please enter valid command    │")
                        print("╰───────────────────────────────────╯")
                        manager()
                    manager() 
 
                def manage_catagory():
                    def create_catagory():
                        mycursor.execute("SELECT c_id,c_name FROM catagory;")
                        data = mycursor.fetchall()
                        h = ['Catagory ID','Catagory Name']
                        print(tabulate(data,headers=h,tablefmt='psql'))

                        c_name = input("\n  ☞ Enter catagory name: ")
                        try:
                            mycursor.execute("insert into catagory (c_name) values ('"+c_name+"')")
                            mydb.commit()
                            print("╭──────────────────────────────────────────╮")
                            print("│      Catagory created successfully       │")
                            print("╰──────────────────────────────────────────╯") 
                            manage_catagory()
                        except:
                            print("╭────────────────────────────────────────╮")
                            print("│         Catagory already exists        │")
                            print("╰────────────────────────────────────────╯")     
                            manage_catagory()                      

                    def show_catagory():
                        mycursor.execute("SELECT c_id,c_name FROM catagory;")
                        data = mycursor.fetchall()
                        h = ['Catagory ID','Catagory Name']
                        print(tabulate(data,headers=h,tablefmt='psql'))
                        manage_catagory()

                    def del_catagory():
                        mycursor.execute("SELECT c_id,c_name FROM catagory;")
                        data = mycursor.fetchall()
                        h = ['Catagory ID','Catagory Name']
                        print(tabulate(data,headers=h,tablefmt='psql'))
                        kill = input("Enter the Catagory ID: ")
                        killi=int(kill)

                        mycursor.execute("SELECT c_id FROM catagory;")
                        d_id = mycursor.fetchall()

                        tr = 0
                        for i in d_id:
                            for j in i:
                                if j == killi:
                                    tr=tr+1
                         
                        if tr == 1:                                                     
                            mycursor.execute("delete from catagory where c_id='"+kill+"'")
                            mydb.commit()
                            print("╭──────────────────────────────────────────╮")
                            print("│      Catagory deleted successfully!      │")
                            print("╰──────────────────────────────────────────╯")                           
                            print("\n")
                            
                        else:
                            print("╭───────────────────────────────────────╮")
                            print("│   Please enter a valid Catagory ID!   │")
                            print("╰───────────────────────────────────────╯")
                            manage_catagory()


                        manage_catagory()

                    def pie_catagory():
                        catagory_name=[]
                        mycursor.execute("SELECT c_name FROM catagory")
                        myresult = mycursor.fetchall()
                        for x in myresult:
                            cx = x[0]
                            catagory_name.append(cx)


                        #get number of catagories
                        noc=0
                        mycursor.execute("SELECT * FROM catagory")
                        myresult = mycursor.fetchall()
                        for x in myresult:
                            noc = noc + 1

                        #get catagory_id
                        c_id = []
                        mycursor.execute("SELECT c_id FROM catagory")
                        myresult = mycursor.fetchall()
                        for x in myresult:
                            c_idx = x[0]
                            c_id.append(c_idx)

                        #get catagory strength
                        c_strength = []

                        for i in c_id:
                            sn = 0
                            i = str(i)
                            mycursor.execute("SELECT * FROM items where c_id ='"+i+"'")
                            myresult = mycursor.fetchall()
                            for x in myresult:
                                sn = sn + 1
                            c_strength.append(sn)

                        colors=['red','yellowgreen','blue','gold','green']
                        plt.pie(c_strength,labels=catagory_name,colors=colors)
                        plt.title('avalibility of items in shop')
                        plt.show()                          

                    def csv_catagory():
                        sq="SELECT * FROM catagory"                       
                        sql_query = pd.read_sql_query(sq,mydb)
                        df = pd.DataFrame(sql_query)
                        filenm=input("Enter file name:")
                        csvfile = filenm+".csv"
                        df.to_csv (csvfile, index = False)
                        manage_catagory()


                    print("╭────────────────────────────────────────╮")
                    print("│     Welcome to Catagory management     │")
                    print("╰────────────────────────────────────────╯")
                    print("╭─────────────────────────────────────────────╮")
                    print("│ ▶︎ 1 • Create new Catagory                   │")
                    print("├─────────────────────────────────────────────┤")
                    print("│ ▶︎ 2 • Show current catagories               │")
                    print("├─────────────────────────────────────────────┤")
                    print("│ ▶︎ 3 • Delete an existing catogory           │")
                    print("├─────────────────────────────────────────────┤")
                    print("│ ▶︎ 4 • Generate pie chart                    │")
                    print("├─────────────────────────────────────────────┤")
                    print("│ ▶︎ 5 • Generate CSV file of catagory list    │")
                    print("├─────────────────────────────────────────────┤")
                    print("│ ▶︎ 6 • Go Back                               │")
                    print("├─────────────────────────────────────────────┤")
                    print("│ ▶︎ 7 • Exit System                           │")
                    print("╰─────────────────────────────────────────────╯")

                    ach = input("\n  ☞ Enter your command: ")
                    try:
                        ach=int(ach)
                    except:
                        print("╭───────────────────────────────────╮")
                        print("│     Please enter valid command    │")
                        print("╰───────────────────────────────────╯")                                
                        manage_catagory()

                    if ach == 1:
                        create_catagory()

                    if ach == 2:
                        show_catagory()
                    
                    
                    if ach == 3:
                        del_catagory()

                    if ach == 4:
                        pie_catagory()


                    if ach == 5:
                        csv_catagory()


                    if ach == 6:
                        manager()

                    if ach == 7:
                        print("╭───────────────────────╮")
                        print("│    Exiting System..   │")
                        print("╰───────────────────────╯\n")
                        quit()


                    else:
                        print("╭───────────────────────────────────╮")
                        print("│     Please enter valid command    │")
                        print("╰───────────────────────────────────╯")
                        manager()
                    manager() 

                
                def manage_stock():
                    
                    def add_stock():
                        mycursor.execute("SELECT * FROM items;")
                        data = mycursor.fetchall()
                        h = ['Item ID','Catagory ID','Item Name','Item Quantity','Item Price']
                        print(tabulate(data,headers=h,tablefmt='psql'))

                        c_id = input("\n  ☞ Enter catagory id: ")
                        item_name = input("\n  ☞ Enter item name: ")
                        item_quantity = input("\n  ☞ Enter item quantity: ")
                        item_price = input("\n  ☞ Enter item price: ")
                        sql = "INSERT INTO items (c_id,item_name,item_quantity,item_price) VALUES (%s, %s, %s, %s)"
                        val = (c_id, item_name, item_quantity, item_price)
                        try:
                            mycursor.execute(sql,val)
                            mydb.commit() 
                            print("╭────────────────────────────────────╮")
                            print("│      Item added succesfully        │")
                            print("╰────────────────────────────────────╯")
                            manage_stock()
                        except:
                            print("╭───────────────────────╮")
                            print("│  Something went wrong │")
                            print("╰───────────────────────╯")
                            manage_stock()
                        # try:
                        #     mycursor.execute("insert into items (c_id,item_name,item_quantity,item_price) values ('"+c_name+"')")
                        #     mydb.commit()
                        #     print("╭──────────────────────────────────────────╮")
                        #     print("│      Catagory created successfully       │")
                        #     print("╰──────────────────────────────────────────╯") 
                        #     manage_catagory()
                        # except:
                        #     print("╭────────────────────────────────────────╮")
                        #     print("│         Catagory already exists        │")
                        #     print("╰────────────────────────────────────────╯")     
                        #     manage_catagory()  
                    
                    def show_items():
                        mycursor.execute("SELECT * FROM items;")
                        data = mycursor.fetchall()
                        h = ['Item ID','Catagory ID','Item Name','Item Quantity','Item Price']
                        print(tabulate(data,headers=h,tablefmt='psql'))
                        manage_stock()

                    

                    def del_item():
                        mycursor.execute("SELECT * FROM items;")
                        data = mycursor.fetchall()
                        h = ['Item ID','Catagory ID','Item Name','Item Quantity','Item Price']
                        print(tabulate(data,headers=h,tablefmt='psql'))
                        kill = input("Enter the Item ID: ")
                        killi=int(kill)

                        mycursor.execute("SELECT item_id FROM items;")
                        d_id = mycursor.fetchall()

                        tr = 0
                        for i in d_id:
                            for j in i:
                                if j == killi:
                                    tr=tr+1
                         
                        if tr == 1:                                                     
                            mycursor.execute("delete from items where item_id='"+kill+"'")
                            mydb.commit()
                            print("╭──────────────────────────────────────────╮")
                            print("│        Item deleted successfully!        │")
                            print("╰──────────────────────────────────────────╯")                           
                            print("\n")
                            
                        else:
                            print("╭───────────────────────────────────────╮")
                            print("│   Please enter a valid Items ID!      │")
                            print("╰───────────────────────────────────────╯")
                            manage_stock()


                        manage_stock()


                    print("╭────────────────────────────────────────╮")
                    print("│     Welcome to Stock management        │")
                    print("╰────────────────────────────────────────╯")
                    print("╭─────────────────────────────────────────────╮")
                    print("│ ▶︎ 1 • Add new items                         │")
                    print("├─────────────────────────────────────────────┤")
                    print("│ ▶︎ 2 • Show current items                    │")
                    print("├─────────────────────────────────────────────┤")
                    print("│ ▶︎ 3 • Export stock list to CSV file         │")
                    print("├─────────────────────────────────────────────┤")
                    print("│ ▶︎ 4 • Delete an existing item               │")
                    print("├─────────────────────────────────────────────┤")
                    print("│ ▶︎ 5 • Go Back                               │")
                    print("├─────────────────────────────────────────────┤")
                    print("│ ▶︎ 6 • Exit System                           │")
                    print("╰─────────────────────────────────────────────╯")

                    ach = input("\n  ☞ Enter your command: ")
                    try:
                        ach=int(ach)
                    except:
                        print("╭───────────────────────────────────╮")
                        print("│     Please enter valid command    │")
                        print("╰───────────────────────────────────╯")                                
                        manage_stock()
                    
                    if ach == 1:
                        add_stock()

                    if ach == 2:
                        show_items()

                    if ach == 3:
                        def csv_stock():
                            sq="SELECT * FROM items"                       
                            sql_query = pd.read_sql_query(sq,mydb)
                            df = pd.DataFrame(sql_query)
                            filenm=input("Enter file name:")
                            csvfile = filenm+".csv"
                            df.to_csv (csvfile, index = False)
                            manage_stock()
                        csv_stock()

                    if ach == 4:
                        del_item()

                    if ach == 5:
                        manager()

                    if ach == 6:
                        print("╭───────────────────────╮")
                        print("│    Exiting System..   │")
                        print("╰───────────────────────╯\n")
                        quit()


                    else:
                        print("╭───────────────────────────────────╮")
                        print("│     Please enter valid command    │")
                        print("╰───────────────────────────────────╯")
                        manager()
                    manager() 


####### End of Functions of Manager #######
###########################################
###########################################

################################################################################################  


                if usertype == 2:
                    def manager():
                        mycursor.execute("select f_name from manager where login_id='"+li+"'")
                        f_namex=mycursor.fetchone()
                        f_name = f_namex[0]
                        mycursor.execute("select l_name from manager where login_id='"+li+"'")
                        l_namex=mycursor.fetchone()
                        l_name = l_namex[0]
                        mycursor.execute("select m_id from manager where login_id='"+li+"'")
                        m_idx=mycursor.fetchone()
                        m_id = m_idx[0]
                        name = f_name+" "+l_name
                        print("╭────────────────────────────────╮")
                        print("│     Welcome Manager :",m_id,"       │")
                        print("╰────────────────────────────────╯")
                        print("╭──────────────────────────────────────╮")
                        print("│ ▶︎ 1 • Create new staff account       │")
                        print("├──────────────────────────────────────┤")
                        print("│ ▶︎ 2 • Manage Staffs                  │")
                        print("├──────────────────────────────────────┤")
                        print("│ ▶︎ 3 • Manage Catagory                │")
                        print("├──────────────────────────────────────┤")
                        print("│ ▶︎ 4 • Manage Stocks                  │")
                        print("├──────────────────────────────────────┤")
                        print("│ ▶︎ 5 • Logout                         │")
                        print("├──────────────────────────────────────┤")
                        print("│ ▶︎ 6 • Exit System                    │")
                        print("╰──────────────────────────────────────╯")
                        ach = input("\n  ☞ Enter your command: ")
                        try:
                            ach=int(ach)
                        except:
                            print("╭───────────────────────────────────╮")
                            print("│     Please enter valid command    │")
                            print("╰───────────────────────────────────╯")                                
                            manager()

                        if ach == 1:
                            create_staff()

                        if ach == 2:
                            manage_staff()

                        if ach == 3:
                            manage_catagory()

                        if ach == 4:
                            manage_stock()
                        
                        
                        if ach == 5:
                            print("╭───────────────────────╮")
                            print("│     Signing out..     │")
                            print("╰───────────────────────╯\n")
                            login()

                        if ach == 6:
                            print("╭───────────────────────╮")
                            print("│    Exiting System..   │")
                            print("╰───────────────────────╯\n")
                            quit()

                        else:
                            print("╭───────────────────────────────────╮")
                            print("│     Please enter valid command    │")
                            print("╰───────────────────────────────────╯")
                            manager()

                    manager()


################################################################################################

###########################################
###########################################
########### Functions of Staff ############

                def gen_bill():
                    def check_cus_exists():
                        phone = input("Enter the Customer Phone Number: ")
                        phonei=int(phone)

                        mycursor.execute("SELECT phone_no FROM customer;")
                        d_id = mycursor.fetchall()
                        tr = 0
                        for i in d_id:
                            for j in i:
                                ji = int(j)
                                if ji == phonei:
                                    tr=tr+1

                        if tr == 0:
                            print("╭─────────────────────────────────────────────────────╮")
                            print("│     Customer does not exsits add customer first     │")
                            print("╰─────────────────────────────────────────────────────╯")
                            cus_name = input("Enter customer name :")
                            phone_no = input("Phone Number :")
                            city = input("City :")
                            today = date.today()
                            stoday= str(today)
                            try:
                                sql = "INSERT INTO customer (cus_name,phone_no,city,date) VALUES (%s, %s, %s, %s)"
                                val = (cus_name,phone_no,city,stoday)
                                try:
                                    mycursor.execute(sql,val)
                                    mydb.commit() 
                                    print("╭──────────────────────────────────────╮")
                                    print("│     Customer added succesfully       │")
                                    print("╰──────────────────────────────────────╯")
                                    check_cus_exists()
                                except:
                                    print("╭───────────────────────╮")
                                    print("│  Something went wrong │")
                                    print("╰───────────────────────╯")
                                    gen_bill()

                            except:
                                print("╭───────────────────────╮")
                                print("│  Something went wrong │")
                                print("╰───────────────────────╯")
                                gen_bill()   

                        if tr == 1:
                            print("╭──────────────────────────────────────────────────╮")
                            print("│   ▶︎  Enter the Item Id to add item to cart       │")
                            print("│   ▶︎  Enter 0 to stop                             │")
                            print("╰──────────────────────────────────────────────────╯")



                            item_id = []
                            picked_item_id = []
                            picked_item_name = []
                            picked_item_quantity = []
                            picked_item_price = []
                            gen_loop = 0
                            no_of_items = 0
                            n=[]

                            mycursor.execute("SELECT item_id FROM items;")
                            myresult = mycursor.fetchall()
                            for x in myresult:
                                x=x[0]
                                item_id.append(x)
                                no_of_items = no_of_items + 1

                            def gen():
                                # print(picked_item_id)
                                # print(picked_item_quantity)
                                # print(picked_item_price)

                                # for i in range(gen_loop):
                                    #print(picked_item_id[i],picked_item_name[i],picked_item_quantity[i],picked_item_price[i])

                                headers = ['Item ID', 'Item Name', 'Quantity', 'Price']
                                table = zip(picked_item_id, picked_item_name, picked_item_quantity, picked_item_price)
                                print(tabulate(table, headers, tablefmt='psql'))
                                total_price = 0
                                for i in range(gen_loop):
                                    price_p = picked_item_quantity[i] * picked_item_price[i]
                                    total_price = total_price + price_p
                                print("\nTotal price: " , total_price,"\n")

                                staff()





                            for i in range(no_of_items):
                                i_id =int(input("Enter item ID: "))
                                
                                if i_id == 0:
                                    gen()

                                elif i_id != 0:
                                    if i_id in item_id:
                                        picked_item_id.append(i_id)

                                    elif i_id not in item_id:
                                        print("╭──────────────────────────────────────╮")
                                        print("│        Enter a valid Item id         │")
                                        print("╰──────────────────────────────────────╯")
                                        gen()
                                qu_of_items = int(input("Enter the number of items:"))
                                sql = "SELECT item_quantity FROM items where item_id = "
                                code = sql+str(i_id)
                                mycursor.execute(code)
                                myresult = mycursor.fetchone()
                                a_i_q=int(myresult[0])
                                if qu_of_items>a_i_q:
                                    print("╭────────────────────────────╮")
                                    print("│        Out of Stock        │")
                                    print("╰────────────────────────────╯")
                                else:
                                    picked_item_quantity.append(qu_of_items)

                                    new_item_quantity = a_i_q - qu_of_items

                                    sql1 = "UPDATE items SET item_quantity = "
                                    sql2 = " WHERE  item_id = ";
                                    code = sql1+str(new_item_quantity)+sql2+str(i_id)
                                    mycursor.execute(code)
                                    mydb.commit()



                                sql = "SELECT item_price FROM items where item_id = "
                                code = sql+str(i_id)
                                mycursor.execute(code)
                                myresult = mycursor.fetchone()
                                a_i_p=int(myresult[0])
                                picked_item_price.append(a_i_p)

                                sql = "SELECT item_name FROM items where item_id = "
                                code = sql+str(i_id)
                                mycursor.execute(code)
                                myresult = mycursor.fetchone()
                                a_i_n=myresult[0]
                                picked_item_name.append(a_i_n)


                                gen_loop = gen_loop + 1
                                
                                



                                                        

                    check_cus_exists()

                def add_customer():
                    cus_name = input("Enter customer name :")
                    phone_no = input("Phone Number :")
                    city = input("City :")
                    today = date.today()
                    stoday= str(today)
                    try:
                        sql = "INSERT INTO customer (cus_name,phone_no,city,date) VALUES (%s, %s, %s, %s)"
                        val = (cus_name,phone_no,city,stoday)
                        try:
                            mycursor.execute(sql,val)
                            mydb.commit() 
                            print("╭──────────────────────────────────────╮")
                            print("│     Customer added succesfully       │")
                            print("╰──────────────────────────────────────╯")
                            staff()
                        except:
                            print("╭───────────────────────╮")
                            print("│  Something went wrong │")
                            print("╰───────────────────────╯")
                            staff()

                    except:
                        print("╭───────────────────────╮")
                        print("│  Something went wrong │")
                        print("╰───────────────────────╯")
                        staff()                      

                def manage_customer():

                    def show_customer():
                        mycursor.execute("SELECT * FROM customer;")
                        data = mycursor.fetchall()
                        h = ['Customer ID','Name','Phone Number','City','Date']
                        print(tabulate(data,headers=h,tablefmt='psql'))
                        manage_customer()

                    def delete_customer():
                        mycursor.execute("SELECT * FROM customer;")
                        data = mycursor.fetchall()
                        h = ['Customer ID','Name','Phone Number','City','Date']
                        print(tabulate(data,headers=h,tablefmt='psql'))
                        kill = input("Enter the Customer ID: ")
                        killi=int(kill)

                        mycursor.execute("SELECT cus_id FROM customer;")
                        d_id = mycursor.fetchall()

                        tr = 0
                        for i in d_id:
                            for j in i:
                                if j == killi:
                                    tr=tr+1
                         
                        if tr == 1:                                                     
                            mycursor.execute("delete from customer where cus_id='"+kill+"'")
                            mydb.commit()
                            print("╭──────────────────────────────────────────╮")
                            print("│      Customer deleted successfully!      │")
                            print("╰──────────────────────────────────────────╯")                           
                            print("\n")
                            
                        else:
                            print("╭───────────────────────────────────────╮")
                            print("│   Please enter a valid Customer ID!   │")
                            print("╰───────────────────────────────────────╯")
                            manage_customer()


                        manage_customer()


                    print("╭───────────────────────────────────╮")
                    print("│   Welcome to Customer Management  │")
                    print("╰───────────────────────────────────╯")
                    print("╭──────────────────────────────────────────────╮")
                    print("│ ▶︎ 1 • Show Customer                          │")
                    print("├──────────────────────────────────────────────┤")
                    print("│ ▶︎ 2 • Delete Customer                        │")
                    print("├──────────────────────────────────────────────┤")
                    print("│ ▶︎ 3 • Export Customer details to CSV file    │")
                    print("├──────────────────────────────────────────────┤")
                    print("│ ▶︎ 4 • Go Back                                │")
                    print("├──────────────────────────────────────────────┤")
                    print("│ ▶︎ 5 • Exit System                            │")
                    print("╰──────────────────────────────────────────────╯")


                    ach = input("\n  ☞ Enter your command: ")
                    try:
                        ach=int(ach)
                    except:
                        print("╭───────────────────────────────────╮")
                        print("│     Please enter valid command    │")
                        print("╰───────────────────────────────────╯")                                
                        staff()
                    if ach == 1:
                        show_customer()

                    if ach == 2:
                        delete_customer()

                    if ach == 3:
                        def csv_customer():
                            sq="SELECT * FROM customer"                       
                            sql_query = pd.read_sql_query(sq,mydb)
                            df = pd.DataFrame(sql_query)
                            filenm=input("Enter file name:")
                            csvfile = filenm+".csv"
                            df.to_csv (csvfile, index = False)
                            manage_customer()
                        csv_customer()
                    
                    if ach == 4:
                        staff()

                    if ach == 5:
                        print("╭───────────────────────╮")
                        print("│    Exiting System..   │")
                        print("╰───────────────────────╯\n")
                        quit()

                    else:
                        print("╭───────────────────────────────────╮")
                        print("│     Please enter valid command    │")
                        print("╰───────────────────────────────────╯")
                        staff()
                    staff() 



######## End of Functions of Staff ########
###########################################
###########################################

################################################################################################  


                if usertype == 3:
                    def staff():
                        mycursor.execute("select staff_id from staff where login_id='"+li+"'")
                        s_idx=mycursor.fetchone()
                        s_id = s_idx[0]
                        print("╭────────────────────────────────╮")
                        print("│     Welcome Staff :",s_id,"         │")
                        print("╰────────────────────────────────╯")
                        print("╭──────────────────────────────────────╮")
                        print("│ ▶︎ 1 • Generate Bill                  │")
                        print("├──────────────────────────────────────┤")
                        print("│ ▶︎ 2 • Add Customers                  │")
                        print("├──────────────────────────────────────┤")
                        print("│ ▶︎ 3 • Manage Customers               │")
                        print("├──────────────────────────────────────┤")
                        print("│ ▶︎ 4 • Logout                         │")
                        print("├──────────────────────────────────────┤")
                        print("│ ▶︎ 5 • Exit System                    │")
                        print("╰──────────────────────────────────────╯")
                        ach = input("\n  ☞ Enter your command: ")
                        try:
                            ach=int(ach)
                        except:
                            print("╭───────────────────────────────────╮")
                            print("│     Please enter valid command    │")
                            print("╰───────────────────────────────────╯")                                
                            staff()

                        if ach == 1:
                            gen_bill()

                        if ach == 2:
                            add_customer()
                        
                        if ach == 3:
                            manage_customer()
                        
                        
                        if ach == 4:
                            print("╭───────────────────────╮")
                            print("│     Signing out..     │")
                            print("╰───────────────────────╯\n")
                            login()

                        if ach == 5:
                            print("╭───────────────────────╮")
                            print("│    Exiting System..   │")
                            print("╰───────────────────────╯\n")
                            quit()

                        else:
                            print("╭───────────────────────────────────╮")
                            print("│     Please enter valid command    │")
                            print("╰───────────────────────────────────╯")
                            staff()

                    staff()




            if password!=pwi:
                print("╭───────────────────────╮")
                print("│  INVALID PASSWORD..!  │")
                print("╰───────────────────────╯")
                login()
            
        login()

    elif user_choice == 2:
        quit()

    else:
        print("╭─────────────────────────────────╮")
        print("│  Please enter a valid command!  │")
        print("╰─────────────────────────────────╯")

        system_init()
#system_init()
# Calling function
att = dir()
# Displaying result
print(att)