from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from .models import Course, Lesson, Enrollment
from django.urls import reverse
from django.views import generic, View
from django.http import Http404



# #Function based views

# #Function-based course list view
# def popular_course_list(request):
#     context = {}
#     # If the request method is GET
#     if request.method == 'GET':
#         # Using the objects model manage to read all course list
#         # and sort them by total_enrollment descending
#         course_list = Course.objects.order_by('-total_enrollment')[:10]
#         # Appen the course list as an entry of context dict
#         context['course_list'] = course_list
#         return render(request, 'adminsite/course_list.html', context)


# def enroll(request, course_id):
#     if request.method == 'POST':
#         course = get_object_or_404(Course, pk=course_id)
#         course.total_enrollment += 1
#         course.save()
#         return HttpResponseRedirect(reverse('adminsite:course_details', args=(course.id, )))


# #Function-based course list view
# def course_details(request, course_id):
#     context = {}
#     if request.method == 'GET':
#         try:
#             course = Course.objects.get(pk=course_id)
#             context['course'] = course
#             # Use render() method to generate HTML page by combining
#             # template and context
#             return render(request, 'adminsite/course_detail.html', context)
#         except Course.DoesNotExist:
#             # If course does not exist, throw a Http404 error
#             raise Http404("No course matches the given id.")



# class-based views
class CourseListView(View):
    def get(self, request):
        context = {}
        course_list = Course.objects.order_by('-total_enrolled')[:10]
        context = {
            'course_list': course_list
        }
        return render(request, 'adminsite/course_list.html', context)


class EnrollView(View):
    def post(self, request, *args, **kwargs):
        course_id = kwargs.get('pk')
        course = get_object_or_404(Course, pk=course_id)
        course.total_enrollment += 1
        course.save()
        return HttpResponseRedirect(reverse('adminsite:course_details', args=(course.id, )))

class CourseDetailsView(View):
    def get(self, request, *args, **kwags):
        context = {}
        course_id = kwags.get('pk')
        try:
            course = Course.objects.get(pk=course_id)
            context = {
                'course': course
            }
            return render(request, 'adminsite/course_detail.html', context)
        except Course.DoesNotExist:
            raise Http404('The course with given Id is not available!!')
