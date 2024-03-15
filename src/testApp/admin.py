from django.contrib import admin
from .models import Test, Question, Option, TestResult, Response

admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(TestResult)
admin.site.register(Response) 