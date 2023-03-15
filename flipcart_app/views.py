import os
import uuid
from django.shortcuts import render,HttpResponse,redirect
from .forms import *
from .models import *

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from flipcart_pj.settings import EMAIL_HOST_USER
from django.contrib.auth import authenticate

# -----------------     0.index page      -----------------
def index(request):
    if request.method=="POST":
        if 'shop_form' in request.POST:
            a=shoplogform(request.POST)
            if a.is_valid():
                un=a.cleaned_data['uname']
                pw=a.cleaned_data['password']
                b=shopregmodel.objects.all()
                for i in b:
                    if i.uname==un and i.password==pw:
                        pic=str(i.pic).split('/')[-1]
                        id=i.id
                        usn=i.uname
                        
                        global val
                        def val():
                            return i
                        request.session['p_pic']=pic
                        request.session['p_id']=id
                        request.session['p_usn']=usn
                        
                        #-----------  1.globaly decleration ---------
                        # request.session['username']=usn
                        
                        
                        #-----------  2.globaly decleration ---------
                        # global val
                        # def val():
                        #     return id
                        
                        # print("----------------success-------------------")
                        return redirect(shopprofile)#url
                else:
                    return HttpResponse("password not matched")
            return HttpResponse("Login Not Succefull")
        elif 'user_form' in request.POST:
            username=request.POST.get('uname')
            password=request.POST.get('password')
            user_obj=User.objects.filter(username=username).first()
            
            if user_obj is None:
                messages.success(request,'user not found')
                return redirect(index)
            profile_obj=userregmodel.objects.filter(user=user_obj).first()
            
            if not profile_obj.is_verified:
                messages.success(request,'profile not verified check your mail')
                return redirect(index)
            user=authenticate(username=username,password=password)
            
            if user is None:
                messages.success(request,'wrong password or username')
                return redirect(index)
            request.session['u_name']=profile_obj.user.username
            pic=str(profile_obj.pic).split('/')[-1]
            request.session['u_pic']=pic
            return redirect(userpofile)
    
    
    
    return render(request,'index.html')

# -----------------     1.shop Register page      -----------------
def shopregister(request):
    if request.method=="POST":
        a=shopregform(request.POST,request.FILES)
        if a.is_valid():
            if a.cleaned_data['password']==a.cleaned_data['cpassword']:
                b=shopregmodel(uname=a.cleaned_data["uname"],
                               email=a.cleaned_data["email"],
                               oname=a.cleaned_data["oname"],
                               sname=a.cleaned_data["sname"],
                               password=a.cleaned_data["password"],
                               pic=a.cleaned_data["pic"])
                b.save()
                return redirect(shoplogin)
            else:
                return HttpResponse("registration filed")
    return render(request,'shopregister.html')

# -----------------     1.shop Login page      -----------------

def shoplogin(request):
    if request.method=="POST":
        a=shoplogform(request.POST)
        if a.is_valid():
            un=a.cleaned_data['uname']
            pw=a.cleaned_data['password']
            b=shopregmodel.objects.all()
            for i in b:
                if i.uname==un and i.password==pw:
                    pic=str(i.pic).split('/')[-1]
                    id=i.id
                    usn=i.uname
                    
                    global val
                    def val():
                        return i
                    request.session['p_pic']=pic
                    request.session['p_id']=id
                    request.session['p_usn']=usn
                    
                    #-----------  1.globaly decleration ---------
                    # request.session['username']=usn
                    
                    
                    #-----------  2.globaly decleration ---------
                    # global val
                    # def val():
                    #     return id
                    
                    # print("----------------success-------------------")
                    return redirect(shopprofile)#url
            else:
                return HttpResponse("password not matched")
        return HttpResponse("Login Not Succefull")
    return render(request,'shoplogin.html')

# -----------------     1.shop Profile page      -----------------

