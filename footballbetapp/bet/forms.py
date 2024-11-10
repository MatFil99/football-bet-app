from django.contrib.auth.forms import BaseUserCreationForm
from django.contrib.auth import get_user_model 

User = get_user_model()

class CustomUserCreationForm(BaseUserCreationForm):
    pass

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name",)