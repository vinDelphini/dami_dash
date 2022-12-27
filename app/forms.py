import pytz
from allauth.account.forms import SetPasswordForm
from django import forms
from django.contrib.auth import get_user_model
from invitations.utils import get_invitation_model
from app.models import Profile

User = get_user_model()


COMMON_TZ = [
    "US/Alaska",
    "US/Arizona",
    "US/Central",
    "US/Eastern",
    "US/Hawaii",
    "US/Mountain",
    "US/Pacific",
    "Canada/Atlantic",
    "Canada/Central",
    "Canada/Eastern",
    "Canada/Mountain",
    "Canada/Newfoundland",
    "Canada/Pacific",
    "",
]

TIMEZONE_CHOICES = tuple(
    zip([*COMMON_TZ, *pytz.common_timezones], [*COMMON_TZ, *pytz.common_timezones])
)


class CurrentProfileForm(forms.ModelForm):
    """A limited form for users to edit info on themselves."""

    time_zone = forms.ChoiceField(label="Timezone", choices=TIMEZONE_CHOICES)

    class Meta:
        model = Profile
        fields = [
            "time_zone",
        ]


class CurrentUserForm(forms.ModelForm):
    """A limited form for users to edit info on themselves."""

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
        ]


class UserForm(forms.ModelForm):
    """
    Used inside the CompanyUserForm and inherited and customized by
    AdminUserCreateForm and AdminUserEditForm.
    """

    class Meta:
        model = get_user_model()
        fields = ("email", "username", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].required = True

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not self.instance.pk and email:
            Invitation = get_invitation_model()
            if Invitation.objects.filter(email=email).exists():
                raise forms.ValidationError(
                    "An invitation has already been sent to this email."
                )
        return email


class AdminUserCreateForm(UserForm):
    """For admins to create users and associate them to one company."""

    time_zone = forms.ChoiceField(choices=TIMEZONE_CHOICES)

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        # Set the user to inactive so they can't log in until they accept
        # their invite link and set a password.
        user.is_active = False
        user.set_unusable_password()
        user.save()
        time_zone = self.cleaned_data.get("time_zone")
        if time_zone:
            Profile.objects.update_or_create(
                user=user, defaults=dict(time_zone=time_zone)
            )
        return user


class AdminUserEditForm(forms.ModelForm):
    """For admins to edit users."""

    time_zone = forms.ChoiceField(choices=TIMEZONE_CHOICES)
    resend_invite = forms.BooleanField(
        label="Resend Invitation to Sign Up",
        help_text=(
            "When checked the user will receive another email "
            "to complete the sign up process."
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields["time_zone"].initial = self.instance.profile.time_zone
            self.fields["resend_invite"].initial = False

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username"]


class DashboardSignupForm(SetPasswordForm):
    email = forms.CharField(disabled=True)

    def __init__(self, *args, **kwargs):
        super(DashboardSignupForm, self).__init__(*args, **kwargs)
        self.fields["email"].initial = self.user.email

    def save(self, request):
        self.user.set_password(self.cleaned_data.get("password1"))
        self.user.is_active = True
        self.user.save()
        return self.user
