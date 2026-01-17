from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView

from main.models import BirthDay
from main.forms import BdInputForm
from common.views import TitleMixin
from .services import MC


def index(request):
    context = {
        'title': 'Главная',
        'flen': len(MC.full_moons),
    }
    return render(request, 'main/index.html', context)


def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request, context={'title': 'О сайте'}))


def calc_result(request):
    context = {
        'title': 'Главная',
        'flen': len(MC.full_moons),
    }
    return render(request, 'main/result.html', context)


class DateInputView(TitleMixin, SuccessMessageMixin, CreateView):
    model = BirthDay
    template_name = 'main/day-form.html'
    form_class = BdInputForm
    title = 'ввод даты ...'
    success_message = 'Вы успешно ввели дату рождения'
    success_url = reverse_lazy('main:calc_result')


def add_date(request):
    if request.method == 'POST':
        date_form = BdInputForm(request.POST)
        if date_form.is_valid():
            saved_bday = date_form.save()
            # Приоритет: X-Forwarded-For, затем REMOTE_ADDR
            # XFF может содержать список IP, берем первый
            client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
            # Если XFF пуст или невалиден, можно использовать REMOTE_ADDR
            if not client_ip:
                client_ip = request.META.get('REMOTE_ADDR')
            # Если есть список, берем самый левый (реальный IP)
            if isinstance(client_ip, str) and ',' in client_ip:
                client_ip = client_ip.split(',')[0].strip()
            """ обновление связанных таблиц """
            return HttpResponseRedirect(reverse('main:calc_result', kwargs={'pk': saved_bday.pk}))
        else:
            context = {'form': date_form}
            return render(request, 'main/day-form.html', context)
    else:
        date_form = BdInputForm()
        context = {'form': date_form}
        return render(request, 'main/day-form.html', context)


# --------------- NN ------------------------
# from django.shortcuts import render, redirect
# from .forms import YourModelForm
# from .models import YourModel

# def create_item_view(request):
#     if request.method == 'POST':
#         form = YourModelForm(request.POST)
#         if form.is_valid():
#             # form.save() возвращает объект модели
#             saved_instance = form.save()
#             # Теперь у вас есть доступ к ID (pk)
#             new_item_id = saved_instance.pk  # или saved_instance.id
#             # Делайте что-то с ID, например, перенаправьте на страницу объекта
#             return redirect('item_detail', pk=new_item_id)
#     else:
#         form = YourModelForm()
#     return render(request, 'your_template.html', {'form': form})
