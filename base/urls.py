from django.urls import path
from .views import CalculatorView, RegisterView, LoginView, logout_view, HistoryView  # import the class based-view

urlpatterns = [
    # Single endpoint handling both form display (GET) and calculation (POST)
    path('', CalculatorView.as_view(), name='calculator'),

    # History URL
    path('history/', HistoryView.as_view(), name='history'),
    
    # User Authentication URLS (Login, Register, Logout)
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view,name='logout')
]