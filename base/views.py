from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, UserUpdateForm, ProfileUpdateForm
from .models import Calculation, Subscription  # Import the Calculation and Subscription model

class CalculatorView(View):
    """
    Class-based view to handle calculator operations.
    GET: Renders calculator template
    POST: Processes calculation, saves to history (authenticated users), and returns result
    """
    template_name = 'base/calculator.html'
    
    # Mapping operations to their mathematical functions
    OPERATION_MAP = {
        'add': lambda x, y: x + y,
        'subtract': lambda x, y: x - y,
        'multiply': lambda x, y: x * y,
        'divide': lambda x, y: x / y if y != 0 else None
    }

    def get(self, request):
        """Render empty calculator form for GET requests"""
        return render(request, self.template_name)

    def post(self, request):
        """
        Process calculation form submission:
        1. Validate input numbers
        2. Validate operation
        3. Perform calculation
        4. Save to database (authenticated users)
        5. Return result or appropriate error
        """
        # Validate input numbers
        try:
            num1 = float(request.POST.get('number_one', '0'))
            num2 = float(request.POST.get('number_two', '0'))
            operation = request.POST.get('operation', '')
        except (TypeError, ValueError):
            return render(request, self.template_name, {
                'error': 'Invalid input: Please enter valid numbers',
                'number_one': request.POST.get('number_one', ''),
                'number_two': request.POST.get('number_two', ''),
                'operation': request.POST.get('operation', '')
            })

        # Validate operation
        if operation not in self.OPERATION_MAP:
            return render(request, self.template_name, {
                'error': 'Invalid operation selected',
                'number_one': num1,
                'number_two': num2,
                'operation': operation
            })

        # Perform calculation
        try:
            result = self.OPERATION_MAP[operation](num1, num2)
            
            # Handle division by zero
            if result is None:
                return render(request, self.template_name, {
                    'error': 'Division by zero is not allowed',
                    'number_one': num1,
                    'number_two': num2,
                    'operation': operation
                })
        except Exception as e:
            return render(request, self.template_name, {
                'error': f'Calculation error: {str(e)}',
                'number_one': num1,
                'number_two': num2,
                'operation': operation
            })

        # Save calculation to database for authenticated users
        if request.user.is_authenticated:
            Calculation.objects.create(
                user=request.user,
                num1=num1,
                num2=num2,
                operation=operation,
                result=result
            )

        # Return successful result
        return render(request, self.template_name, {
            'result': result,
            'operation_symbol': self.get_operation_symbol(operation)
        })

    def get_operation_symbol(self, operation):
        """Return mathematical symbol for given operation name"""
        return {
            'add': '+',
            'subtract': '-',
            'multiply': '*',
            'divide': '÷',
        }.get(operation, '')


class HistoryView(LoginRequiredMixin, ListView):
    """
    View to display calculation history for authenticated users.
    Requires login - redirects to login page if not authenticated.
    Displays paginated list of user's calculations (most recent first).
    """
    model = Calculation
    template_name = 'base/history.html'
    context_object_name = 'calculations'  # Template variable name
    paginate_by = 10  # Show 10 calculations per page

    def get_queryset(self):
        """
        Return filtered queryset:
        - Only current user's calculations
        - Ordered by most recent first
        """
        return Calculation.objects.filter(
            user=self.request.user
        ).order_by('-created_at')


class RegisterView(View):
    """
    Handles user registration:
    GET: Displays registration form
    POST: Processes registration data and creates new user
    """
    template_name = 'registration/register.html'
    form_class = RegisterForm

    def get(self, request):
        """Redirect authenticated users away from registration page"""
        if request.user.is_authenticated:
            return redirect('calculator')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        """Validate form and create new user account"""
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('calculator')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    """
    Handles user authentication:
    GET: Displays login form
    POST: Validates credentials and logs in user
    """
    template_name = 'registration/login.html'
    form_class = LoginForm

    def get(self, request):
        """Redirect authenticated users away from login page"""
        if request.user.is_authenticated:
            return redirect('calculator')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        """Authenticate user and create session"""
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('calculator')
        return render(request, self.template_name, {'form': form})


def logout_view(request):
    """
    Handles user logout:
    1. Ends user session
    2. Displays logout message
    3. Redirects to calculator
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('calculator')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)


        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'registration/profile.html', context)


# Footer Subscribe Form View
def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Basic Validation
        if email and '@' in email:
            # Save to database
            Subscription.objects.get_or_create(email=email)
            messages.success(request, 'Thanks for subscribing!')
        else:
            messages.error(request, 'Please enter a valid email address.')
    return redirect('calculator')