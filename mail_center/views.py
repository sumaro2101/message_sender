from typing import Any
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth import mixins


from .models import SendingMessage
from .forms import FormSendMesssage
from .services import check_message, create_task_interval
from mess.models import MessageInfo
from mail_center.tasks import send
# Create your views here.

    
class ListSendMessages(mixins.LoginRequiredMixin, ListView):
    model = SendingMessage
    context_object_name = 'messages'
    paginate_by = 4
    template_name = 'mail_center/mail_list.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('message').filter(message__employee=self.request.user).order_by('-pk')
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Send'
        context['catg_selected'] = 5
        return context
    
    
class CreateSend(mixins.LoginRequiredMixin, CreateView):
    model = SendingMessage
    form_class = FormSendMesssage
    success_url = reverse_lazy('mail_center:mails')
    
    def dispatch(self, request, *args, **kwargs):
        self.message = check_message(self.request, MessageInfo, self.kwargs.get('slug'))
        return super().dispatch(request, *args, **kwargs)
        
    def form_valid(self, form):
        form.instance.owner_send = self.request.user
        form.instance.message = self.message
        periodicity = form.cleaned_data['periodicity']
        clients = [email.client_mail for email in form.cleaned_data['clients']]
        start_time = form.cleaned_data['date_first_send']
        if start_time:
            form.instance.status = 'run'
        object_ = form.save()
        create_task_interval(object_=object_, task='mail_center.tasks.send', interval=periodicity, start_time=start_time, kwargs={'user_email': clients})
        return super().form_valid(form)
    
    def get_initial(self) -> dict[str, Any]:
        initial = super().get_initial()
        initial['message'] = self.message.pk
        return initial
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['message'] = self.message
        return context
      