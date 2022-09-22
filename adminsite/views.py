from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from .models import Course, Lesson, Enrollment
from django.urls import reverse
from django.views import generic
from django.http import Http404

# Create your views here.
def popular_course_list(request):
    context = {}
    # If the request method is GET
    if request.method == 'GET':
        # Using the objects model manage to read all course list
        # and sort them by total_enrollment descending
        course_list = Course.objects.order_by('-total_enrollment')[:10]
        # Appen the course list as an entry of context dict
        context['course_list'] = course_list
        return render(request, 'adminsite/course_list.html', context)


def enroll(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        course.total_enrollment += 1
        course.save()
        return HttpResponseRedirect(reverse('adminsite:popular_course_list'))