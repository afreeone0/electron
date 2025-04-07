import re
from django import forms


class CreateOrderForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    requires_delivery = forms.ChoiceField(
        choices=[
            ("0", False),
            ("1", True),
        ],
    )
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(
        choices=[
            ("0", 'False'),
            ("1", 'True'),
        ],
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if len(phone_number) > 25:
            raise forms.ValidationError("Неверный формат номера")

        for x in '() +-':
            phone_number = phone_number.replace(x, '')

        regex = r'^\d{11}$'
        pattern = re.compile(regex)
        if not pattern.match(phone_number):
            raise forms.ValidationError("Неверный формат номера")

        return phone_number
