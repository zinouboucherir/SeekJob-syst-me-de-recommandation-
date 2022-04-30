from django.contrib import admin

from .models import company, user_account, recruiter, seeker_resume, Jobs, applications

admin.site.register(company)
admin.site.register(user_account)
admin.site.register(recruiter)
admin.site.register(seeker_resume)
admin.site.register(Jobs)
admin.site.register(applications)
