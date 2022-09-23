from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'adminsite'
urlpatterns = [
    # Path for Function based Views

    # path('', views.popular_course_list, name='popular_course_list'),
    # path('course/<int:course_id>/enroll/', views.enroll, name="enroll"),
    # path('course/<int:course_id>/', views.course_details, name='course_details'),

    # pathe for class based views
    path(route='', view=views.CourseListView.as_view(), name='popular_course_list'),
    path(route='course/<int:pk>/enroll/', view=views.EnrollView.as_view(), name='enroll'),
    path(route='course/<int:pk>/', view=views.CourseDetailsView.as_view(), name='course_details'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
 + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

