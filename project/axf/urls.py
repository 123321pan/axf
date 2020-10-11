
from django.urls import path,re_path
from . import views
urlpatterns = [
    path('home/', views.home),
    re_path(r'market/(\d+)/(\d+)/(\d+)', views.market),
    re_path(r'login/', views.login),
    re_path(r'register/', views.register),
    re_path(r'checkuserid/', views.checkuserid),
    re_path(r'quit/', views.quit),
    re_path(r'changecart/(\d+)', views.changecart),
    path('cart/', views.cart),
    path('mine/', views.mine),

]