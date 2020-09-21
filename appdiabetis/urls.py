from appdiabetis import views
 
 
from django.urls import path, include




urlpatterns = [
     
    path('',views.project_home,name="projecthome"),
    path('signup',views.signup, name='signup'),
    path('login',views.login, name='login'),
    path('predict',views.predict, name='predict'),

    
]
