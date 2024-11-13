from typing import Any
from django.views.generic import TemplateView
from django.db.models import Q
from django.contrib.auth import get_user_model

from mail_center.models import SendingMessage
from our_clients.models import ClientServise
from blog.models import Posts


class MainPageView(TemplateView):
    template_name = 'main_page/main_page.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Main'
        context['catg_selected'] = 1
        context['users'] = (get_user_model().objects
                            .filter(~Q(is_staff=True) &
                                    ~Q(is_superuser=True) &
                                    ~Q(is_active=False))
                            .count())
        context['active_newslatters'] = (SendingMessage.objects
                                         .filter(Q(status='run'))
                                         .count())
        context['wait_newslatters'] = (SendingMessage.objects
                                       .filter(~Q(status='run') &
                                               ~Q(status='end'))
                                       .count())
        context['clients_give_newslatter'] = (ClientServise.objects
                                              .filter(~Q(actual=False))
                                              .count())
        try:
            best_posts = (Posts.objects.filter(is_published=True)
                          .order_by('-views')[:3]
                          .select_related('name_user'))
        except:
            best_posts = (Posts.objects.filter(is_published=True)
                          .select_related('name_user'))
        context['best_posts'] = best_posts
        return context
