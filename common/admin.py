class SoftDeletionModelAdminMixin:
    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        qs = self.model.all_objects.all()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs