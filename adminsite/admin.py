from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner


class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 5


# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('name', 'image', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['name', 'description']


class LessonAdmin(admin.ModelAdmin):
    list_display = ['title']


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)

class InstructorAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_time', 'total_learners')
    list_filter = ['total_learners']

    
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Learner)
