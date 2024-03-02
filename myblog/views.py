from django.shortcuts import render,redirect,get_object_or_404
import requests
import datetime
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import *
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .helpers import send_forgot_password_mail,send_contactus_mail,send_email_verify_otp,validate_email
from django.contrib.auth.models import User
# from django.http import HttpResponseRedirect
# from django.urls import reverse


def home(request):
    posts = Post.objects.all()
    p=Paginator(posts,3)   #paginator object
    page_number=request.GET.get('page')  #fetching page no from url
    try:
        page_obj=p.get_page(page_number)  #return desired page object
    except PageNotAnInteger:
        #if page is not integer then assign first page
        page_obj=p.page(1)
    except EmptyPage:
        #if page is empty then return last page
        page_obj=p.page(p.num_page)
    context={'page_obj':page_obj}
    return render(request,'home.html',context)


@login_required(login_url='login')
def addpost(request):
    if request.method=='POST':
        form = AddPostForm(request.POST,request.FILES)
        if form.is_valid():  
            user_form=form.save(commit=False)
            user_form.user=request.user
            user_form.save()
            # print(user_form.user)
            # print(request.FILES)
            # print(user_form.date)
            
            # post=Post()
            # post.user=request.user
            # post.title=request.POST.get('title')
            # post.author=request.POST.get('author')
            # post.description=request.POST.get('post_desc')
            # post.date=datetime.datetime.now()
            # post.save()
            # form.save()
            messages.success(request,'Post was created successfully ')
            return redirect('addpost')
        # else:
        #   print(f'is valid is not working {request.user}')
    form = AddPostForm()
    context={ 'form':form }
    return render(request,'addpost.html',context)
        
       
    


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()  
                # email=form.cleaned_data.get('email')
                # print(email)
                # print(validate_email(email))
                user=form.cleaned_data.get('username')
                
                
                messages.success(request,'Account created successfully for '+user )
                return redirect('home')
            messages.error(request,"Enter password again")
        context={ 'form':form }
        return render(request,'register.html',context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,f'Welcome {username} you logged in succesfully.')
                return redirect('home')
            else:
                messages.info(request,'Username or Password incorrect')

        context={ }
        return render(request,'login.html',context)
    
def adminLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/admin')
        else:
            messages.info(request,'Username or Password incorrect')
        
    return render(request,'admin_login.html')
    

