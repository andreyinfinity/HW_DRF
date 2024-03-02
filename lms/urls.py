from django.urls import path
from rest_framework.routers import DefaultRouter
from lms.apps import LmsConfig
from lms import views

app_name = LmsConfig.name

router = DefaultRouter()
router.register(prefix=r'courses', viewset=views.CourseViewSet, basename='course')

urlpatterns = [
    path('lessons/create/', views.LessonCreate.as_view(), name='lesson-create'),
    path('lessons/', views.LessonList.as_view(), name='lessons'),
    path('lessons/<int:pk>/', views.LessonRetrieve.as_view(), name='lesson-retrieve'),
    path('lessons/<int:pk>/update/', views.LessonUpdate.as_view(), name='lesson-update'),
    path('lessons/<int:pk>/delete/', views.LessonDestroy.as_view(), name='lesson-delete'),
    path('courses/<int:pk>/subscribe/', views.SubscribeAPI.as_view(), name='subscribe'),
] + router.urls
