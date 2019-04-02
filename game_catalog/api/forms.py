from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2",
                  "last_name", "first_name")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        if commit:
            user.save()
        return user