def post_d(request,pk=1):
    post_detials=Post.objects.get(pk=pk)
    total_likes=post_detials.total_likes()
    comments=Comment.objects.filter(post_id=pk)
    # for c in comments:
    #     print(c)
    
    liked=False
    #if user already liked
    if post_detials.likes.filter(id=request.user.id).exists():
         liked=True
    
    context={'post_detials':post_detials,'total_likes':total_likes,'liked':liked,'comments':comments}
    return render(request,'post.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def admin_login(request):
    
    return render(request,'admin_login.html')

import uuid
def ForgotPassword(request):
    try:
        if request.method == "POST":
           username = request.POST.get('username')

           if not User.objects.filter(username=username).first():     
            messages.success(request,'User Not Found.')
            return redirect('/forgot_password/')
          
           user_obj=User.objects.get(username=username)
           user_email=user_obj.email
           token=str(uuid.uuid4())
           print(user_email)
           username=user_obj.username
           print(send_forgot_password_mail(user_email,token,username))
           messages.success(request,'An email has been sent.')
           context={}
           return redirect('/forgot_password/',context)
        
    except Exception as e:
        messages.info(request,'Please check your internet connection.')
        return redirect(f'/forgot_password/')
        print(e)
    
    return render(request,'forgot_password.html')

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings



def VerifyEmail(request):
    try:
        if request.method == "POST":
            
            user_email= request.POST.get('email')
            print(user_email)
            print(validate_email(user_email))
            if(validate_email(user_email)):
                # template= render_to_string('emailMessage.html',{'email':user_email}) 
                # context={'email':user_email,'activation_link':'http://127.0.0.1:8000/email_success'}
                context={'email':user_email,'activation_link':'https://ganeshgodse.pythonanywhere.com/email_success'}
                email_content = render(request, 'emailMessage.html', context).content.decode('utf-8')
            
                email = EmailMessage (
                    'Activate Your Account',
                    email_content,
                    settings.EMAIL_HOST_USER,
                    [user_email],
                )
                email.fail_silently=False
                email.content_subtype = 'html' 
                email.send()
                messages.success(request,'An email has been sent.')
                context={'email_sendended':True,'email':user_email}
            
                return render(request,'verifyEmail.html',context)
            else:
                messages.info(request,'Inavlid Email Plaese Enter Valid Email')
                return render(request,'verifyEmail.html')

            
        else:
            print(request.method )

    
    except Exception as e:
        
        messages.info(request,'Invalid email please enter valid one')
        print(e)
    return render(request,'verifyEmail.html')


def EmailSucces(request):
    return redirect('register')

def ChangePassword(request,username,token):
    try:
        if request.method == "POST":
           new_password = request.POST.get('new_password')
           confirm_password = request.POST.get('confirm_password')
        
        if username is None:
            messages.success(request,'User id Not Found.')
            return redirect(f'/change_password/{username}/{token}/')

        if new_password != confirm_password:
            messages.success(request,'Both should equal.')
            return redirect(f'/change_password/{username}/{token}/')
        
        user_obj=User.objects.get(username=username)
        user_obj.set_password(new_password)
        user_obj.save()
        return redirect('/login/')

    except Exception as e:
        print(e)
    
    return render(request,'change_password.html')


def Contact_Us(request):
    try:
        if request.method == "POST":
            message = request.POST.get('message')
            user_emailadd = request.POST.get('email')
            user_name = request.POST.get('name')
            if  not message :
                messages.success(request,'Please Enter Your Message.')
                return redirect('/contact_us/')

            send_contactus_mail(user_emailadd,message,user_name)
            messages.success(request,'Thank You For Your Feedback.')
            return redirect('/contact_us/')
    
    except Exception as e:
        print(e)
    
    return render(request,'contactus.html')
    
def About_Us(request):
    return render(request,'aboutus.html')

def Search_Post(request):
    try:
        if request.method == "POST":
            user_search= request.POST.get('user_search')
            if not user_search:
                messages.success(request,'Please Enter Again.')
                return redirect('/search_post/')

            mydata= Post.objects.filter(title__icontains=user_search).values()
            #pagination
            p=Paginator(mydata,3) 
            page_number=request.GET.get('page')  #fetching page no from url
            try:
                page_obj=p.get_page(page_number)  #return desired page object
            except PageNotAnInteger:
                #if page is not integer then assign first page
                page_obj=p.page(1)
            except EmptyPage:
                #if page is empty then return last page
                page_obj=p.page(p.num_page)
            context={'mydata':mydata,'page_obj':page_obj}
            return render(request,'search_post.html',context)
            
    except Exception as e:
        print(e)
        return redirect('home')

@login_required(login_url='login')
def MyPost(request):
    if request.user.is_authenticated:
        logged_in_user=request.user
        logged_in_user_posts=Post.objects.filter(user=logged_in_user).values()
        #pagination
        p=Paginator(logged_in_user_posts,3) 
        page_number=request.GET.get('page')  #fetching page no from url
        try:
            page_obj=p.get_page(page_number)  #return desired page object
        except PageNotAnInteger:
            #if page is not integer then assign first page
            page_obj=p.page(1)
        except EmptyPage:
            #if page is empty then return last page
            page_obj=p.page(p.num_page)
        
        context={'logged_in_user_posts':logged_in_user_posts,'page_obj':page_obj}
        return render(request,'mypost.html',context)
    else:
        messages.info(request,'Username or Password incorrect')
        return redirect('/login/')

# @login_required(login_url='login')
# def EditPost(request,pk):
#     try:
#         post_to_edit= Post.objects.get(pk=pk)
#         user=request.user
#         print(post_to_edit)
#         post_changed=False
         
#         if request.method=='POST' and request.FILES:
#             post_to_edit.title=request.POST.get('title')
#             post_to_edit.author=request.POST.get('author')
#             post_to_edit.description=request.POST.get('post_desc')
#             post_to_edit.date=datetime.datetime.now()
#             post_to_edit.user_id=user.id
#             post_to_edit.post_image=request.POST.get('myfile')
#             print(post_to_edit.post_image)   
#             post_to_edit.save()
#             post_changed=True
            
#             # print(post_changed)
#         context={ 'post_to_edit' : post_to_edit,'post_changed':post_changed }
#         return render(request,'edit_post.html',context)
        
    # except Exception as e:
    #     print(e)
    #     return render(request,'mypost.html')

@login_required(login_url='login')
def EditPost(request,pk):
    try:
        post_to_edit= Post.objects.get(pk=pk)
        user=request.user
        post_changed=False
        if request.method == 'POST':
            form = AddPostForm(data=request.POST,files=request.FILES,instance=post_to_edit)
            if form.is_valid():
                form.save()
                post_changed=True
                messages.success(request,'Post has been changed succesfully.')
                # return render(request,f'edit_post/{pk}/',{'post_changed':post_changed})
                return redirect('/logged_in_user_posts/')
        form=AddPostForm(instance=post_to_edit)
        context={ 'post_to_edit' : post_to_edit,'post_changed':post_changed,'form':form}
        return render(request,'edit_post.html',context)
    except Exception as e:
        print(e)
        return render(request,'mypost.html')

def EmailVerification(request):
    try:   
        if request.method == "POST":
            email = request.POST.get('email')
            if email:
                return redirect(f'/otp_verification/{email}/')
            # return render(request,f'otp_verification/{email}/',{'email':email})

        return render(request,'email_verification.html')

    except Exception as e:
        print(e)
        return render(request,'email_verification.html')

def OtpVerification(request,email):
    try:
        user_otp=str(send_email_verify_otp(email))
        print(user_otp)
        if request.method == "POST":
            otp = request.POST.get('otp')
            print(type(otp))
            if user_otp==otp:
                return redirect('rgister')
            else:
                messages.success(request,'Invaild otp.')
        return render(request,'otp_verification.html')
    except Exception as e:
        print(e)
        return render(request,'otp_verification.html')

@login_required(login_url='login')    
def LikePost(request,pk):
    # post=Post.objects.get(pk=pk)
    post=get_object_or_404(Post,id=pk)
    liked=False
    #if user already liked
    if post.likes.filter(id=request.user.id).exists():
        liked=False
        post.likes.remove(request.user)
    else:
        liked=True
        post.likes.add(request.user)
    return redirect(f'/post/{pk}/')
    # return HttpResponseRedirect(reverse(f'post/{pk}/'))

@login_required(login_url='login')    
def AddComment(request,pk):
    if request.method=='POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():  
            user_form=form.save(commit=False)
            user_form.post_id=pk
            user_form.save()
            print("ssssssssssssssssss")
            comment=Comment.objects.get(pk=pk)
        
            print(comment)
            return redirect(f'/post/{pk}/')
  
    form = AddCommentForm()
    context={ 'form':form }
    return render(request,'add_comment.html',context)