def shopprofile(request):
    p_id=request.session['p_id']
    p_usn=request.session['p_usn']
    p_pic=request.session['p_pic']
    a=shopaddmodel.objects.all()
    # print('-------------',a,'---------------')
    na=[]
    pr=[]
    di=[] 
    ca=[]
    im=[]
    id=[]
    for i in a:
        if i.sid==p_id:
            na.append(i.iname)
            pr.append(i.iprice)
            di.append(i.idisc)
            ca.append(i.category)
            im.append(str(i.iimage).split('/')[-1])
            id.append(i.id)
    mylist=zip(na,pr,di,ca,im,id)    
    
    
    
    
    #-----------  1.globaly decleration ---------
    # user=request.session['username']  
    
    
    #-----------  2.globaly decleration ---------
    # id=val()  
              
    return render(request,"shopprofile.html",{'mylist':mylist,'p_pic':p_pic,'p_id':p_id,'p_usn':p_usn})


def shopprofileedit(request,id):
    a=shopregmodel.objects.get(id=id)
    im=str(a.pic).split('/')[-1]
    if request.method=='POST':
        a.uname=request.POST.get('uname')
        a.email=request.POST.get('email')
        a.oname=request.POST.get('oname')
        a.sname=request.POST.get('sname')
        a.password=request.POST.get('password')
        if len(request.FILES)>0:
            if len(a.pic)>0:
                os.remove(a.pic.path)
            a.pic=request.FILES['pic']
        a.save()
        return redirect(shopprofile)
        
    return render(request,'shopprofileedit.html',{'a':a,'im':im})




# -----------------     1.shop Add item page      -----------------

def shopadd(request):
    p_id=request.session['p_id']
    if request.method=='POST':
        a=shopaddform(request.POST,request.FILES)
        if a.is_valid():
            b=shopaddmodel(iname=a.cleaned_data['iname'],
                           iprice=a.cleaned_data['iprice'],
                           idisc=a.cleaned_data['idisc'],
                           category=a.cleaned_data['category'],
                           iimage=a.cleaned_data['iimage'],
                           sid=a.cleaned_data['sid'])
            b.save()
            return redirect(shopprofile)
        else:
            return HttpResponse("data is not valid")
    return render(request,'shopadd.html',{'p_id':p_id})

# -----------------     1.shop Remove item page      -----------------

def shopremove(request,id):
    a=shopaddmodel.objects.get(id=id)
    if len(a.iimage)>0:
        os.remove(a.iimage.path)
    a.delete()
    return redirect(shopprofile)

# ----------------     1.shop Edit item page      -----------------

def shopedit(request,id):        
    a=shopaddmodel.objects.get(id=id)
    im=str(a.iimage).split('/')[-1]
    if request.method=='POST':
        a.iname = request.POST.get('iname')
        a.iprice = request.POST.get('iprice')
        a.idisc = request.POST.get('idisc')
        a.category = request.POST.get('category')
        if len(request.FILES)>0:
            if len(a.iimage)>0:
                os.remove(a.iimage.path)
            a.iimage=request.FILES['iimage']
        a.save()
        return redirect(shopprofile)
    return render(request,'shopedit.html',{'a':a,'im':im})    

# ----------------     2.user register page      -----------------

def userregister(request):
    if request.method=='POST':  
        username=request.POST.get('uname')
        email=request.POST.get('email')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword') 
        phone=request.POST.get('phone') 
        pic=request.FILES['pic']
        print(pic)
        if password == cpassword:
        
            # --------    user pic and phone    -------
            # a=userregform(request.FILES,request.POST)
            # if a.is_valid():
            #     b=userregmodel(pic=a.cleaned_data['pic'],phone=a.cleaned_data['phone'])
            #     b.save()
            # else:
            #     messages.success(request,'entered invalid data')
            # --------    User authentication    -------
            
            if User.objects.filter(username=username).first():
                messages.success(request,'Username already taken')
                return redirect(userregister)
            if User.objects.filter(email=email).first():
                messages.success(request,'Email Id already taken')
                return redirect(userregister)
            # if userregmodel.objects.filter(phone=phone).first():
            #     messages.success(request,'Phone Number already taken')
            #     return redirect(userregister)
            user_obj=User(username=username,email=email,first_name=fname,last_name=lname)
            user_obj.set_password(password)    
            user_obj.save()
            auth_token=str(uuid.uuid4())
            profile_obj=userregmodel.objects.create(user=user_obj,auth_token=auth_token,phone=phone,pic=pic)
            profile_obj.save()
            send_mail_user(email,auth_token,username)
            messages.success(request,'You have a messege..!!')  
            return redirect(userlogin)    
        else:
            messages.success(request,'password and confirm password must be same')
            return redirect(userregister)
    return render(request,'userregister.html')

