from django.urls import path
from .views import *
from .views import signup,login,logout,servicepro,show1,show2,servicecreate,contacts

urlpatterns = [
    path('signup', signup, name='signup'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('servicepro', servicepro, name='servicepro'),
    path('adminclint', ClientView, name='adminclint'),
    path('show1', show1,name='show1'),
    path('show2',show2,name='show2'),
    path('servicecreate', servicecreate, name='servicecreate'),
    path('contact',contacts,name='contact')

]
