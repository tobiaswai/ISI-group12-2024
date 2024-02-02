from django.urls import path
from . import views # the “.” means current directory

urlpatterns = [
 path('signup/', views.SignUpView.as_view(), name='signup'),
]
