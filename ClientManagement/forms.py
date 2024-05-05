from django import forms
from ClientManagement.models import Client


class ClientUpdateForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['client_name', 'client_number', 'client_address', 'active_plan',
                  'plan_start_date', 'plan_end_date', 'total_amount', 'amount_paid']
