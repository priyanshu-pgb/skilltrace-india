from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile

class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select select-custom'}),
        initial='user'
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control input-custom', 'placeholder': 'name@example.com'})
    )
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control input-custom', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control input-custom', 'placeholder': 'Last Name'})
    )

    consent_given = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_consent_given'}),
        error_messages={'required': 'You must review and agree to the Terms & Conditions and DPDP Act Privacy Policy to create an account.'}
    )
    allow_whatsapp_outreach = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'id_allow_whatsapp_outreach'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control input-custom', 'placeholder': 'Choose a username'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.consent_given = self.cleaned_data.get('consent_given', True)
        from django.utils import timezone
        user.consent_timestamp = timezone.now()
        user.allow_whatsapp_outreach = self.cleaned_data.get('allow_whatsapp_outreach', True)
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control input-custom', 'placeholder': 'Username or Email', 'autocomplete': 'username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control input-custom', 'placeholder': 'Password', 'autocomplete': 'current-password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                # Try finding by email
                try:
                    user_obj = User.objects.get(email__iexact=username)
                    user = authenticate(username=user_obj.username, password=password)
                except (User.DoesNotExist, User.MultipleObjectsReturned):
                    user = None

            if not user:
                raise forms.ValidationError("Invalid username/email or password.")
            if not user.is_active:
                raise forms.ValidationError("This account has been deactivated.")
            cleaned_data['user'] = user
        return cleaned_data


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'location')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control input-custom'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control input-custom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control input-custom'}),
            'phone': forms.TextInput(attrs={'class': 'form-control input-custom', 'placeholder': '+91 9876543210'}),
            'location': forms.TextInput(attrs={'class': 'form-control input-custom', 'placeholder': 'City, State'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('degree', 'institution', 'graduation_year', 'target_role', 'headline', 'experience_summary', 'linkedin_url', 'github_url', 'portfolio_url')
        widgets = {
            'degree': forms.TextInput(attrs={'class': 'form-control input-custom', 'placeholder': 'e.g. B.Tech Computer Science'}),
            'institution': forms.TextInput(attrs={'class': 'form-control input-custom', 'placeholder': 'e.g. National Institute of Technology'}),
            'graduation_year': forms.NumberInput(attrs={'class': 'form-control input-custom', 'placeholder': 'e.g. 2026'}),
            'target_role': forms.TextInput(attrs={'class': 'form-control input-custom', 'placeholder': 'e.g. Data Analyst / Web Developer'}),
            'headline': forms.TextInput(attrs={'class': 'form-control input-custom', 'placeholder': 'e.g. Aspiring Full Stack Engineer passionate about Django'}),
            'experience_summary': forms.Textarea(attrs={'class': 'form-control input-custom', 'rows': 3, 'placeholder': 'Brief summary of internships, projects, or work history'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'form-control input-custom', 'placeholder': 'https://linkedin.com/in/username'}),
            'github_url': forms.URLInput(attrs={'class': 'form-control input-custom', 'placeholder': 'https://github.com/username'}),
            'portfolio_url': forms.URLInput(attrs={'class': 'form-control input-custom', 'placeholder': 'https://portfolio-demo.com'}),
        }
