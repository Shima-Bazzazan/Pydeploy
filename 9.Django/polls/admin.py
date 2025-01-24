from django.contrib import admin
from .models import Question, Choice
import jdatetime

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text", "get_jalali_pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]

    def get_jalali_pub_date(self, obj):
        jalali_date = jdatetime.datetime.fromgregorian(datetime=obj.pub_date)
        return jalali_date.strftime("%Y/%m/%d")

    get_jalali_pub_date.short_description = "تاریخ انتشار (شمسی)"

admin.site.register(Question, QuestionAdmin)
