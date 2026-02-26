from django import forms
from django.contrib.auth import authenticate, get_user_model, password_validation

User = get_user_model()


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "autofocus": True,
                "placeholder": "Enter your username",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your password",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError("Invalid username or password.")

        return cleaned_data

    def get_user(self):
        return self.user_cache


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Choose a strong password",
            }
        ),
        help_text=password_validation.password_validators_help_text_html(),
    )

    class Meta:
        model = User
        fields = ("first_name", "username")
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "autofocus": True,
                    "placeholder": "Your first name",
                }
            ),
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Choose a username",
                }
            ),
        }

    def clean_password(self):
        password = self.cleaned_data.get("password") or ""

        # Enforce Django's configured password validators (length, common passwords, etc.).
        password_validation.validate_password(password)

        # Simple extra complexity rule: require at least one letter and one digit.
        has_letter = any(c.isalpha() for c in password)
        has_digit = any(c.isdigit() for c in password)
        if not (has_letter and has_digit):
            raise forms.ValidationError(
                "Password must contain at least one letter and one digit."
            )

        return password

    def clean_username(self):
        username = self.cleaned_data.get("username") or ""
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        user.set_password(password)
        if commit:
            user.save()
        return user

