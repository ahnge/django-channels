from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm 


class CreateRoomForm(forms.Form):
    room_name = forms.CharField(max_length=255)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def clean_first_name(self):
        """Make first name to be required"""
        first_name = self.cleaned_data.get("first_name")
        if not first_name:
            raise ValidationError("This field is required.", code="no_first_name")
        return first_name

    def clean_last_name(self):
        """Make last name to be required"""
        last_name = self.cleaned_data.get("last_name")
        if not last_name:
            raise ValidationError("This field is required.", code="no_last_name")
        return last_name

    def clean_email(self):
        """Reject emails that already exists and reject if email is not specified."""
        email = self.cleaned_data.get("email")
        if not email:
            raise ValidationError("Email field is required.", code="no_email")
        elif email and self._meta.model.objects.filter(email__iexact=email).exists():
            self._update_errors(
                ValidationError(
                    {
                        "email": self.instance.unique_error_message(
                            self._meta.model, ["email"]
                        )
                    }
                )
            )
        else:
            return email
