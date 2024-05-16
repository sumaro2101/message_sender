from django.shortcuts import render

# Create your views here.

def mail_center(request):
    return render(request, 'mail_center/mail_list.html', {'catg_selected': 5,
                                                          'title': 'Центр отправки'})