from django.shortcuts import render
from django.http import HttpResponse
import mysql.connector as sql
fn=''
mn=''
ln=''
email_pri=''
email_bak=''
pwd=''


def home(request):
     return render(request,"user/home.html")


def signup(request):
    global user_id,net_id,fn,mn,ln,email_pri,email_bak,pwd
    if request.method=='POST':
        m=sql.connect(host="localhost",user="root",passwd="Mango@100",database='nyunite')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key=="net_id":
                net_id=value
            elif key=="first_name":
                fn=value
            elif key=="middle_name":
                mn=value
            elif key=="last_name":
                ln=value
            elif key=="email_pri":
                email_pri=value
            elif key=="email_bak":
                email_bak=value
            elif key=="password":
                pwd=value
        c=" insert into user(net_id,first_name,middle_name,last_name,email_pr,email_bak,password) values('{}','{}','{}','{}','{}','{}','{}')".format(net_id,fn,mn,ln,email_pri,email_bak,pwd)
        cursor.execute(c)
        m.commit()
            
    return render(request,"user/signup.html")

def login(request):
    global net_id,pwd
    if request.method=='POST':
        m=sql.connect(host="localhost",user="root",passwd="Mango@100",database='nyunite')
        cursor=m.cursor()
        d=request.POST
        for key,value in d.items():
            if key=="net_id":
                net_id=value
            elif key=="password":
                pwd=value
        c="select * from user where net_id='{}' and password='{}'".format(net_id,pwd)
        cursor.execute(c)
        t=tuple(cursor.fetchall())
        if t==():
            return render(request,'error.html')
        else:
            return render (request,'welcome.html')

    return render(request,"user/login.html") 

def logout(request):
    pass


# Create your views here.
