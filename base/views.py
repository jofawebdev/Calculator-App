from django.shortcuts import render
from django.views import View

class CalculatorView(View):
    """
    A class-based view to handle calculator operations.

    GET: Renders the calculator template
    POST: Processes calculation and returns result
    """

    template_name = 'base/calculator.html'

    # Mapping of operation names to their respective functions
    OPERATION_MAP = {
        'add': lambda x, y: x + y,
        'subtract': lambda x, y: x - y,
        'multiply': lambda x, y: x * y,
        'divide': lambda x, y: x / y if y != 0 else None
    }

    def get(self, request):
        """
        Handle GET requests - render an empty calculator form
        """
        return render(request, self.template_name)

    def post(self, request):
        """
        Handle POST requests - process calculation and return result or error
        """
        # Extract and validate input parameters
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

        # Validate operation type
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
            if result is None:
                # Handle division by zero
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

        # On success, clear form inputs and show result
        return render(request, self.template_name, {
            'result': result,
            'operation_symbol': self.get_operation_symbol(operation)
        })

    def get_operation_symbol(self, operation):
        """
        Helper method to return the math symbol corresponding to an operation
        """
        return {
            'add': '+',
            'subtract': '-',
            'multiply': '*',
            'divide': '÷',
        }.get(operation, '')