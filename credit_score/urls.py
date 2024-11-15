from django.urls import path
from .views import sign_up, save_user, login_page, logged, logout, home, get_questions, save_response, calculate_user_score

urlpatterns = [
    path('signup/', sign_up, name='signup'),
    path('save_user/', save_user, name='saveuser'),
    path('', login_page, name='login_page'),
    path('logged/', logged, name='logged'),
    path('logout/', logout, name='logout'),
    path('home/', home, name='home'),
    path('api/questions/', get_questions, name='get_questions'),
    path('api/save_response/', save_response, name='save_response'),
    path('calculate_user_score/', calculate_user_score, name='calculate_user_score'),
]