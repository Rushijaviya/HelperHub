from django.contrib import admin
from django.contrib.auth.models import User
from .models import userInfo, Doctor, Tutor, Logistic, Service_Provider, Other, Message

admin.site.register(userInfo)
admin.site.register(Doctor)
admin.site.register(Tutor)
admin.site.register(Logistic)
admin.site.register(Service_Provider)
admin.site.register(Other)
admin.site.register(Message)
