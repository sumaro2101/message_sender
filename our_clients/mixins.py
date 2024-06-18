from django.contrib.auth import mixins

class OwnerOrStaffPermissionMixin(mixins.UserPassesTestMixin):
    
    def test_func(self) -> bool | None:
        self.object = self.get_object()
        return self.request.user.is_staff or\
            self.request.user.is_superuser or\
                self.request.user == self.object.employee
                