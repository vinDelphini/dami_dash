from django.shortcuts import render

# Create your views here.
from allauth.account.views import SignupView
from common.mixins import SuperUserRequiredMixin
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django_tables2 import SingleTableView
from invitations.utils import get_invitation_model
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    RedirectView,
    UpdateView,
)
from app.forms import (
    AdminUserCreateForm,
    AdminUserEditForm,
    CurrentProfileForm,
    CurrentUserForm,
    DashboardSignupForm,
)
from app.models import Profile
from app.tables import AllUsersTable

User = get_user_model()


class HomeRedirect(LoginRequiredMixin, RedirectView):
    """
    Redirect user based on who they are. If they are a Superuser
    redirect them to the company list. If they are a client, redirect them
    to the dashboard.
    """

    permanent = False
    query_string = False

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return reverse_lazy("all-users-list")


class CurrentProfileDetailView(LoginRequiredMixin, DetailView):
    """Allows a user to view their profile"""

    # Not sure if this view is needed (yet) but adding it
    model = Profile
    http_method_names = ["get"]
    queryset = Profile.objects.all()
    context_object_name = "profile"
    template_name = "profiles/profile_detail.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

'''    def get_context_data(self, **kwargs):
        profile = self.get_object()
        context = super().get_context_data(**kwargs)
        company_users = CompanyUser.objects.filter(user=profile.user).all()
        context["companies"] = [company_user.company for company_user in company_users]
        return context'''


class CurrentProfileUpdateView(LoginRequiredMixin, DetailView):
    """Allows a user to edit their profile"""

    model = Profile
    http_method_names = ["get", "post"]
    queryset = Profile.objects.all()
    context_object_name = "profile"
    template_name = "profiles/profile_update_contact.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user=self.request.user)

    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        context = {
            "profile": profile,
            "profile_form": CurrentProfileForm(instance=profile),
            "user_form": CurrentUserForm(instance=request.user),
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        profile = self.get_object()
        profile_form = CurrentProfileForm(request.POST, instance=profile)
        user_form = CurrentUserForm(request.POST, instance=request.user)

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, "Your contact information has been updated.")
            return redirect("current-profile-detail")
        return self.render_to_response(
            {"profile": profile, "profile_form": profile_form, "user_form": user_form}
        )


class ProfileDetailView(SuperUserRequiredMixin, DetailView):
    """Allows admins to view users profiles"""

    model = Profile
    http_method_names = ["get"]
    context_object_name = "profile"
    template_name = "profiles/admin_profile_detail.html"

'''    def get_context_data(self, **kwargs):
        profile = self.get_object()
        context = super().get_context_data(**kwargs)
        users = User.objects.filter(user=profile.user).all()
        context["users_"] = [user for user in users]
        return context'''

'''    def get_context_data(self, **kwargs):
        profile = self.get_object()
        context = super().get_context_data(**kwargs)
        company_users = CompanyUser.objects.filter(user=profile.user).all()
        context["companies"] = [company_user.company for company_user in company_users]
        return context'''


class UserCreateView(SuperUserRequiredMixin, CreateView):
    """Allows admins to create new Users with a Profile and CompanyUser"""

    model = User
    form_class = AdminUserCreateForm
    http_method_names = ["get", "post"]
    template_name = "profiles/admin_user_create_form.html"
    context_object_name = "user"
    extra_context = {"heading": "Create New Profile"}

    def form_valid(self, form):
        """Save the form and send an invite to the User's email for
        them to sign up."""
        self.object = form.save()
        Invitation = get_invitation_model()
        invite = Invitation.create(self.object.email, inviter=self.request.user)
        invite.send_invitation(self.request, dashboard_name=settings.SITE_NAME)
        messages.success(
            self.request,
            f"Success! A user has been created and an invite link has been emailed to "
            f"{self.object.email} to complete sign up.",
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("admin-profile-detail", args=[self.object.profile.pk])


class UserUpdateView(SuperUserRequiredMixin, UpdateView):
    """Allows admins to edit users and their associated Profile and CompanyUser"""

    model = User
    form_class = AdminUserEditForm
    http_method_names = ["get", "post"]
    template_name = "profiles/admin_user_form.html"
    context_object_name = "user"
    extra_context = {"heading": "Edit Profile"}

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        user_form = form.save(commit=False)
        time_zone = form.cleaned_data.get("time_zone")
        resend_invite = form.cleaned_data.get("resend_invite")
        user_form.save()
        # save the timezone to the user's profile
        user_form.profile.time_zone = time_zone
        user_form.profile.save()
        # save associated companies

        # check if invitation to signup needs to be
        # resent to user.
        profile_user_email = getattr(user_form, "email")
        if resend_invite and profile_user_email:
            Invitation = get_invitation_model()
            try:
                prior_invitation = Invitation.objects.get(email=profile_user_email)
                if not prior_invitation.accepted:
                    prior_invitation.delete()
                    new_invite = Invitation.create(
                        self.object.email, inviter=self.request.user
                    )
                    new_invite.send_invitation(
                        self.request, dashboard_name=settings.SITE_NAME
                    )
                    messages.success(
                        self.request,
                        "Success! An invite link has been emailed to "
                        f"{self.object.email} to complete sign up.",
                    )
                else:
                    messages.error(
                        self.request,
                        f"An invitation to {self.object.email} has already "
                        "been accepted.",
                    )
            except Invitation.DoesNotExist:
                invite = Invitation.create(self.object.email, inviter=self.request.user)
                invite.send_invitation(self.request, dashboard_name=settings.SITE_NAME)
                messages.success(
                    self.request,
                    "Success! An invite link has been emailed to "
                    f"{self.object.email} to complete sign up.",
                )

        messages.success(
            self.request,
            "Profile has been saved.",
        )

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form)
        )

    def get_success_url(self):
        return reverse_lazy("admin-profile-detail", args=[self.object.profile.pk])


class InvitedUserSignup(SignupView):
    form_class = DashboardSignupForm
    template_name = "account/account_signup.html"

    def get_user_from_email(self):
        email = self.request.session.get("account_verified_email")
        if email:
            Invitation = get_invitation_model()
            try:
                Invitation.objects.get(email=email)
                user = User.objects.get(email=email, is_active=False)
            except (Invitation.DoesNotExist, User.DoesNotExist):
                # django-invitations handles redirects before getting here, so the user
                # should already have been redirected to the signup url with a message.
                pass
            else:
                return user

    def get_form_kwargs(self):
        """Get the user from the email stashed by django-invitations and
        set it in the form."""
        kwargs = super().get_form_kwargs()
        user = self.get_user_from_email()
        kwargs.update({"user": user})
        return kwargs


class AllUsersList(SuperUserRequiredMixin, SingleTableView):
    """A view for superusers to list company admins"""

    table_class = AllUsersTable
    model = User
    template_name = "profiles/all_users_list.html"
    table_pagination = {"per_page": 10}


'''class Dashboard(LoginRequiredMixin, ListView):
    template_name = "dashboard/dashboard.html"'''
    
'''    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return reverse_lazy("dash")'''


def Dashboard(request):
    return render(request, "dashboard/dashboard.html")
