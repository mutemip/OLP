from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Course, Lesson, Enrollment
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404
from django.urls import reverse
from django.views import generic, View
from collections import defaultdict
from django.contrib.auth import login, logout, authenticate
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


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


#-------------------------------------------------------------------------------------------
# class-based views
# class CourseListView(View):
#     def get(self, request):
#         context = {}
#         course_list = Course.objects.order_by('-total_enrolled')[:10]
#         context = {
#             'course_list': course_list
#         }
#         return render(request, 'adminsite/course_list.html', context)


# class EnrollView(View):
#     def post(self, request, *args, **kwargs):
#         course_id = kwargs.get('pk')
#         course = get_object_or_404(Course, pk=course_id)
#         course.total_enrollment += 1
#         course.save()
#         return HttpResponseRedirect(reverse('adminsite:course_details', args=(course.id, )))

# class CourseDetailsView(View):
#     def get(self, request, *args, **kwags):
#         context = {}
#         course_id = kwags.get('pk')
#         try:
#             course = Course.objects.get(pk=course_id)
#             context = {
#                 'course': course
#             }
#             return render(request, 'adminsite/course_detail.html', context)
#         except Course.DoesNotExist:
#             raise Http404('The course with given Id is not available!!')


#---------------------------------------------------------------------------------------------
# Generic Built-in Views
class CourseListView(generic.ListView):
    template_name = 'adminsite/course_list.html'
    context_object_name = 'course_list'
    def get_queryset(self):
        courses = Course.objects.order_by('-total_enrollment')[:10]
        return courses

class EnrollView(View):
    def post(self, request, *args, **kwargs):
        course_id = kwargs.get('pk')
        course = get_object_or_404(Course, pk=course_id)
        course.total_enrollment += 1
        course.save()
        return HttpResponseRedirect(reverse('adminsite:course_details', args=(course.id, )))


class CourseDetailsView(generic.DetailView):
    model = Course
    template_name = 'adminsite/course_detail.html'


def logout_request(request):
    print("Log out the user '{}'".format(request.user.username))
    logout(request)
    return redirect('adminsite:popular_course_list')
    
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('adminsite:popular_course_list')
        else:
            # If not, return to login page again
            return render(request, 'adminsite/user_login.html', context)
    else:
        return render(request, 'adminsite/user_login.html', context)

def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'adminsite/user_registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("adminsite:popular_course_list")
        else:
            return render(request, 'adminsite/user_registration.html', context)