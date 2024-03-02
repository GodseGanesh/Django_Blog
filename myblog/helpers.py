from django.core.mail import send_mail
from django.conf import settings
import random
import re

def validate_email(email):  
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):  
        return True  
    return False 


def send_forgot_password_mail(email,token,username):
    subject='Your forgot password link'
    message=f'Hi, Click on the link to reset your password http://127.0.0.1:8000/change_password/{username}/{token}'
    email_from=settings.EMAIL_HOST_USER
    recipent_list=[email]
    send_mail(subject,message,email_from,recipent_list,fail_silently=False)
    return True

def send_contactus_mail(email_from,message,name):
    subject=f'Feedback from {name}.'
    message=message
    email_from=email_from
    recipent_list=[settings.EMAIL_HOST_USER]
    send_mail(subject,message,email_from,recipent_list,fail_silently=False)
    return True

def send_email_verify_otp(email_to):
    subject='Welcome to Codinghunder.'
    otp=random.randint(1000,9999)
    message= f'Your email verfication otp is {otp}'
    email_from=settings.EMAIL_HOST_USER
    recipent_list=[email_to]
    send_mail(subject,message,email_from,recipent_list,fail_silently=False)
    return otp