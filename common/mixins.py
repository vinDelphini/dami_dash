from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View


class SuperUserRequiredMixin(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser
