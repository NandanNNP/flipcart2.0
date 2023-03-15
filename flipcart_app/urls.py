from django.urls import path
from .views import *
urlpatterns = [
    path('',index),
    # -----------     shop    ------------
    # path('',shoplogin),
    path('shoplogin/',shoplogin),
    path('shopregister/',shopregister),
    path('shopprofile/',shopprofile),
    path('shopadd/',shopadd),
    path('shopremove/<int:id>/',shopremove),
    path('shopedit/<int:id>/',shopedit),
    path('shopprofileedit/<int:id>/',shopprofileedit),
    
    # -----------     user    ------------
    path('userregister/', userregister),
    path('userlogin/',userlogin),
    path('userverify/<auth_token>',userverify),
    path('userprofile/',userpofile)
]