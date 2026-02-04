from datetime import datetime, timedelta

# from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
from django.urls import reverse
# from django.views.generic.edit import CreateView

from main.models import BirthDay, IP, BDayIP
from main.forms import BdInputForm
# from common.views import TitleMixin
from .services import MC, rounding, fase_presentation


def index(request):
    context = {
        'title': 'lunarage-главная',
        'flen': len(MC.full_moons),
    }
    return render(request, 'main/index.html', context)


def other_page(request, page):
    try:
        template = get_template('main/' + page + '.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request, context={'title': 'О сайте'}))


# def calc_result(request):
def calc_result(request, bday):
    # Конвертируем строку в datetime, например, из "2024-12-25"
    try:
        birth_date = datetime.strptime(bday, '%Y-%m-%d')  # или %Y-%m-%d %H:%M:%S
    except ValueError:
        # Обработка неверного формата
        print('НЕВЕРНЫЙ ФОРМАТ')
        print(f'bday ::::  {bday}')
    pf_moons = MC.fool_moons_calc(birth_date)[0]
    pn_moons, moon_age, fase = MC.new_moons_calc(birth_date)
    moonniversaries = []
    moonniversary = rounding(moon_age)
    moonniversary_date = MC.round_moon_date(birth_date, moonniversary)
    moonniversaries.append((moonniversary, moonniversary_date.date()))
    if moonniversary % 1000:
        moonniversary = rounding(moonniversary)
        moonniversary_date = MC.round_moon_date(birth_date, moonniversary)
        moonniversaries.append((moonniversary, moonniversary_date.date()))
    if moonniversary % 1000:
        moonniversary = rounding(moonniversary)
        moonniversary_date = MC.round_moon_date(birth_date, moonniversary)
        moonniversaries.append((moonniversary, moonniversary_date.date()))

    context = {
        'title': 'lunarage-расчёт',
        'precise_lunarage': moon_age,
        'full_moons': pf_moons,
        'new_moons': pn_moons,
        'fase': fase_presentation(fase),
        'moonniversaries': moonniversaries,
    }
    return render(request, 'main/result.html', context)


def date_input(request):
    if request.method == 'POST':
        date_form = BdInputForm(request.POST)
        print(request.POST.__dict__)
        if date_form.is_valid():
            print('date_form IS VALID')
            birthday = date_form.cleaned_data['birthday'] + timedelta(hours=4)
            new_bd_entry = BirthDay.objects.create(birthday=birthday)
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
            saved_ip_entry, save_status = IP.objects.get_or_create(ip=client_ip)
            if not save_status:
                saved_ip_entry.count += 1
                saved_ip_entry.save()
            BDayIP.objects.create(birth_day=new_bd_entry, ip=saved_ip_entry)
            return HttpResponseRedirect(reverse(
                'main:result',
                kwargs={'bday': new_bd_entry.birthday.strftime('%Y-%m-%d')}
                ))
        else:
            print('date_form IS NOOOOOOOOOOOOT VALID')
            print(date_form.errors.as_data())
            context = {
                'form': date_form,
                'title': 'ввод даты...',
                }
            return render(request, 'main/day-form.html', context)
    else:
        date_form = BdInputForm()
        context = {
            'form': date_form,
            'title': 'ввод даты...',
            }
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
