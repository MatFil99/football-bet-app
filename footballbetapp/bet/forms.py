from django.contrib.auth.forms import BaseUserCreationForm
from django.contrib.auth import get_user_model 
from django.conf import settings
from django import forms

from .models import *
from .services import send_contact_email


User = get_user_model()

class CustomUserCreationForm(BaseUserCreationForm):
    pass

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name",)


class StandingsForm(forms.Form):
    """Form definition for TeamsView."""
    league = forms.CharField(max_length=20)
    season = forms.CharField(max_length=9)
    
class MatchesForm(forms.Form):
    """Form definition for MatchesView"""
    league = forms.CharField(max_length=20)
    season = forms.CharField(max_length=9)
    matchday = forms.IntegerField(min_value=1)

class MatchCommentForm(forms.Form):
    """Form definition for MatchCommentView"""
    # author = forms.IntegerField()
    match_id = forms.IntegerField()
    text = forms.Textarea()

class MatchPredictionForm(forms.Form):
    """Form definition for """
    # match_id = forms.IntegerField()
    # user_id = forms.IntegerField()
    home_score = forms.IntegerField()
    away_score = forms.IntegerField()

    def is_valid(self):
        home_score = self.data['home_score']
        away_score = self.data['away_score']
        valid = (home_score is not None and away_score is not None) \
                or (home_score is None and away_score is None)
        return valid
    
class ContactForm(forms.Form):
    """Form definition for contact"""
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    inquiry = forms.CharField(max_length=70)
    message = forms.CharField(widget=forms.Textarea)

    def get_info(self):
        """
        Method that returns formatted information
        :return: subject, msg
        """
        # Cleaned data
        cl_data = super().clean()

        name = cl_data.get('name').strip()
        from_email = cl_data.get('email')
        subject = cl_data.get('inquiry')

        msg = f'{name} with email {from_email} said:'
        msg += f'\n"{subject}"\n\n'
        msg += cl_data.get('message')

        return subject, msg

    def send(self):
        subject, msg = self.get_info()
        send_contact_email(
            subject=subject,
            message=msg,
            recipient_list=[settings.EMAIL_HOST_USER]
        )
