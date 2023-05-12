import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data


class CartAddBookForm(forms.Form):
    """Form to add a book to the cart."""

    # The quantity field is always 1 for this form, as only one book can be added to the cart at a time
    quantity = forms.TypedChoiceField(choices=((1, 1),), coerce=int, widget=forms.HiddenInput)
    
    def __init__(self, *args, **kwargs):
        self.book = kwargs.pop('book', None)
        super().__init__(*args, **kwargs)

    def clean_quantity(self):
        """Return the only allowed value for quantity: 1."""
        return 1

    def get_book(self):
        """Return the book associated with this form."""
        return self.book