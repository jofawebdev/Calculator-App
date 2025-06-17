from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import CalculatorView, RegisterView, LoginView, logout_view, HistoryView, profile, subscribe  # import the class based-view

urlpatterns = [
    # Home calculator view: Single endpoint handling both form display (GET) and calculation (POST)
    path('', CalculatorView.as_view(), name='calculator'),

    # View for user's calculation history 
    path('history/', HistoryView.as_view(), name='history'),

    # View for user profile
    path('profile/', profile, name='profile'),
    
    # User Authentication URLS (Login, Register, Logout, Password Reset)
    path('register/', RegisterView.as_view(), name='register'), # User Registration
    path('login/', LoginView.as_view(), name='login'), # User Login
    path('logout/', logout_view, name='logout'), # User logout
    
    # Password Reset URLS (customized for this project under)
    # Step 1: Request reset link
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),

    # Step 2: Confirmation that reset email has been sent
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),

    # Step 3: Link from email leads here, where the user sets a new password
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),

    # Step 4: Completion page after successful reset
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    
    # Newsletter or service subscription endpoint
    path('subscribe/', subscribe, name='subscribe')
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)