from django.contrib.auth import mixins


class RequiredNotAuthenticatedMixin(mixins.UserPassesTestMixin):

    def test_func(self) -> bool | None:
        return (not self.request.user.is_authenticated or
                self.request.user.is_superuser or
                self.request.user.is_staff)
