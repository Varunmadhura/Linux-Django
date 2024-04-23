from django.urls import path
from testapp import views

urlpatterns = [
    path('',views.user_login, name='login'),
    path('scenario2/', views.scenario2, name='scenario2'),
    path('execute_command/',views.execute_command, name ='execute_command')

]
