from django.urls import path
from . import views


urlpatterns = [
    path('',views.index, name='index'),
    path('face/',views.face,name='face'),
    path('facecam_feed', views.facecam_feed, name='facecam_feed'),
    path('face/current_passenger/',views.current_passenger,name="current_passenger"),
    path('face/current_passenger/generate_boarding_pass/',views.generate_boarding_pass, name='generate_boarding_pass'),
    path('face/current_passenger/generate_boarding_pass/nextp/',views.nextp,name="nextp"),
    path('add1/',views.add1,name="add1"),
    path('add1/addpassenger/',views.addpassenger,name="addpassenger"),
    path('displaypassenger/',views.displaypassenger,name="displaypassenger"),
    path('add2/',views.add2,name="add2"),
    path('add2/addflight/',views.addflight,name="addflight"),
    path('displayflight/',views.displayflight,name="displayflight"),


]