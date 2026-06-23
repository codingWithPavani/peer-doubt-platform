from django.contrib import admin

# Register your models here.


# qa/admin.py

from django.contrib import admin
from .models import Question, Answer

admin.site.register(Question)
admin.site.register(Answer)
