from django.contrib import admin
from .models import Test, Question, Option, TestResult, Response, QuestionImage, OptionImage

admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(TestResult)
admin.site.register(Response)
admin.site.register(QuestionImage)
admin.site.register(OptionImage)