from django.urls import path
from shop import views 
from .views import SignUpView, ProfileEditView, ProfilePageView

urlpatterns = [
    path('create/', SignUpView.as_view(), name='signup'),
    path('edit_profile/<int:pk>/', ProfileEditView.as_view(), name='edit_profile'),
    path('profile/<int:pk>/', ProfilePageView.as_view(), name='show_profile'),
]