# ----------------     2.user email send page      -----------------
def send_mail_user(email,auth_token,username):
    subject='Flipcart'
    message=username + f' please click the below link to varify your account http://127.0.0.1:8000/userverify/{auth_token}'
    email_from=EMAIL_HOST_USER
    recipient=[email]
    send_mail(subject,message,email_from,recipient)

# ----------------     2.user email verify page      -----------------
def userverify(request,auth_token):
    profile_obj=userregmodel.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request,'your account has been varified')
            return redirect(userlogin)
        profile_obj.is_verified=True
        profile_obj.save()
        messages.success(request,'your account has been varified')
        return redirect(userlogin)
    else:
        messages.success(request,"user not found")
        return redirect(userlogin)
        


# ----------------     2.user login page      -----------------
def userlogin(request):
    if request.method=='POST':
        username=request.POST.get('uname')
        password=request.POST.get('password')
        user_obj=User.objects.filter(username=username).first()
        
        if user_obj is None:
            messages.success(request,'user not found')
            return redirect(userlogin)
        profile_obj=userregmodel.objects.filter(user=user_obj).first()
        
        if not profile_obj.is_verified:
            messages.success(request,'profile not verified check your mail')
            return redirect(userlogin)
        user=authenticate(username=username,password=password)
        
        if user is None:
            messages.success(request,'wrong password or username')
            return redirect(userlogin)
        request.session['u_name']=profile_obj.user.username
        pic=str(profile_obj.pic).split('/')[-1]
        request.session['u_pic']=pic
        return redirect(userpofile)
    return render(request,'userlogin.html') 

# ----------------     2.user profil page      -----------------

