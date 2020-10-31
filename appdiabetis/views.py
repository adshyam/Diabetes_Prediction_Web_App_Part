from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from django.contrib.auth.models import User
from django.contrib import auth
import numpy as np
import joblib

model=joblib.load("./MOdelStore/model")


# Create your views here.
def project_home(request):
    return render(request, 'appdiabetis/home.html')

def app_home(request):
    return render(request, 'appdiabetis/index_app.html')



def signup(request):
    if request.method=='POST':

        #checking if the user confirmed the password
        if request.POST['password']==request.POST['passwordagain']:
            # check if the user is already registered or not
            try:
                user=User.objects.get(username=request.POST['email'])
                return render(request,'appdiabetis/home.html',{'message': 'this email is already registered !'})

            except User.DoesNotExist:
                user=User.objects.create_user(username=request.POST['email'],password=request.POST['password'],first_name=request.POST['fullName'])
                return render(request,'appdiabetis/home.html',{'message': 'registration success! log in now! '})



            

        else:
            return render(request,'appdiabetis/home.html',{'message': 'password do not match '})

    
        
    else:
        return render(request, 'appdiabetis/home.html')
def login(request):


    if request.method=='POST':
        username=request.POST['email']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return render(request, 'appdiabetis/input.html')
        else:
            return render(request, 'appdiabetis/home.html',{'message':'User Credential does not match'})
    else:
         return render(request, 'appdiabetis/home.html')

     


def predict(request):
    if request.method =='POST':
         
       
         


        temp={}
        # if(type(request.POST.get('crim')))=='string':
        #     print("success")
        #     temp['crim']=0.0


        temp['preg']= request.POST['pregency']
        temp['glu']=  request.POST['glucose']
        temp['bp']=  request.POST['pressure']
        temp['skin']=  request.POST['skin']
        temp['ins']= request.POST['insulin']
        temp['bmi']= request.POST['bmi']
        temp['pedgree']= request.POST['diabetis']
        temp['age']= request.POST['age']
    else:
        return render(request, 'appdiabetis/input.html')

    # testing=pd.DataFrame({'x':temp}).transpose()
    testing=pd.DataFrame([temp])
    result=model.predict_proba(testing)
    # print("hte result is ",result)
    for i in result:
         
        noDiabetis=np.around(i[0],3)
        yesDiabetis=(np.around(i[1],3))*100
    params={'no': noDiabetis,'yes':yesDiabetis}
     
    return render(request,'appdiabetis/input.html',{'params':yesDiabetis})
     