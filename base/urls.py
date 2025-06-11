from django.urls import path
from .views import CalculatorView  # import the class based-view

urlpatterns = [
    # Single endpoint handling both form display (GET) and calculation (POST)
    path('', CalculatorView.as_view(), name='calculator'),
]