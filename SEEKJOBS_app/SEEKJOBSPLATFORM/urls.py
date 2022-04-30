from django.urls import path

import SEEKJOBSPLATFORM.views as views

app_name = 'SEEKJOBSPLATFORM'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('jobs', views.jobs, name='jobs'),
    path('recommendations', views.recommendations, name='recommendations'),
    path('register', views.register, name='register'),
    path('login', views.loginview, name='login'),
    path('uploadcv', views.uploadcv, name='uploadcv'),
    path('job/<int:job_id>', views.job, name='job'),
    path('resume/<str:username>', views.resume, name='resume'),
    path('applications/<int:job_id>', views.application, name='applications'),
    path('complete-company', views.CompanyInfo, name="complete-company"),
    path('jobs/new', views.post, name="post-a-job"),
    path('logout', views.logout_view, name="logout"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('job/apply', views.apply, name="apply"),
    path('company/<str:name>', views.companyprofile, name="company"),
    path('companies', views.companies, name="companies")
]
