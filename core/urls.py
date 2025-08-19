from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('airbnb/', views.airbnb, name='airbnb'),
    path('airbnb/<slug:slug>/', views.airbnb_detail, name='airbnb_detail'),
    path('courses/', views.courses, name='courses'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('careers/', views.careers, name='careers'),
    path('contact/', views.contact, name='contact'),
]
