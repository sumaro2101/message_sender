from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth import mixins
from .models import SendingMessage
# Create your views here.

    
class ListSendMessages(mixins.LoginRequiredMixin, ListView):
    model = SendingMessage
    context_object_name = 'messages'
    paginate_by = 4
    template_name = 'mail_center/mail_list.html'
    
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('message').filter(message__employee=self.request.user)
        return queryset
        
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Send'
        context['catg_selected'] = 5
        return context
    