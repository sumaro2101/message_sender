from typing import Any
from django.contrib.auth import mixins
from mail_center.cache import get_or_set_cache


class OwnerOrStaffPermissionMixin(mixins.UserPassesTestMixin):

    def test_func(self) -> bool | None:
        self.object = self.get_object()
        return (self.request.user.is_superuser or
                self.request.user == self.object.owner_send)


class CheckModeratorMixin:
    """Миксин которой проверяет являтся ли текущий пользователем модератором
    """
    def dispatch(self, request, *args: Any, **kwargs: Any):
        self.moderator = get_or_set_cache(
            self.request.user.groups,
            slug='moderator',
            type_field='name',
            )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['moderator'] = self.moderator
        return context
