from datetime import datetime
from django import forms
from products.models import Product, Category


class DatePickerInput(forms.widgets.DateInput):
    input_type = 'date'

class TimePickerInput(forms.DateTimeInput):
    input_type = 'time'

class FromToForm(forms.Form):
    from_date = forms.DateField(widget=DatePickerInput())
    from_time = forms.TimeField(widget=TimePickerInput())
    to_date = forms.DateField(widget=DatePickerInput(), initial=datetime.today())
    to_time = forms.TimeField(widget=TimePickerInput(), initial=datetime.today().strftime('%H:%M'))

    def get_from_datetime(self):
        return datetime.combine(self.cleaned_data['from_date'], self.cleaned_data['from_time'])

    def get_to_datetime(self):
        return datetime.combine(self.cleaned_data['to_date'], self.cleaned_data['to_time'])

class SalesByCategoryForm(FromToForm):
    category = forms.ModelChoiceField(queryset = Category.objects.all())

class SalesByProductForm(FromToForm):
    product = forms.ModelChoiceField(queryset = Product.objects.all())

class SalesByOrderForm(FromToForm):
    category = forms.ModelChoiceField(queryset = Category.objects.all(), required=False)
    product = forms.ModelChoiceField(queryset = Product.objects.all(), required=False)


