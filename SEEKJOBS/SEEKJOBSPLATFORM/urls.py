from django.urls import path
import SEEKJOBSPLATFORM.views as views

app_name = 'SEEKJOBSPLATFORM'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('jobs', views.jobs, name='jobs'),
    path('register', views.register, name='register'),
    path('login', views.loginview, name='login'),
    path('uploadcv', views.uploadcv, name='uploadcv'),
    path('job/<int:job_id>', views.job, name='job'),
    path('resume/<str:username>', views.resume, name='resume'),
  
]