def userpofile(request):
    u_name=request.session['u_name']
    u_pic=request.session['u_pic']
    a=shopaddmodel.objects.all()
    na1=[]
    na2=[]
    na3=[]
    na4=[]
    na5=[]
    na6=[]
    na7=[]
    na8=[]
    na9=[]
    na10=[]
    
    pr1=[]
    pr2=[]
    pr3=[]
    pr4=[]
    pr5=[]
    pr6=[]
    pr7=[]
    pr8=[]
    pr9=[]
    pr10=[]
    
    apr1=[]
    apr2=[]
    apr3=[]
    apr4=[]
    apr5=[]
    apr6=[]
    apr7=[]
    apr8=[]
    apr9=[]
    apr10=[]
    
    di1=[]
    di2=[]
    di3=[]
    di4=[]
    di5=[]
    di6=[]
    di7=[]
    di8=[]
    di9=[]
    di10=[]
     
    ca1=[]
    ca2=[]
    ca3=[]
    ca4=[]
    ca5=[]
    ca6=[]
    ca7=[]
    ca8=[]
    ca9=[]
    ca10=[]
    
    im1=[]
    im2=[]
    im3=[]
    im4=[]
    im5=[]
    im6=[]
    im7=[]
    im8=[]
    im9=[]
    im10=[]
    
    id1=[]
    id2=[]
    id3=[]
    id4=[]
    id5=[]
    id6=[]
    id7=[]
    id8=[]
    id9=[]
    id10=[]
    # print(a)
    for i in a:
        if i.category=="grocery":
            na1.append(i.iname)
            pr1.append(i.iprice)
            apr1.append(i.iprice + 50)
            di1.append(i.idisc)
            ca1.append(i.category)
            im1.append(str(i.iimage).split('/')[-1])
            id1.append(i.id)
        if i.category=="mobile":
            na2.append(i.iname)
            pr2.append(i.iprice)
            apr2.append(i.iprice + 50)
            di2.append(i.idisc)
            ca2.append(i.category)
            im2.append(str(i.iimage).split('/')[-1])
            id2.append(i.id)
        if i.category=="fashion":
            # print(i.iname)
            na3.append(i.iname)
            pr3.append(i.iprice)
            apr3.append(i.iprice + 50)
            di3.append(i.idisc)
            ca3.append(i.category)
            im3.append(str(i.iimage).split('/')[-1])
            id3.append(i.id)
        if i.category=="electronics":
            # print(i.iname)
            na4.append(i.iname)
            pr4.append(i.iprice)
            apr4.append(i.iprice + 50)
            di4.append(i.idisc)
            ca4.append(i.category)
            im4.append(str(i.iimage).split('/')[-1])
            id4.append(i.id)
        if i.category=="home":
            # print(i.iname)
            na5.append(i.iname)
            pr5.append(i.iprice)
            apr5.append(i.iprice + 50)
            di5.append(i.idisc)
            ca5.append(i.category)
            im5.append(str(i.iimage).split('/')[-1])
            id5.append(i.id)
        if i.category=="apllances":
            # print(i.iname)
            na6.append(i.iname)
            pr6.append(i.iprice)
            apr6.append(i.iprice + 50)
            di6.append(i.idisc)
            ca6.append(i.category)
            im6.append(str(i.iimage).split('/')[-1])
            id6.append(i.id)
        if i.category=="travel":
            # print(i.iname)
            na7.append(i.iname)
            pr7.append(i.iprice)
            apr7.append(i.iprice + 50)
            di7.append(i.idisc)
            ca7.append(i.category)
            im7.append(str(i.iimage).split('/')[-1])
            id7.append(i.id)
        if i.category=="topoffer":
            # print(i.iname)
            na8.append(i.iname)
            pr8.append(i.iprice)
            apr8.append(i.iprice + 50)
            di8.append(i.idisc)
            ca8.append(i.category)
            im8.append(str(i.iimage).split('/')[-1])
            id8.append(i.id)
        if i.category=="toys":
            # print(i.iname)
            na9.append(i.iname)
            pr9.append(i.iprice)
            apr9.append(i.iprice + 50)
            di9.append(i.idisc)
            ca9.append(i.category)
            im9.append(str(i.iimage).split('/')[-1])
            id9.append(i.id)
        if i.category=="twowheeler":
            # print(i.iname)
            na10.append(i.iname)
            pr10.append(i.iprice)
            apr10.append(i.iprice + 50)
            di10.append(i.idisc)
            ca10.append(i.category)
            im10.append(str(i.iimage).split('/')[-1])
            id10.append(i.id)
    # print(na1)
    # print(na2)
    mylist=zip(na1,pr1,di1,ca1,im1,id1,apr1)
    mylist2=zip(na2,pr2,di2,ca2,im2,id2,apr2)
    mylist3=zip(na3,pr3,di3,ca3,im3,id3,apr3)
    mylist4=zip(na4,pr4,di4,ca4,im4,id4,apr4)
    mylist5=zip(na5,pr5,di5,ca5,im5,id5,apr5)
    mylist6=zip(na6,pr6,di6,ca6,im6,id6,apr6)
    mylist7=zip(na7,pr7,di7,ca7,im7,id7,apr7)
    mylist8=zip(na8,pr8,di8,ca8,im8,id8,apr8)
    mylist9=zip(na9,pr9,di9,ca9,im9,id9,apr9)
    mylist10=zip(na10,pr10,di10,ca10,im10,id10,apr10)
    # print(mylist2)
    return render(request,'userprofile.html',{'u_name':u_name,'u_pic':u_pic,'mylist':mylist,
                                              'mylist2':mylist2,'mylist3':mylist3,'mylist4':mylist4,
                                              'mylist5':mylist5,'mylist6':mylist6,'mylist7':mylist7,
                                              'mylist8':mylist8,'mylist9':mylist9,'mylist10':mylist10})