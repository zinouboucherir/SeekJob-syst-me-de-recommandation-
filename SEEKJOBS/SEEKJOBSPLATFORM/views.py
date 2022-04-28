from operator import itemgetter

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect


from .forms import RegistrationForm,LoginForm,ResumeUpload, SearchtitledocumentForm, \
    SearchregionForm, JobTypeFilterForm,CompanyInformation
# Create your views here.
from .models import Jobs, seeker_resume, recruiter,company,user_account






def homepage(request):
    if request.user.is_anonymous:
        return render(request=request, template_name='SEEKJOBSPLATFORM/index.html',
                      context={'jobs': Jobs.objects.all().order_by("-id")[:5],}
                      )
    else:
        candidate = True
        if request.method == 'POST':
            return searchJob(request)
        else:
            print(candidate)
            if recruiter.objects.filter(user_id=request.user.id).exists():
                candidate = False
                print(request.user.username)
            print(candidate)
            return render(request=request, template_name='SEEKJOBSPLATFORM/index.html',
                          context={'jobs': Jobs.objects.all().order_by("-id")[:5], 'candidate': candidate}
                          )

def jobs(request):
    candidate = True
    if recruiter.objects.filter(user_id=request.user.id).exists():
        candidate = False
    jobs_list = Jobs.objects.all().order_by("-id")
    paginator = Paginator(jobs_list, 8)  # Show 25 contacts per page

    page = request.GET.get('page')
    jobs = paginator.get_page(page)

    return render(request=request, template_name='SEEKJOBSPLATFORM/jobs.html', context={'jobs': jobs, 'candidate': candidate})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            sexe = form.cleaned_data['sexe']
            user_address = form.cleaned_data['user_address']
            type = form.cleaned_data['type']

            user = User.objects.create_user(username=username, password=password, email=email,
                                            last_name=last_name, first_name=first_name)
            user = authenticate(username=username, password=password)
            login(request, user)
            if type == 'candidate':
                user_account(user=user, user_address=user_address, gender=sexe).save()
                return jobs(request)
            else:
                recruiter(user=user, user_address=user_address, gender=sexe).save()
                return redirect('SEEKJOBSPLATFORM:complete-company')

    return render(request=request, template_name='SEEKJOBSPLATFORM/signin.html', context={'form': RegistrationForm}
                  )

def loginview(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('SEEKJOBSPLATFORM:jobs')
            else:
                return render(request=request, template_name='SEEKJOBSPLATFORM/login.html', context={'form': LoginForm}
                              )
    return render(request=request, template_name='SEEKJOBSPLATFORM/login.html', context={'form': LoginForm}
                  )

@login_required
def uploadcv(request):
    if not recruiter.objects.filter(user_id=request.user.id).exists():

        if request.method == 'POST':
            form = ResumeUpload(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES['cv']

                file.name = request.user.username + '_resume.' + file.name.split('.')[-1]
                user = user_account.objects.get(user=request.user)

                if seeker_resume.objects.filter(user=user).exists():
                    cv = seeker_resume.objects.get(user=user)
                    print(cv.resume_path)
                    cv.resume_path = file
                    print(cv.resume_path)
                    cv.save()
                else:
                    cv = seeker_resume(resume_path=file, user=user)
                    cv.save()
                return redirect('SEEKJOBSPLATFORM:recommendations')
    else:
        return HttpResponse('you are a recruiter, you can not upload a cv. Please login as job seeker')


def job(request, job_id):
    candidate = True
    if recruiter.objects.filter(user_id=request.user.id).exists():
        candidate = False
    job = Jobs.objects.get(id=job_id)
    job.views = job.views + 1
    job.save()
    t = True
    if recruiter.objects.filter(user_id=request.user.id).exists():
        t = False
    return render(request=request, template_name='SEEKJOBSPLATFORM/job.html',
                  context={'job': job, 'type': t, 'candidate': candidate})

def searchJob(request):
    def search_offres(title=None, region=None, type=None):
        # & ( Q(job_type = type['freelance']) | Q(job_type = type['freelance']) | Q(job_type = type['fullTime']) | Q(job_type = type['partTime']) | Q(job_type = type['temporary']) )
        if title and region:
            return Jobs.objects.filter(Q(job_location__contains=region) & (
                    Q(job_title__contains=title) | Q(job_description__contains=title) | Q(
                job_education__contains=title) | Q(job_skills__contains=title) | Q(
                job_company__company_name__contains=title)))
        elif title:
            print('title')
            return Jobs.objects.filter((Q(job_title__contains=title) | Q(job_description__contains=title) | Q(
                job_education__contains=title) | Q(job_skills__contains=title) | Q(
                job_company__company_name__contains=title)))
        elif region:
            return Jobs.objects.filter(job_location__contains=region)
        else:
            print('None')
            return None

    form_adr = SearchregionForm(request.POST or None)
    form_title = SearchtitledocumentForm(request.POST or None)
    form_type = JobTypeFilterForm(request.POST or None)
    documents = []
    type = None
    if form_type.is_valid():
        type = {
            'freelance': form_type.cleaned_data['freelance'],
            'full': form_type.cleaned_data['fullTime'],
            'internship': form_type.cleaned_data['internship'],
            'part': form_type.cleaned_data['partTime'],
            'temporary': form_type.cleaned_data['temporary'],
        }

    if form_title.is_valid():
        title = form_title.cleaned_data['title']
        if form_adr.is_valid():
            # recherche les deux le titre et l'adresse
            region = form_adr.cleaned_data['region']
            documents = search_offres(title=title, region=region, type=type)
        else:
            # recherche le titre
            documents = search_offres(title=title, type=type)
    elif form_adr.is_valid():
        # recherche l'offre d'emploi de l'adresse
        region = form_adr.cleaned_data['region']
        documents = search_offres(region=region, type=type)


def resume(request, username):
    usr = User.objects.get(username=username)
    user = user_account.objects.get(user=usr)
    cv = seeker_resume.objects.get(user=user)
    print(cv.resume_path)
    return render(request=request, template_name='SEEKJOBSPLATFORM/resume.html', context={'user': user, 'cv': cv})

def logout_view(request):
    logout(request)
    return redirect('SEEKJOBSPLATFORM:homepage')


def companyprofile(request, name):
    candidate = True
    if recruiter.objects.filter(user_id=request.user.id).exists():
        candidate = False
    cmp = company.objects.get(company_name=name)
    jobs = Jobs.objects.filter(job_company=cmp).order_by("-id")[:4]
    return render(request=request, template_name='SEEKJOBSPLATFORM/companyProfile.html',
                  context={'company': cmp, 'jobs': jobs, 'candidate': candidate})


def companies(request):
    candidate = True
    if recruiter.objects.filter(user_id=request.user.id).exists():
        candidate = False
    return render(request=request, template_name='SEEKJOBSPLATFORM/companies.html',
                  context={'companies': company.objects.all(), 'candidate': candidate})

@login_required
def CompanyInfo(request):
    if request.method == 'POST':
        form = CompanyInformation(request.POST)
        user = request.user
        print(user.username)
        if form.is_valid():
            print("company form is valid")
            name = form.cleaned_data['name']
            tagline = form.cleaned_data['tagline']
            website = form.cleaned_data['website']
            linkedin = form.cleaned_data['linkedin']
            # logo = form.cleaned_data['logo']
            description = form.cleaned_data['description']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            location = form.cleaned_data['location']
            cmp = company(company_name=name, company_tagline=tagline, company_email=email, company_linkedin=linkedin,
                          company_website_url=website, profile_description=description,
                          company_phone=phone, company_location=location)
            cmp.save()
            print("company saved")
            rec = recruiter.objects.get(user=request.user)
            rec.recruiter_company = cmp
            rec.save()
            print(rec.recruiter_company.company_name)
            return redirect('SEEKJOBSPLATFORM:dashboard')
        else:
            print("not valid")
    return render(request=request, template_name='SEEKJOBSPLATFORM/company.html', context={'form': CompanyInformation}
                  )
