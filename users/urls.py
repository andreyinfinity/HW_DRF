from django.urls import path
from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path('register/', views.UserRegister.as_view(), name='user-register'),
    path('<int:pk>/update/', views.UserUpdate.as_view(), name='user-update'),
    path('<int:pk>/', views.UserRetrieve.as_view(), name='user-retrieve'),
    path('payments/', views.PaymentList.as_view(), name='payments'),
]
