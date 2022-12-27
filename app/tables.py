import django_tables2 as tables
from django.contrib.auth import get_user_model
from django_tables2 import A

User = get_user_model()


class AllUsersTable(tables.Table):
    name = tables.LinkColumn(
        "admin-profile-detail",
        text=lambda record: f"{record.first_name} {record.last_name}",
        args=[A("profile__pk")],
        order_by="first_name",
    )

    actions = tables.TemplateColumn(
        template_name="profiles/user_actions_column_for_admins.html",
        orderable=False,
    )

    class Meta:
        model = User
        template_name = "common/tables/base_table.html"
        fields = ("is_superuser", "is_active", "last_login")
        sequence = ("name",)
        empty_text = "No users, how did you get here?"
