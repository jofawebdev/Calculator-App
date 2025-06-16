from django.contrib import admin
from .models import Calculation

@admin.register(Calculation)
class CalculationAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Calculation model
    - Displays relevant fields
    - Filters by user and operation
    - Search by numbers and result
    - Read-only timestamp
    """
    list_display = ('user', 'expression', 'result', 'created_at')
    list_filter = ('user', 'operation')
    search_fields = ('num1', 'num2', 'result')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'

    def expression(self, obj):
        """
        Custom column showing the calculation expression
        """
        return f"{obj.num1} {obj.get_operation_symbol()} {obj.num2}"
    expression.short_description = 'Calculation'
