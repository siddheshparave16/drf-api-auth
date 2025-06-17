from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    """
    Extends Django's default UserCreationForm to:
    - Add mandatory email field
    - Save email to user model during registration
    - Used for sending welcome emails post-registration
    """
    email = forms.EmailField(
        required=True,
        help_text="Required. Please provide a valid email address."
    )

    class Meta:
        """
        Configuration for the form:
        - Uses Django's built-in User model
        - Fields displayed in order: username → email → password1 → password2
        """
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        """
        Overrides the default save method to:
        1. Get the unsaved user instance with email from cleaned_data
        2. Only save to database if commit=True
        3. Returns the user instance (saved or unsaved)
        """
        user = super().save(commit=False)  # Get user instance without saving
        user.email = self.cleaned_data['email']  # Assign validated email
        
        if commit:
            user.save()  # Persist to database if committing
        
        return user  # Return user object for further processing