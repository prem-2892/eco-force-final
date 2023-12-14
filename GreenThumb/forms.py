from django.forms import ModelForm , TextInput, NumberInput, EmailInput
from .models import Company,Feedback
from crispy_forms.layout import Submit, Layout, Div
from crispy_forms.helper import FormHelper
class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'  # You can specify which fields you want to include in the form

    def __init__(self, *args, **kwargs):
            super(CompanyForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.add_input(Submit("submit", "Submit"))

            self.helper.layout = Layout(
                Div(
                    "company_name",
                    "Email_ID",
                    "postal_code",
                    css_class="flex flex-col md:flex-row md:justify-between md:items-end absolute-white",
                ),
                Div(
                    "employee_count",
                    "annual_electricity_budget",
                    "company_sector",
                    css_class="flex flex-col md:flex-row md:justify-between md:items-end absolute-white",
                ),
                Div(
                    "annual_natural_gas_budget",
                    css_class="flex gap-4 items-end absolute-white",
                ),
                # Add more Div elements as needed
            )
class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'description']