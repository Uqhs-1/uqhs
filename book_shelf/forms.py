from django import forms
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import Book, Author, BookInstance
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
    
class BookRenew(forms.Form):
    renewal_date = forms.CharField(max_length=5, help_text="Just type 'renew'")
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        return data
    
class Author_form(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('first_name', 'last_name', 'date_of_birth', 'date_of_death',)
    
class Genre_form(forms.Form):
    name = forms.CharField(max_length=100, help_text="Just type-in the name.")
    def clean_renewal_date(self):
        data = self.cleaned_data['name']
        return data
    
class Book_form(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'genre', 'summary', 'isbn', 'language', 'no_of_copy',)
        
class BookInstanceForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ('imprint', 'status',)
    #name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Book Imprint here'}))
    #status = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter Book Status('Available') here or leave blanck for book on Maintenance"}))

