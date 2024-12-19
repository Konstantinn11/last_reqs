from django.views.generic import CreateView
import re
import requests
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()
from .forms import CreationForm, User_infoForm, VacationForm, MessageForm
from django.core.paginator import Paginator
from django.conf import settings
from posts.models import Feedback
from django.shortcuts import render, get_object_or_404, redirect
from .models import User_info, Log, Vacation, User_widgets, Message
from django.db.models import Q
#from django.utils import timezone
import datetime as dt
from posts.models import Unit, Post
from tasks.models import Bord, Note, Task
from tasks.forms import NoteForm
from storage.models import User_units
from storage.models import Unit as Block
from datetime import timedelta

from calendar import monthrange
import openpyxl
from openpyxl.styles import  Border, Side
#import pythoncom
#from win32com import client
import json
import shutil
import os
import zipfile
from corresp.models import Corresp
from users.vacation_data import holidays, month_num_str, special_work_days, bosses, months_ru, color_cycle 
from django.http import JsonResponse, Http404

def vac_access_check(request):
    return get_object_or_404(User_info, user_id=request.user.id).vacs_access

def user_access_check(request):
    return get_object_or_404(User_info, user_id=request.user.id).user_access

def some_count(request):

    content = {
        'feedbacks_count': Feedback.objects.filter(state_id__in=[5, 6]).count, # Новое, В работе,
        'users_counts': User.objects.all().count,
        'users_with_pass_access_counts': User_info.objects.filter(pass_access=True).count,
        'users_with_reqs_access_counts': User_info.objects.filter(reqs_access=True).count,
        'users_with_stor_access_counts': User_info.objects.filter(stor_access=True).count,
        'users_with_task_access_counts': User_info.objects.filter(task_access=True).count,
        'users_with_user_access_counts': User_info.objects.filter(user_access=True).count,
        'users_with_corr_access_counts': User_info.objects.filter(corr_access=True).count,
        'users_with_conf_access_counts': User_info.objects.filter(conf_access=True).count,
        }
    if request.user.username in settings.RIGHTS:
        try:
            ips = {'10.1.98.247', '10.1.98.248', '10.1.98.249'} # не везде это нужно (tasks например)
            rele_count_of_1 = []
            for ip in ips:
                res = requests.get(
                    'http://admin:admin@' + ip + '/pstat.xml',
                    verify=False,
                    timeout=5,
                    )
                rele_count_of_1 += re.findall(r'[>][1][<]', str(res.content))
            content_plus = {'count_of_1': len(rele_count_of_1), }
        except:
            content_plus = {'count_of_1': 0, }
        return {**content, **content_plus}
    return {**content}

def rights(request):
    rights = {
        'rights': settings.RIGHTS,
        'storage_rights': settings.STORAGE_RIGHTS,
        'sadec_rights': settings.SADEC_RIGHTS,
        'pro_rights': settings.PRO_RIGHTS,
        'passes_rights': settings.PASSES_RIGHTS,
        **some_count(request), #если реле нет - тормозит работу сайта
        }
    return rights


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = "users/signup.html"


def users(request):
    if not user_access_check(request):
        return render(request, 'no_rights.html',)

    users_list = User.objects.all().order_by('username')

    users_info = User_info.objects.all()
    paginator = Paginator(users_info, 40)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    content = {'users_info': users_info, }
    if request.user.username not in settings.RIGHTS:
        return redirect('index')
    add_log(
        request.user.id,
        dt.datetime.now(),
        "Переход на страницу",
        "Users",
        "Страница - Все сотрудники",
        'http://virtual2025.oak.cc:8000/' + 'auth/users/',
    )

    return render(request, 'users.html', {'page': page, **content, **rights(request)})


def users_access(request, app):
    if not user_access_check(request):
        return render(request, 'no_rights.html',)

    if app == 'user':
        users_info = User_info.objects.filter(user_access=True)
    elif app == 'reqs':
        users_info = User_info.objects.filter(reqs_access=True)
    elif app == 'conf':
        users_info = User_info.objects.filter(conf_access=True)
    elif app == 'task':
        users_info = User_info.objects.filter(task_access=True)
    elif app == 'stor':
        users_info = User_info.objects.filter(stor_access=True)
    elif app == 'corr':
        users_info = User_info.objects.filter(corr_access=True)
    elif app == 'pass':
        users_info = User_info.objects.filter(pass_access=True)

    users_id = []
    for user in users_info:
        users_id.append(user.user_id)

    users = User.objects.filter(id__in=users_id).order_by('username')
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    content = {'users_info': users_info, }
    if request.user.username not in settings.RIGHTS:
        return redirect('index')
    add_log(
        request.user.id,
        dt.datetime.now(),
        "Переход на страницу",
        "Users",
        f"Страница - Права доступа({app})",
        'http://virtual2025.oak.cc:8000/' + f'auth/users_access/{app}/',
    )
    return render(request, 'users.html', {'page': page, **content, **rights(request)})


def users_in_otd(request, number):
    if not user_access_check(request):
        return render(request, 'no_rights.html',)

    users_info = User_info.objects.filter(otd_number_id=number)
    users_id = []
    for user in users_info:
        users_id.append(user.user_id)

    users = User.objects.filter(id__in=users_id).order_by('username')
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    content = {'users_info': users_info, }
    if request.user.username not in settings.RIGHTS:
        return redirect('index')

    otd_number = Unit.objects.filter(id=number)[0].title
    if str(otd_number).rfind('(') != -1:
        otd_number = Unit.objects.filter(id=number)[0].title.split('(')[1][:-1]
    add_log(
        request.user.id,
        dt.datetime.now(),
        "Переход на страницу",
        "Users",
        f"Страница - Сотрудники отдела {otd_number}",
        'http://virtual2025.oak.cc:8000/' + f'auth/users_in_otd/{number}/',
    )
    return render(request, 'users.html', {'page': page, **content, **rights(request)})


@login_required
def users_info_change(request, user_id):
    if not user_access_check(request):
        return render(request, 'no_rights.html',)

    info = User_info.objects.filter(user_id=user_id)[0]
    name = User.objects.filter(id=user_id)[0].get_full_name
    form = User_infoForm(
        request.POST or None,
        files=request.FILES or None,
        instance=info,
    )
    if form.is_valid():
        form.save()
        return redirect('user_space', request.user.id)
        # return redirect('users')
    content = {'form': form, 'edit': "edit", 'name': name, **rights(request), }
    return render(request, 'user_info_new.html', {**content, **rights(request), } )


def user_search(request):
    #users_info = User_info.objects.all()
    q = request.GET.get("q")
    users = User.objects.filter(
        Q(first_name__icontains=q) | Q(last_name__icontains=q)
    )
    users_id = [user.id for user in users]
    users_info = User_info.objects.filter(user_id__in=users_id)

    content = {'page': users_info,  }
    return render(request, 'users.html', {**content, **rights(request), })


def log_all(request):
    logs = Log.objects.all()
    paginator = Paginator(logs, 29)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'log_all.html', {'page': page, **rights(request)},)


def add_log(*args):
    log = Log()
    log.user_id = args[0]
    log.day = args[1]
    log.event = args[2]
    log.res = args[3]
    log.before = args[4]
    log.after = args[5]
    log.save()


def del_vac_by_drop(request, otd, user_name, day):
    if not vac_access_check(request):
        return render(request, 'no_rights.html',)

    year = day.split('-')[0]
    f_n = user_name.split(' ')[0]
    l_n = user_name.split(' ')[1]
    user = User.objects.filter(first_name=f_n, last_name=l_n)[0]

    if request.user.id != user.id:
        if request.user.get_full_name() not in bosses.keys():
            return redirect('vacations', year, otd)

    vacations = Vacation.objects.filter(user_id=user.id, year=str(year))
    date = dt.datetime.strptime(day, '%Y-%m-%d').date()
    for vac in vacations:
        if vac.day_start.date() <= date and vac.day_end.date() >= date:
            vac.delete()
            break
    return redirect('vacations', year, otd)

def get_key_from_dict_by_value(dict, value):
    return [k for k, v in dict.items() if v == value][0]


def get_cross_vacations(vacations, users_colors, month_num_str):
    data = []
    for i in range(len(vacations)):
        for j in range(i + 1, len(vacations)):
            if vacations[i] != vacations[j]:
                if (
                    (vacations[i].day_start >= vacations[j].day_start and vacations[i].day_end <= vacations[j].day_end)
                    or (vacations[i].day_start <= vacations[j].day_end and vacations[i].day_end > vacations[j].day_end)
                    or (vacations[i].day_start < vacations[j].day_start and vacations[i].day_end >= vacations[j].day_start)
                    or (vacations[i].day_start < vacations[j].day_start and vacations[i].day_end > vacations[j].day_end)
                ):
                    data.append(vacations[i])
                    data.append(vacations[j])
    vac_with_color = []
    for vac in set(data):
        d = {
            'vac': vac,
            'range': f"{vac.day_start.day} {month_num_str[vac.day_start.month][:3]} - {vac.day_end.day} {month_num_str[vac.day_end.month][:3]}",
            'color': users_colors[vac.user.get_full_name()],
        }
        vac_with_color.append(d)
    return vac_with_color


def copy_dict_for_js(month_all):
    month_all_for_js = {}
    for month, days in month_all.items():
        month_all_for_js[month] = {}
        for week, days_in_week in days.items():
            month_all_for_js[month][week] = {}
            for i in range(len(days_in_week)):
                month_all_for_js[month][week][i] = {}
                month_all_for_js[month][week][i]['name'] =month_all[month][week][i]['name']
                month_all_for_js[month][week][i]['date'] = {}
                for key in month_all[month][week][i]['data'].keys():
                    month_all_for_js[month][week][i]['date'][key.replace(' ', '_')] =  month_all[month][week][i]['data'][key]
                month_all_for_js[month][week][i]['data'] = month_all[month][week][i]['data']
    return month_all_for_js


def vac_2(request, year, otd):
    if not vac_access_check(request):
        return render(request, 'no_rights.html',)

    if year == 0:
        year = dt.datetime.today().year
    today = dt.datetime.today().date()
    month_all = full_year(year)

    bosses_list = list(bosses.keys())
    current_user_name = request.user.get_full_name()

    if request.user.get_full_name() not in bosses.keys():
        otd_id = User_info.objects.filter(user_id=request.user.id)[0].otd_number_id
        otd = int(Unit.objects.filter(id=otd_id)[0].description)
        otd_users = User_info.objects.filter(otd_number_id=otd_id) 
        otd_users_id = [user.user_id for user in otd_users] 
        vacations = Vacation.objects.filter(user_id__in=otd_users_id, year=str(year))
        otds_for_choise = [otd]
        otd_users_full_names = [request.user]
    else:
        if otd == 0:  # Все
            vacations = Vacation.objects.filter(year=str(year))
        else:
            otd_id = Unit.objects.filter(description=otd)[0].id  
            otd_users = User_info.objects.filter(otd_number_id=otd_id)  
            otd_users_id = [user.user_id for user in otd_users]  
            vacations = Vacation.objects.filter(user_id__in=otd_users_id, year=str(year))
        otds_for_choise = bosses[request.user.get_full_name()]


        otd_ids = [Unit.objects.filter(description=descr)[0].id for descr in bosses[request.user.get_full_name()]]

        otd_users = User_info.objects.filter(otd_number_id__in=otd_ids) 
        otd_users_id = [user.user_id for user in otd_users]
        otd_users_full_names = [user for user in User.objects.filter(id__in=otd_users_id)]


    vacation_start_dates = {}
    for vac in vacations:
        if vac.user.get_full_name() not in vacation_start_dates:
            vacation_start_dates[vac.user.get_full_name()] = []

        vacation_start_dates[vac.user.get_full_name()].append(vac.day_start.date())

    users_colors = {} 

    for vac in vacations:
        if vac.user.get_full_name() not in users_colors.keys():
            users_colors[vac.user.get_full_name()] = next(color_cycle)

    cross_vacations = get_cross_vacations(vacations, users_colors, month_num_str)


    vacations_by_user = {}
    users_otd = User_info.objects.all()
    for vac in vacations:
        if vac.user.get_full_name() not in vacations_by_user.keys():
            vacations_by_user[vac.user.get_full_name()] = {
                'color': users_colors[vac.user.get_full_name()],
                'dates': [],
                'sum': 0,
                'otd': '',
                'user_id': vac.user_id,
                'vacation_start_dates': [],
                'vacation_end_dates': [],
            }
            for u in users_otd:
                if u.user_id == vac.user_id:
                    vacations_by_user[vac.user.get_full_name()]['otd'] =  u.otd_number
                    break
        
        start_date = vac.day_start.date()
        days_count = (vac.day_end.date() - vac.day_start.date()).days + 1  

        # Считаем количество праздничных дней, которые попадают в отпуск
        holidays_count = 0
        for y, m_d in holidays.items():
            for m, d in m_d.items():
                for day in d:
                    # Получаем номер месяца
                    month_number = get_key_from_dict_by_value(month_num_str, m)

                    # Формируем дату праздника
                    holiday_date = today.replace(year=int(y), month=month_number, day=day)

                    # Проверяем, попадает ли праздник в диапазон отпуска
                    if vac.day_start.date() <= holiday_date <= vac.day_end.date():
                        holidays_count += 1

        # Корректируем количество дней отпуска с учетом праздничных дней
        days_count -= holidays_count

        # Теперь вычисляем дату окончания с учетом исключенных праздничных дней
        end_date = start_date + dt.timedelta(days=days_count - 1)

        # Если мы вычли праздничные дни, увеличиваем дату окончания
        end_date += dt.timedelta(days=holidays_count)

        vacations_by_user[vac.user.get_full_name()]['vacation_start_dates'].append((start_date, days_count))

        vacations_by_user[vac.user.get_full_name()]['dates'].append(
            {'d': f"{vac.day_start.day} {month_num_str[vac.day_start.month][:3]} - {vac.day_end.day} {month_num_str[vac.day_end.month][:3]}",
            'vac_id': vac.id,
            }
        )

        vacations_by_user[vac.user.get_full_name()]['sum'] += (vac.day_end.date() - vac.day_start.date()).days + 1

        # Добавление даты окончания в словарь
        vacations_by_user[vac.user.get_full_name()]['vacation_end_dates'].append(end_date)
        
        for y, m_d in holidays.items():
            for m, d in m_d.items():
                for day in d:
                    month_number = get_key_from_dict_by_value(month_num_str, m)

                    date = today.replace(year=int(y), month=month_number, day=day)
                    if date >= vac.day_start.date() and date <= vac.day_end.date():
                        vacations_by_user[vac.user.get_full_name()]['sum'] -= 1

    for month, days in month_all.items():
        for week, days_in_week in days.items():
            for i in range(len(days_in_week)):
                data = {}
                date = ""
                if str(days_in_week[i]) != "":
                    month_number = get_key_from_dict_by_value(month_num_str, month)

                    day = today.replace(year=int(year), month=month_number, day=days_in_week[i])

                    for vac in vacations:
                        if day >= vac.day_start.date() and day <= vac.day_end.date():
                            data[vac.user.get_full_name()] = {
                                'date': f"{vac.day_start.date()} - {vac.day_end.date()}",
                                'color': users_colors[vac.user.get_full_name()],
                                'vac_id': vac.id,
                            }

                    m = [k for k, v in month_num_str.items() if v == month ][0]
                    date = today.replace(year=int(year), month=m, day=int(days_in_week[i]))
                month_all[month][week][i] = {'name': days_in_week[i], 'data': data, 'date': date, }

    month_all_for_js = copy_dict_for_js(month_all)

    
    
    if year in holidays.keys():
        h_days = holidays[year]
    else:
        h_days = {}

    all_vac_for_js = {}
    for vac in vacations:
        all_vac_for_js[vac.id] = [str(vac.day_start.date()), str(vac.day_end.date()), vac.how_long]

    
    return render(
        request,
        'vac_new_calendar.html',
        {**rights(request),
         'today': today,
         'year': year,
         'otd': otd,
         'pdf': settings.BASE_DIR + f"/posts/static/users/vacations_{otd}_{year}.pdf",
         **month_all,
         'json_data': json.dumps(month_all_for_js),
         'json_data_vacs': json.dumps(all_vac_for_js),
         
         'cross_vacations': cross_vacations,
         'len_cross_vacations': len(cross_vacations),
         'len_vacations': vacations.count,
         'special_work_days': special_work_days,
         'vacations_by_user': vacations_by_user,
         'holidays': h_days,
         'otds_for_choise': otds_for_choise,
         'bosses': [key for key in bosses.keys()],
         'otd_users_full_names': otd_users_full_names,
         'vacation_start_dates': vacation_start_dates,

         'show_button': True,
         'show_add_leave_button': True,
         'bosses_list': json.dumps(bosses_list),
         'current_user_name': current_user_name,
         'navbar_style': 'custom-navbar',
         'show_vacation_link': True,
        }
    )

def get_user_bords_and_ids(all_bords, user_id):
    user_bords = [b for b in all_bords if (str(user_id) in b.guests.split('_')) or b.user_id == user_id ]
    user_bords_ids = [bord.id for bord in user_bords]
    if len(user_bords_ids) == 0:
        user_bords_ids.append(0)
    return user_bords, user_bords_ids

def get_tasks_sorted_by_bords(user_bords_ids):
    data = {}
    all_tasks = Task.objects.all()
    for t in all_tasks:
        if t.bord_id in user_bords_ids:
            if t.bord_id not in data.keys():
                data[t.bord_id] = []
            data[t.bord_id].append(t)
    return data

def get_new_tasks_sorted_by_bords(tasks_sorted_by_bords, user):
    data = {}
    for key in tasks_sorted_by_bords.keys():
        for t in tasks_sorted_by_bords[key]:
            if t.slave == user:
                if t.new:
                    if key not in data.keys():
                        data[key] = 0
                    data[key] += 1
    return data

@login_required
def user_space(request, user_id):
    if user_id == 0:
        return redirect('user_space', request.user.id)
    users = User.objects.all()
    users_info = User_info.objects.all()
    users_info_for_widget = {}
    for u in users_info:
        if u.otd_number not in users_info_for_widget.keys():
            users_info_for_widget[u.otd_number] = {}
        users_info_for_widget[u.otd_number][u.user_id] = get_object_or_404(User, id=u.user_id)

    user = get_object_or_404(User, id=user_id)
    #user_info = get_object_or_404(User_info, user_id=user_id)

    user_info = User_info.objects.filter(user_id=user_id)
    if len(user_info) == 0:
        new_u_i = User_info()
        new_u_i.user_id = user_id
        new_u_i.save()
        user_info = User_info.objects.filter(user_id=user_id)[0]
    else:
        user_info = User_info.objects.filter(user_id=user_id)[0]

    # user_widgets = get_object_or_404(User_widgets, user_id=user_id)
    user_widgets = User_widgets.objects.filter(user_id=user_id)
    if len(user_widgets) == 0:
        new_u_w = User_widgets()
        new_u_w.user_id = user_id
        new_u_w.save()
        user_widgets = User_widgets.objects.filter(user_id=user_id)[0]
    else:
        user_widgets = User_widgets.objects.filter(user_id=user_id)[0]

    widgets_order = str(user_widgets.widgets_order)
    # Работа с досками задач -------------------------------------------------
    # Все доски с задачами
    all_bords = Bord.objects.all()
    # Все доски [], где участвует пользователь и их id [] 

    user_bords, user_bords_ids = get_user_bords_and_ids(all_bords, user_id)
    tasks_sorted_by_bords = get_tasks_sorted_by_bords(user_bords_ids)
    new_tasks_sorted_by_bords = get_new_tasks_sorted_by_bords(tasks_sorted_by_bords, request.user)
    # ------------------------------------------------------------------------

    posts = Post.objects.filter(author_id=user.id).order_by('-id')[:20]
    posts_new = Post.objects.filter(task_state_id=1).order_by('-day')
    vacations = Vacation.objects.filter(user_id=user.id, year=str(dt.datetime.today().year))
    chats = Message.objects.filter(
        Q(user_one_id=user_id) | Q(user_two_id=user_id)
    )
    user_chats = set()
    for c in chats:
        user_chats.add(User.objects.filter(id=c.user_one_id)[0])
        user_chats.add(User.objects.filter(id=c.user_two_id)[0])

    unreaded = {}
    for u in user_chats:
        for chat in chats:
            if (u.id == chat.user_two_id or u.id == chat.user_one_id) and u.id != chat.witch_write_id and not chat.readed:
                if u.id not in unreaded.keys():
                    if u.id == chat.user_two_id:
                        unreaded[chat.user_one_id] = 0
                    else:
                        unreaded[chat.user_two_id] = 0     
                try:                 
                    unreaded[chat.user_one_id] += 1
                except:
                    unreaded[chat.user_two_id] += 1

    user_notes = Note.objects.filter(user=request.user)
    json_data ={}
    for t in user_notes:

        json_data[t.id] = []
        json_data[t.id].append(t.text)
        json_data[t.id].append(t.same_id)

        if t.day_update is not None:
            json_data[t.id].append(str(t.day_update.date()))
        else:
            json_data[t.id].append("")

    note = Note()
    note.user = request.user
    form = NoteForm(
        request.POST or None,
        files=request.FILES or None,
        instance=note,
    )
    if form.is_valid():
        note = form.save(commit=False)
        if note.same_id is not None:
            note.id = int(note.same_id)
        else: 
            try:
                note.id = Note.objects.all().latest('id').id + 1
            except:
                note.id = 1
            note.same_id = note.id
        note.save()
        return redirect('user_space', request.user.id)

    some_colors = ["#FA8072"]
    year = dt.datetime.today().year
    today = dt.datetime.today().date()
    month_all = full_year(year)

    users_colors = {}  # изменить на присвоение уникального номера юзеру

    for vac in vacations:
        if vac.user.get_full_name() not in users_colors.keys():
            # Получаем следующий цвет из цикла
            users_colors[vac.user.get_full_name()] = next(color_cycle)

    # [{'vac': vac, 'range': range, 'color': color, }]
    cross_vacations = get_cross_vacations(vacations, users_colors, month_num_str)


    vacations_by_user = {}
    users_otd = User_info.objects.all()
    for vac in vacations:
        if vac.user.get_full_name() not in vacations_by_user.keys():
            vacations_by_user[vac.user.get_full_name()] = {
                'color': users_colors[vac.user.get_full_name()],
                'dates': [],  # {'d': 12.12 -18.12, 'vac_id': vac_id, 'vac_can_redact': vac_can_redact}
                'sum': 0,
                'otd': '',
                'user_id': vac.user_id,
            }
            for u in users_otd:
                if u.user_id == vac.user_id:
                    vacations_by_user[vac.user.get_full_name()]['otd'] =  u.otd_number
                    break
        vacations_by_user[vac.user.get_full_name()]['dates'].append(
            {'d': f"{vac.day_start.day} {month_num_str[vac.day_start.month][:3]} - {vac.day_end.day} {month_num_str[vac.day_end.month][:3]}",
            'vac_id': vac.id,
            'vac_can_redact': vac.can_redact,
            }
        )


        vacations_by_user[vac.user.get_full_name()]['sum'] += (vac.day_end.date() - vac.day_start.date()).days + 1

        for y, m_d in holidays.items():
            for m, d in m_d.items():
                for day in d:
                    month_number = get_key_from_dict_by_value(month_num_str, m)

                    date = today.replace(year=int(y), month=month_number, day=day)
                    if date >= vac.day_start.date() and date <= vac.day_end.date():
                        vacations_by_user[vac.user.get_full_name()]['sum'] -= 1

    for month, days in month_all.items():
        for week, days_in_week in days.items():
            for i in range(len(days_in_week)):
                data = {}
                date = ""
                if str(days_in_week[i]) != "":
                    month_number = get_key_from_dict_by_value(month_num_str, month)

                    day = today.replace(year=int(year), month=month_number, day=days_in_week[i])

                    for vac in vacations:
                        if day >= vac.day_start.date() and day <= vac.day_end.date():
                            data[vac.user.get_full_name()] = {
                                'date': f"{vac.day_start.date()} - {vac.day_end.date()}",
                                'color': users_colors[vac.user.get_full_name()],
                            }

                    m = [k for k, v in month_num_str.items() if v == month ][0]
                    date = today.replace(year=int(year), month=m, day=int(days_in_week[i]))
                month_all[month][week][i] = {'name': days_in_week[i], 'data': data, 'date': date, }
    if year in holidays.keys():
        h_days = holidays[year]
    else:
        h_days = {}

    storage_user_likes = User_units.objects.filter(user_id=request.user.id)
    storage_user_likes_ids = [like.unit_id for like in storage_user_likes]
    favorite_units = Block.objects.filter(id__in=storage_user_likes_ids)

    corresp = Corresp.objects.all()
    cor_years = [c.day.year for c in corresp]
    cor_years = sorted(set(cor_years))
    cor_tags = [str(c.tag) for c in corresp]
    cor_tags = sorted(set(cor_tags))

    return render(
        request,
        'user_space.html', {
            'today': today,
            'user': user,
            'users': users,
            'user_info': user_info,
            'users_info': users_info,
            'user_widgets': user_widgets,
            'widgets_order': widgets_order,
            'user_notes': user_notes,
            'user_bords': user_bords,
            'user_start_bord_id': user_bords_ids[0],
            'posts': posts,
            'posts_new': posts_new,
            'vacations': vacations,
            'user_chats': user_chats,
            'unreaded': unreaded,
            'form': form,
            'json_data': json.dumps(json_data),
            'year': year,
            **month_all,
            'cross_vacations': cross_vacations,
            'len_cross_vacations': len(cross_vacations),
            'len_vacations': vacations.count,
            'special_work_days': special_work_days,
            'vacations_by_user': vacations_by_user,
            'holidays': h_days,
            'favorite_units': favorite_units,
            'users_info_for_widget': users_info_for_widget,
            'new_tasks_sorted_by_bords': new_tasks_sorted_by_bords,
            'corresp': corresp,
            'cor_years': cor_years,
            'cor_tags': cor_tags,
            **rights(request),
        }
    )


@login_required
def backup_base(request):
    if not user_access_check(request):
        return render(request, 'no_rights.html',)

    if os.path.exists(settings.MEDIA_ROOT + f"/db.sqlite3"):
        os.remove(settings.MEDIA_ROOT + f"/db.sqlite3")
    shutil.copy2(settings.BASE_DIR + f"/db.sqlite3", settings.MEDIA_ROOT + f"/db.sqlite3")
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def backup_files(request):
    if not user_access_check(request):
        return render(request, 'no_rights.html',)


    def zipdir(path, ziph):
        for root, dirs, files in os.walk(path):
            for file in files:
                if file != 'files.zip':
                    ziph.write(os.path.join(root, file))

    if os.path.exists(settings.MEDIA_ROOT + f"/files.zip"):
        os.remove(settings.MEDIA_ROOT + f"/files.zip")
    
    zipf = zipfile.ZipFile(settings.MEDIA_ROOT + f"/files.zip", 'w', zipfile.ZIP_DEFLATED)
    zipdir(settings.MEDIA_ROOT, zipf)
    zipf.close()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def user_widget_add(request, user_id, widget_name):
    user_info = get_object_or_404(User_info, user_id=user_id)
    user_widgets = get_object_or_404(User_widgets, user_id=user_id)

    names = {
        'reqs': 'reqs_access',
        'vacs': 'vacs_access',
        'test': 'test_access',
        'corr': 'corr_access',
        'task': 'task_access',
        'bibl': 'bibl_access',
        'stor': 'stor_access',
        'users': 'user_access',
        'news': 'news_access',
        'mess': 'mess_access',
        'notes': 'note_access',
        'calc': 'calc_access',
    }
    if names[widget_name] == 'reqs_access':
        if user_info.reqs_access and not user_widgets.reqs:
            user_widgets.reqs = True
    elif names[widget_name] == 'vacs_access':
        if user_info.vacs_access and not user_widgets.vacs:
            user_widgets.vacs = True
    elif names[widget_name] == 'test_access':
        if user_info.test_access and not user_widgets.test:
            user_widgets.test = True
    elif names[widget_name] == 'corr_access':
        if user_info.corr_access and not user_widgets.corr:
            user_widgets.corr = True
    elif names[widget_name] == 'task_access':
        if user_info.task_access and not user_widgets.task:
            user_widgets.task = True
    elif names[widget_name] == 'bibl_access':
        if user_info.bibl_access and not user_widgets.bibl:
            user_widgets.bibl = True
    elif names[widget_name] == 'stor_access':
        if user_info.stor_access and not user_widgets.stor:
            user_widgets.stor = True
    elif names[widget_name] == 'user_access':
        if user_info.user_access and not user_widgets.users:
            user_widgets.users = True
    elif names[widget_name] == 'news_access':
        if user_info.news_access and not user_widgets.news:
            user_widgets.news = True
    elif names[widget_name] == 'mess_access':
        if user_info.mess_access and not user_widgets.mess:
            user_widgets.mess = True
    elif names[widget_name] == 'note_access':
        if not user_widgets.notes:
            user_widgets.notes = True
    elif names[widget_name] == 'calc_access':
        if not user_widgets.calc:
            user_widgets.calc = True
    user_widgets.save()

    return redirect('user_space', user_id)


@login_required
def user_widget_close(request, user_id, widget_name,  widget_id):
    user_widgets = get_object_or_404(User_widgets, user_id=user_id)

    names = {
        'reqs': 'reqs_open',
        'vacs': 'vacs_open',
        'test': 'test_open',
        'corr': 'corr_open',
        'tasks': 'task_open',
        'bibl': 'bibl_open',
        'stor': 'stor_open',
        'users': 'users_open',
        'news': 'news_open',
        'mess': 'mess_open',
        'notes': 'notes_open',
        'calc': 'calc_open',
    }


    order = getattr(user_widgets, 'widgets_order').split('_')
    if getattr(user_widgets, names[widget_name]):
        setattr(user_widgets, names[widget_name], False)

        order.append(order.pop(order.index(str(widget_id))))
        setattr(user_widgets, 'widgets_order', '_'.join(order))
    else:
        setattr(user_widgets, names[widget_name], True)

        order.insert(0, order.pop(order.index(str(widget_id))))
        setattr(user_widgets, 'widgets_order', '_'.join(order))


            
    user_widgets.save()
    return redirect(request.META.get('HTTP_REFERER'))
    #return redirect('user_space', user_id)


@login_required
def user_widget_close_all(request, user_id, state):
    user_widgets = get_object_or_404(User_widgets, user_id=user_id)

    names = {
        'reqs': 'reqs_open',
        'vacs': 'vacs_open',
        'test': 'test_open',
        'corr': 'corr_open',
        'tasks': 'task_open',
        'bibl': 'bibl_open',
        'stor': 'stor_open',
        'users': 'users_open',
        'news': 'news_open',
        'mess': 'mess_open',
        'notes': 'notes_open',
        'calc': 'calc_open',
    }
    if state == 'close':
        for name in names.keys():
            setattr(user_widgets, names[name], False)
    elif state == 'open':
        for name in names.keys():
            setattr(user_widgets, names[name], True)

            
    user_widgets.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def user_widget_delete(request, user_id, widget_name):
    user_info = get_object_or_404(User_info, user_id=user_id)
    user_widgets = get_object_or_404(User_widgets, user_id=user_id)

    names = {
        'reqs': 'reqs_access',
        'vacs': 'vacs_access',
        'test': 'test_access',
        'corr': 'corr_access',
        'task': 'task_access',
        'bibl': 'bibl_access',
        'stor': 'stor_access',
        'users': 'user_access',
        'news': 'news_access',
        'mess': 'mess_access',
        'notes': 'note_access',
        'calc': 'calc_access',
    }
    if names[widget_name] == 'reqs_access':
        if user_widgets.reqs:
            user_widgets.reqs = False
    elif names[widget_name] == 'vacs_access':
        if user_widgets.vacs:
            user_widgets.vacs = False
    elif names[widget_name] == 'test_access':
        if user_widgets.test:
            user_widgets.test = False
    elif names[widget_name] == 'corr_access':
        if user_widgets.corr:
            user_widgets.corr = False
    elif names[widget_name] == 'task_access':
        if user_widgets.task:
            user_widgets.task = False
    elif names[widget_name] == 'bibl_access':
        if user_widgets.bibl:
            user_widgets.bibl = False
    elif names[widget_name] == 'stor_access':
        if user_widgets.stor:
            user_widgets.stor = False
    elif names[widget_name] == 'user_access':
        if user_widgets.users:
            user_widgets.users = False
    elif names[widget_name] == 'news_access':
        if user_widgets.news:
            user_widgets.news = False
    elif names[widget_name] == 'mess_access':
        if user_widgets.mess:
            user_widgets.mess = False
    elif names[widget_name] == 'note_access':
        if user_widgets.notes:
            user_widgets.notes = False
    elif names[widget_name] == 'calc_access':
        if user_widgets.calc:
            user_widgets.calc = False
    user_widgets.save()

    return redirect('user_space', user_id)


@login_required
def note_delete(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    note.delete()
    return redirect('user_space', request.user.id)

@login_required
def messages(request, user_one_id, user_two_id):
    user_one = get_object_or_404(User, id=user_one_id)
    user_two = get_object_or_404(User, id=user_two_id)
    chats = Message.objects.filter(
        Q(user_one_id=request.user.id) | Q(user_two_id=request.user.id)
    )
    user_chats = set()
    for c in chats:
        user_chats.add(User.objects.filter(id=c.user_one_id)[0])
        user_chats.add(User.objects.filter(id=c.user_two_id)[0])
    
    unreaded = {}
    for user in user_chats:
        for chat in chats:
            if (user.id == chat.user_two_id or user.id == chat.user_one_id) and user.id != chat.witch_write_id and not chat.readed:
                if user.id not in unreaded.keys():
                    if user.id == chat.user_two_id:
                        unreaded[chat.user_one_id] = 0
                    else:
                        unreaded[chat.user_two_id] = 0
                try:
                    unreaded[chat.user_one_id] += 1
                    
                except:
                    unreaded[chat.user_two_id] += 1

    messages = Message.objects.filter(
        Q(user_one_id=user_one_id, user_two_id=user_two_id) | Q(user_one_id=user_two_id, user_two_id=user_one_id)
    )
    for m in messages:
        if m.witch_write_id != request.user.id:
            
            if m.readed == False:
                m.readed = True
                m.save()

    mes = Message()
    mes.user_one_id = user_one_id
    mes.user_two_id = user_two_id
    mes.witch_write_id = request.user.id
    mes.pub_date = dt.datetime.now()
    mes.user_one_id = user_one_id
    form = MessageForm(
        request.POST or None,
        files=request.FILES or None,
        instance=mes,
    )
    if form.is_valid():
        mes = form.save(commit=False)
        if mes.text != "":
            mes.save()
            return redirect('messages', user_one_id, user_two_id)
            
    return render(
        request,
        'user_messages.html',
        {'user': request.user, **rights(request), 'messages': messages, 'user_one': user_one, 'user_two': user_two, 'form': form,
        'user_chats': user_chats, 'unreaded': unreaded, 'users': User.objects.all()}
    )


@login_required
def vacations_by_user(request, year, otd):
    if not vac_access_check(request):
        return render(request, 'no_rights.html',)

    vacations = Vacation.objects.filter(user_id=request.user.id, year=str(year))
    years = [2023, 2024]
    return render(
        request,
        'vacations_by_user.html',
        {'user': request.user, **rights(request), 'otd': otd, 'number': otd,  'vacations': vacations, 'year': year, 'years': years, 'bosses': bosses,
        'pdf': settings.BASE_DIR + f"/posts/static/users/vacations_{otd}.pdf",}
    )

@login_required
def vacation_confirm_from_day(request, year, otd, user, day):
    if not vac_access_check(request):
        return render(request, 'no_rights.html',)

    day = dt.datetime.strptime(day, '%Y-%m-%d')
    for u in User.objects.all():
        if u.get_full_name() == user:
            print(u.id)
            vac = get_object_or_404(Vacation, user_id=u.id, day_start__lte=day, day_end__gte=day)
            if vac.can_redact:
                vac.can_redact = False
            else:
                vac.can_redact = True
            vac.save()
            break


    return redirect('vacations', year, otd)

def paint_all_borders(full_len, start, mass, ws):
    thin = Side(border_style="thin", color="000000") # стиль границ
    for i in range(int(start), full_len + int(start)):
        for el in mass:
            cell = el + str(i)
            ws[cell].border = Border(top=thin, left=thin, right=thin, bottom=thin,)

def full_year(year):
    month_all = {
        1:'Январь', 2:'Февраль', 3:'Март',
        4:'Апрель', 5:'Май', 6:'Июнь',
        7:'Июль', 8:'Август', 9:'Сентябрь',
        10:'Октябрь', 11:'Ноябрь', 12:'Декабрь',
        }
    month_new = {}
    for i in range(1, 13):
        day = dt.datetime.today().replace(
            year=year,
            month=i,
            day=1
            )
        mnth_strt_d = day.replace(month=i, day=1).weekday()
        days_in_month = monthrange(year, i)[1]
        weeks, k = {}, 1
        weeks[k] = []
        #добавляем пустые клетки в начале месяца, если он начался не с понедельника
        [weeks[k].append('') for j in range(mnth_strt_d) if mnth_strt_d != 0]
        #заполняем месяц
        for j in range(1, days_in_month + 1):
            if mnth_strt_d < 7:
                weeks[k].append(j)
                mnth_strt_d += 1
            else:
                k += 1
                weeks[k] = []
                weeks[k].append(j)
                mnth_strt_d = 1
        #добавляем пустые клетки в конце месяца, если он закончился не в воскресенье    
        [weeks[k].append('') for j in range(mnth_strt_d, 7)]
        month_new[month_all[i]] = weeks
    return month_new

def vacations_start(request):
    if not vac_access_check(request):
        return render(request, 'no_rights.html',)

    try:
        otd_id = User_info.objects.filter(user_id=request.user.id)[0].otd_number_id
        otd = int(Unit.objects.filter(id=otd_id)[0].description)
    except:
        otd = 0
    year = dt.datetime.today().year
    bosses = {'Константин Мишуков' : [305, 306, 307],}
    return render(
        request,
        'vacations_all.html',
        {**rights(request), 'otd': otd, 'bosses': bosses, 'year': year, },
    )

def vac_2_days(request, year, otd):
    if not vac_access_check(request):
        return render(request, 'no_rights.html',)
    
    if year == 0:
        year = dt.datetime.today().year
    today = dt.datetime.today().date()
    month_all = full_year(year)

    bosses_list = list(bosses.keys())
    current_user_name = request.user.get_full_name()

    if request.user.get_full_name() not in bosses.keys():
        otd_id = User_info.objects.filter(user_id=request.user.id)[0].otd_number_id
        otd = int(Unit.objects.filter(id=otd_id)[0].description)
        otd_users = User_info.objects.filter(otd_number_id=otd_id)
        otd_users_id = [user.user_id for user in otd_users]
        vacations = Vacation.objects.filter(user_id__in=otd_users_id, year=str(year))
        otds_for_choise = [otd]
        otd_users_full_names = [request.user]
    else:
        if otd == 0:  # Все
            vacations = Vacation.objects.filter(year=str(year))
        else:
            otd_id = Unit.objects.filter(description=otd)[0].id
            otd_users = User_info.objects.filter(otd_number_id=otd_id)
            otd_users_id = [user.user_id for user in otd_users]
            vacations = Vacation.objects.filter(user_id__in=otd_users_id, year=str(year))
        otds_for_choise = bosses[request.user.get_full_name()]


        otd_ids = [Unit.objects.filter(description=descr)[0].id for descr in bosses[request.user.get_full_name()]]

        otd_users = User_info.objects.filter(otd_number_id__in=otd_ids)
        otd_users_id = [user.user_id for user in otd_users]
        otd_users_full_names = [user for user in User.objects.filter(id__in=otd_users_id)]


    vacation_start_dates = {}
    for vac in vacations:
        if vac.user.get_full_name() not in vacation_start_dates:
            vacation_start_dates[vac.user.get_full_name()] = []

        vacation_start_dates[vac.user.get_full_name()].append(vac.day_start.date())

    users_colors = {}

    for vac in vacations:
        if vac.user.get_full_name() not in users_colors.keys():
            users_colors[vac.user.get_full_name()] = next(color_cycle)

    vacations_by_user = {}
    users_otd = User_info.objects.all()
    for vac in vacations:
        if vac.user.get_full_name() not in vacations_by_user.keys():
            vacations_by_user[vac.user.get_full_name()] = {
                'color': users_colors[vac.user.get_full_name()],
                'dates': [],
                'sum': 0,
                'otd': '',
                'user_id': vac.user_id,
                'vacation_start_dates': [],
                'vacation_end_dates': [],
            }
            for u in users_otd:
                if u.user_id == vac.user_id:
                    vacations_by_user[vac.user.get_full_name()]['otd'] =  u.otd_number
                    break
        
        start_date = vac.day_start.date()
        days_count = (vac.day_end.date() - vac.day_start.date()).days + 1

        # Считаем количество праздничных дней, которые попадают в отпуск
        holidays_count = 0
        for y, m_d in holidays.items():
            for m, d in m_d.items():
                for day in d:
                    month_number = get_key_from_dict_by_value(month_num_str, m)

                    holiday_date = today.replace(year=int(y), month=month_number, day=day)

                    if vac.day_start.date() <= holiday_date <= vac.day_end.date():
                        holidays_count += 1

        days_count -= holidays_count

        end_date = start_date + dt.timedelta(days=days_count - 1)

        end_date += dt.timedelta(days=holidays_count)

        vacations_by_user[vac.user.get_full_name()]['vacation_start_dates'].append((start_date, days_count))

        vacations_by_user[vac.user.get_full_name()]['dates'].append(
            {'d': f"{vac.day_start.day} {month_num_str[vac.day_start.month][:3]} - {vac.day_end.day} {month_num_str[vac.day_end.month][:3]}",
            'vac_id': vac.id,
            }
        )

        vacations_by_user[vac.user.get_full_name()]['sum'] += (vac.day_end.date() - vac.day_start.date()).days + 1

        # Добавление даты окончания в словарь
        vacations_by_user[vac.user.get_full_name()]['vacation_end_dates'].append(end_date)
        
        for y, m_d in holidays.items():
            for m, d in m_d.items():
                for day in d:
                    month_number = get_key_from_dict_by_value(month_num_str, m)

                    date = today.replace(year=int(y), month=month_number, day=day)
                    if date >= vac.day_start.date() and date <= vac.day_end.date():
                        vacations_by_user[vac.user.get_full_name()]['sum'] -= 1

    for month, days in month_all.items():
        for week, days_in_week in days.items():
            for i in range(len(days_in_week)):
                data = {}
                date = ""
                if str(days_in_week[i]) != "":
                    month_number = get_key_from_dict_by_value(month_num_str, month)

                    day = today.replace(year=int(year), month=month_number, day=days_in_week[i])

                    for vac in vacations:
                        if day >= vac.day_start.date() and day <= vac.day_end.date():
                            data[vac.user.get_full_name()] = {
                                'date': f"{vac.day_start.date()} - {vac.day_end.date()}",
                                'color': users_colors[vac.user.get_full_name()],
                            }

                    m = [k for k, v in month_num_str.items() if v == month ][0]
                    date = today.replace(year=int(year), month=m, day=int(days_in_week[i]))
                month_all[month][week][i] = {'name': days_in_week[i], 'data': data, 'date': date, }
    
    if year in holidays.keys():
        h_days = holidays[year]
    else:
        h_days = {}

    return render(
        request,
        'vac_schedule_days.html',
        {**rights(request),
         'today': today,
         'year': year,
         'otd': otd,
         **month_all,
         'len_vacations': vacations.count,
         'special_work_days': special_work_days,
         'vacations_by_user': vacations_by_user,
         'holidays': h_days,
         'otds_for_choise': otds_for_choise,
         'bosses': [key for key in bosses.keys()],
         'otd_users_full_names': otd_users_full_names,
         'vacation_start_dates': vacation_start_dates,

         'show_button': True,
         'show_add_leave_button': True,
         'bosses_list': json.dumps(bosses_list),
         'current_user_name': current_user_name,
         'navbar_style': 'custom-navbar',
         'show_vacation_link': True,
        }
    )

def vac_all(request, otd):
    if not vac_access_check(request):
        return render(request, 'no_rights.html',)

    today = dt.datetime.today().date()
    year = today.year

    current_user_name = request.user.get_full_name()

    # Если пользователь не является боссом
    if current_user_name not in bosses:
        otd_id = User_info.objects.filter(user_id=request.user.id)[0].otd_number_id
        otd = int(Unit.objects.filter(id=otd_id)[0].description)
        otd_users = User_info.objects.filter(otd_number_id=otd_id)
        otd_users_id = [user.user_id for user in otd_users]
        vacations = Vacation.objects.filter(user_id__in=otd_users_id, day_end__gte=today).order_by('day_start')
        otds_for_choise = [otd]
    else:
        # Если пользователь босс
        if otd == 0:  # Все отделы, которыми он руководит
            otds_for_choise = bosses[current_user_name]
            otd_ids = [Unit.objects.filter(description=descr)[0].id for descr in otds_for_choise]
            otd_users = User_info.objects.filter(otd_number_id__in=otd_ids)
        else:  # Выбран конкретный отдел
            otd_id = Unit.objects.filter(description=otd)[0].id
            otd_users = User_info.objects.filter(otd_number_id=otd_id)
            otds_for_choise = [otd]

        otd_users_id = [user.user_id for user in otd_users]
        vacations = Vacation.objects.filter(user_id__in=otd_users_id, day_end__gte=today).order_by('day_start')

    # Дальнейшая логика остаётся прежней
    nearest_vacations = {}
    for vac in vacations:
        if vac.day_start.date() >= today or (vac.day_start.date() <= today <= vac.day_end.date()):
            if vac.user.get_full_name() not in nearest_vacations:
                nearest_vacations[vac.user.get_full_name()] = vac
            elif vac.day_start.date() < nearest_vacations[vac.user.get_full_name()].day_start.date():
                nearest_vacations[vac.user.get_full_name()] = vac

    filtered_vacations = list(nearest_vacations.values())

    vacation_start_dates = {}
    for vac in filtered_vacations:
        vacation_start_dates.setdefault(vac.user.get_full_name(), []).append(vac.day_start.date())

    users_colors = {}
    for vac in vacations:
        if vac.user.get_full_name() not in users_colors.keys():
            # Получаем следующий цвет из цикла
            users_colors[vac.user.get_full_name()] = next(color_cycle)

    vacations_by_user = {}
    users_otd = User_info.objects.all()
    for vac in filtered_vacations:
        if vac.user.get_full_name() not in vacations_by_user:
            user_info = users_otd.get(user_id=vac.user_id)
            position = user_info.position.position if user_info.position else "Не указана"
            vacations_by_user[vac.user.get_full_name()] = {
                'color': users_colors[vac.user.get_full_name()],
                'dates': [],
                'sum': 0,
                'otd': '',
                'user_id': vac.user_id,
                'position': position,
                'vacation_start_dates': [],
                'vacation_periods': [],
                'in_vacation': False,
            }

            if vac.day_start.date() <= today <= vac.day_end.date():
                vacations_by_user[vac.user.get_full_name()]['in_vacation'] = True

            for u in users_otd:
                if u.user_id == vac.user_id:
                    vacations_by_user[vac.user.get_full_name()]['otd'] = u.otd_number
                    break
        
        start_date = vac.day_start.date()
        days_count = (vac.day_end.date() - vac.day_start.date()).days + 1
        
        # Подсчитываем количество праздничных дней в отпуске (включая выходные и будние)
        holidays_in_vacation = 0
        for y, m_d in holidays.items():
            for m, d in m_d.items():
                for day in d:
                    month_number = get_key_from_dict_by_value(month_num_str, m)
                    holiday_date = today.replace(year=int(y), month=month_number, day=day)

                    # Проверяем, попадает ли праздник в диапазон отпуска
                    if start_date <= holiday_date <= start_date + dt.timedelta(days=days_count - 1):
                        holidays_in_vacation += 1

        # Уменьшаем количество дней отпуска на праздничные дни
        actual_days_count = days_count - holidays_in_vacation

        # Устанавливаем дату окончания, добавляя количество праздничных дней
        end_date = start_date + dt.timedelta(days=actual_days_count + holidays_in_vacation - 1)

        # Обновляем данные пользователя с корректными значениями
        vacations_by_user[vac.user.get_full_name()]['vacation_start_dates'].append((start_date, actual_days_count))

        vacations_by_user[vac.user.get_full_name()]['dates'].append(
            {'d': f"{vac.day_start.day} {month_num_str[vac.day_start.month][:3]} - {vac.day_end.day} {month_num_str[vac.day_end.month][:3]}",
            'vac_id': vac.id,
            }
        )

        vacations_by_user[vac.user.get_full_name()]['sum'] += actual_days_count
        formatted_start = f"{start_date.day} {months_ru[start_date.month]} {start_date.year}"
        formatted_end = f"{end_date.day} {months_ru[end_date.month]} {end_date.year}"
        vacations_by_user[vac.user.get_full_name()]['vacation_periods'].append(f"{formatted_start} - {formatted_end}")

    return render(
        request,
        'vac_all.html',
        {
            'today': today,
            'year': year,
            'otd': otd,
            'len_vacations': len(filtered_vacations),
            'vacations_by_user': vacations_by_user,
            'holidays': holidays.get(year, {}),
            'otds_for_choise': otds_for_choise,
            'otd_users_full_names': [request.user],
            'vacation_start_dates': vacation_start_dates,
            'show_button': True,
            'navbar_style': 'custom-navbar',
            'users_colors': users_colors,
            'bosses': list(bosses.keys()),
        }
    )

def vac_calendars(request, otd, year=None):
    if not vac_access_check(request):
        return render(request, 'no_rights.html')

    current_year = dt.datetime.now().year
    current_user_name = request.user.get_full_name()
    today = dt.datetime.today().date()

    year = request.GET.get('year', current_year)
    year = int(year)

    years_range = [current_year - 1, current_year, current_year + 1]
    years_range.sort(reverse=True)

    # Проверка, является ли пользователь боссом
    if current_user_name not in bosses.keys():
        otd_id = User_info.objects.filter(user_id=request.user.id).first().otd_number_id
        otd_users = User_info.objects.filter(otd_number_id=otd_id)
        otd_users_id = [user.user_id for user in otd_users]
        linked_units = [Unit.objects.filter(id=otd_id).first().description]
    else:
        if otd == 0:
            linked_units = bosses[current_user_name]
            otd_ids = [Unit.objects.filter(description=desc).first().id for desc in linked_units]
        else:
            otd_id = Unit.objects.filter(description=otd).first().id
            linked_units = [otd]
            otd_ids = [otd_id]

        otd_users = User_info.objects.filter(otd_number_id__in=otd_ids)
        otd_users_id = [user.user_id for user in otd_users]

    otds_for_choise = linked_units

    otd_data = []
    units = Unit.objects.filter(description__in=linked_units)
    for unit in units:
        unit_users = User_info.objects.filter(otd_number_id=unit.id)
        unit_user_ids = [user.user_id for user in unit_users]
        vacations_count = Vacation.objects.filter(user_id__in=unit_user_ids, year=str(year)).count()

        if vacations_count > 0:
            otd_data.append({
                'otd': unit.title,
                'otd_description': unit.description,
                'employees': unit_users.count(),
                'vacations': vacations_count
            })

    filtered_years_vacations_count = {}
    for y in years_range:
        filtered_years_vacations_count[y] = Vacation.objects.filter(
            user_id__in=otd_users_id, year=str(y)
        ).count()

    has_vacations_in_linked_units = any(count > 0 for count in filtered_years_vacations_count.values())

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'otd_data': otd_data,
            'linked_units': linked_units,
        })

    return render(
        request,
        'vac_calendars.html',
        {
            **rights(request),
            'today': today,
            'year': year,
            'current_year': current_year,
            'otd': otd,
            'years_vacations_count': filtered_years_vacations_count,
            'otds_for_choise': otds_for_choise,
            'bosses': list(bosses.keys()),
            'current_user_name': current_user_name,
            'navbar_style': 'custom-navbar',
            'show_button': True,
            'years_range': years_range,
            'has_vacations_in_linked_units': has_vacations_in_linked_units,
        }
    )

def vac_my_vacations(request):
    if not vac_access_check(request):
        return render(request, 'no_rights.html')

    today = dt.datetime.today().date()
    year = today.year

    # Получаем все отпуска текущего пользователя, начиная с текущей даты
    vacations = Vacation.objects.filter(
        user_id=request.user.id,
        day_end__gte=today
    ).order_by('day_start')

    # Новый список для хранения отпусков
    vacations_list = []

    for vac in vacations:
        start_date = vac.day_start.date()
        days_count = (vac.day_end.date() - vac.day_start.date()).days + 1

        # Учет праздничных дней
        holidays_in_vacation = sum(
            1
            for y, m_d in holidays.items()
            for m, d in m_d.items()
            for day in d
            if start_date <= today.replace(year=int(y), month=get_key_from_dict_by_value(month_num_str, m), day=day) <= start_date + dt.timedelta(days=days_count - 1)
        )

        actual_days_count = days_count - holidays_in_vacation
        end_date = start_date + dt.timedelta(days=actual_days_count + holidays_in_vacation - 1)

        # Добавляем отпуск в список
        vacations_list.append({
            'period': f"{start_date.day} {months_ru[start_date.month]} {start_date.year} - {end_date.day} {months_ru[end_date.month]} {end_date.year}",
            'days_count': actual_days_count,
            'id': vac.id,
            'is_current': start_date <= today <= vac.day_end.date(),
        })
    
    vacation_year = None
    
    for vacation in vacations_list:
        start_date = vacation['period'].split(' ')[-1]
        vacation_year = int(start_date)
        vacation['vacation_year'] = vacation_year

    return render(
        request,
        'vac_my_vacations.html',
        {
            'today': today,
            'year': year,
            'vacation_year': vacation_year,
            'vacations_list': vacations_list,
            'show_button': True,
            'navbar_style': 'custom-navbar',
            'bosses': list(bosses.keys()),
            'show_my_vacations': True,
        }
    )

def vac_all_vacations(request):
    today = dt.datetime.today()
    current_year = today.year
    year_range = range(current_year - 1, current_year + 2)

    selected_otd = request.GET.get('otd', '') 
    selected_user = request.GET.get('user', '')
    selected_year = request.GET.get('year', '')

    current_user_name = request.user.get_full_name()
    filters = {}
    user_colors = {}

    if current_user_name in bosses:
        boss_departments = bosses[current_user_name]
        boss_departments = [str(department) for department in boss_departments]
        department_ids = Unit.objects.filter(description__in=boss_departments).values_list('id', flat=True)
        filters['user__user_info__otd_number_id__in'] = department_ids

    if selected_otd:
        otd = Unit.objects.filter(title=selected_otd).first()
        if otd:
            filters['user__user_info__otd_number_id'] = otd.id

    if selected_user:
        name_parts = selected_user.split()
        if len(name_parts) == 2:
            filters['user__first_name'] = name_parts[0]
            filters['user__last_name'] = name_parts[1]

    if selected_year:
        filters['year'] = selected_year

    vacations = Vacation.objects.filter(**filters)

    vacation_count = vacations.count()

    otds_for_choise = Unit.objects.all()
    if current_user_name in bosses:
        otds_for_choise = otds_for_choise.filter(description__in=bosses[current_user_name])
        department_ids = Unit.objects.filter(description__in=bosses[current_user_name]).values_list('id', flat=True)
        users_for_filter = User.objects.filter(user_info__otd_number_id__in=department_ids)
    else:
        users_for_filter = User.objects.all()

    years_vacations_count = {}
    for year in year_range:
        year_filters = filters.copy()
        
        if 'year' in year_filters:
            del year_filters['year']
        
        year_filters['year'] = str(year)

        years_vacations_count[year] = Vacation.objects.filter(**year_filters).count()

    # Список отпусков с подсчитанными днями и периодами
    vacations_list = []
    for vac in vacations:
        start_date = vac.day_start.date()
        days_count = (vac.day_end.date() - vac.day_start.date()).days + 1

        holidays_in_vacation = sum(
            1
            for y, m_d in holidays.items()
            for m, d in m_d.items()
            for day in d
            if start_date <= today.replace(year=int(y), month=get_key_from_dict_by_value(month_num_str, m), day=day).date() <= start_date + dt.timedelta(days=days_count - 1)
        )

        actual_days_count = days_count - holidays_in_vacation
        end_date = start_date + dt.timedelta(days=actual_days_count + holidays_in_vacation - 1)

        user_info = vac.user.user_info.first()
        department = user_info.otd_number.title if user_info and user_info.otd_number else 'Не указан'

        user_name = vac.user.get_full_name()
        if user_name not in user_colors:
            user_colors[user_name] = next(color_cycle)

        # Добавляем отпуск в список
        vacations_list.append({
            'user': vac.user.get_full_name(),
            'period': f"{start_date.day} {months_ru[start_date.month]} {start_date.year} - {end_date.day} {months_ru[end_date.month]} {end_date.year}",
            'days_count': actual_days_count,
            'id': vac.id,
            'is_current': start_date <= today.date() <= vac.day_end.date(),
            'department': department,
            'color': user_colors[user_name],
        })

    return render(
        request,
        'vac_all_vacations.html',
        {
            **rights(request),
            'today': today,
            'year': selected_year,
            'otds_for_choise': otds_for_choise,
            'users_for_filter': users_for_filter,
            'vacations': vacations_list,
            'selected_otd': selected_otd,
            'selected_user': selected_user,
            'selected_year': selected_year,
            'year_range': year_range,
            'years_vacations_count': years_vacations_count,
            'show_button': True,
            'navbar_style': 'custom-navbar',
            'bosses': list(bosses.keys()),
            'show_all_vacations': True,
            'vacation_count': vacation_count,
        }
    )

def vacation_detail(request, vac_id):
    if not vac_access_check(request):
        return render(request, 'no_rights.html')

    current_user_name = request.user.get_full_name()

    if current_user_name not in bosses:
        vacation = get_object_or_404(Vacation, id=vac_id, user_id=request.user.id)
    else:
        # Получаем список отделов, которые под управлением босса
        boss_departments = bosses[current_user_name]

        boss_departments = [str(department) for department in boss_departments]

        department_ids = Unit.objects.filter(description__in=boss_departments).values_list('id', flat=True)

        allowed_users = User_info.objects.filter(otd_number_id__in=department_ids).values_list('user_id', flat=True)

        if not allowed_users:
            raise Http404("No users found for this boss's departments.")

        vacation = get_object_or_404(Vacation, id=vac_id, user_id__in=allowed_users)

    vacation_user_name = vacation.user.get_full_name()

    # Дальнейшая обработка отпуска
    start_date = vacation.day_start.date()
    end_date = vacation.day_end.date()
    total_days = (end_date - start_date).days + 1

    holidays_in_vacation = sum(
        1
        for year, months in holidays.items()
        for month, days in months.items()
        for day in days
        if start_date <= dt.date(int(year), get_key_from_dict_by_value(month_num_str, month), day) <= end_date
    )

    actual_days_count = total_days - holidays_in_vacation
    adjusted_end_date = start_date + dt.timedelta(days=actual_days_count + holidays_in_vacation - 1)

    from_page = request.GET.get('from', None)
    year = vacation.day_start.year

    return render(
        request,
        'vacation_detail.html',
        {
            'start_date': start_date.strftime('%d.%m.%Y'),
            'end_date': adjusted_end_date.strftime('%d.%m.%Y'),
            'days_count': actual_days_count,
            'vacation_user_name': vacation_user_name,
            'show_button': True,
            'vacation': vacation,
            'navbar_style': 'custom-navbar',
            'bosses': list(bosses.keys()),
            'show_vacation_detail': True,
            'from_page': from_page,
            'year': year,
        }
    )

@login_required
def vacation_new(request, year):
    if not vac_access_check(request):  # Проверяем доступ к отпуску
        return render(request, 'no_rights.html')

    # Инициализация формы и модели отпуска
    vacation = Vacation(user_id=request.user.id)
    form = VacationForm(request.POST or None, files=request.FILES or None, instance=vacation)

    # Определяем, является ли пользователь боссом
    current_user_name = request.user.get_full_name()
    is_boss = current_user_name in bosses

    employees = None

    employee_name = request.GET.get('employee_name', None)

    if is_boss:
        boss_departments = bosses[current_user_name]
        department_ids = Unit.objects.filter(description__in=boss_departments).values_list('id', flat=True)
        employees = User_info.objects.filter(otd_number_id__in=department_ids).select_related('user', 'position')

    selected_employee_name = current_user_name
    
    if form.is_valid():
        vac = form.save(commit=False)

        if is_boss and 'employee' in request.POST:
            selected_employee_id = request.POST['employee']
            vac.user_id = selected_employee_id
            selected_employee_name = User.objects.get(id=selected_employee_id).get_full_name()
        else:
            vac.user_id = request.user.id

        if vac.day_end:
            # Если дата окончания введена вручную, используем ее как есть
            vac.day_end += timedelta(days=1)
        elif vac.day_start and vac.how_long:
            # Если указана дата начала и длительность отпуска, рассчитываем дату окончания
            current_date = vac.day_start
            remaining_days = int(vac.how_long)

            while remaining_days > 0:
                current_date += timedelta(days=1)
                if current_date not in holidays:
                    remaining_days -= 1

            vac.day_end = current_date 
        elif vac.day_start and vac.day_end:
            # Если указаны обе даты, рассчитываем количество рабочих дней
            delta_days = (vac.day_end - vac.day_start).days
            working_days = 0
            current_date = vac.day_start

            while current_date < vac.day_end:
                if current_date not in holidays:
                    working_days += 1
                current_date += timedelta(days=1)

            vac.how_long = working_days

        if vac.day_start:
            vac.day_start += timedelta(days=1)

        vac.save()

        if employee_name:
            return redirect('vac_2', year=year, otd=0)
        elif 'employee' in request.POST and request.POST['employee'] != str(request.user.id):
            return redirect(f'{reverse("vac_all_vacations")}?user={selected_employee_name}')
        else:
            return redirect('vac_my_vacations')

    current_holidays = holidays.get(year, {})
    holidays_json = json.dumps(current_holidays)
    
    context = {
        'form': form,
        'user': request.user,
        'employees': employees,
        'is_boss': is_boss,
        'navbar_style': 'custom-navbar',
        'bosses': list(bosses.keys()),
        'year': year,
        'show_person': True,
        'holidays_json': holidays_json,
        'employee_name': employee_name,
    }

    return render(request, 'vacation_new.html', context)

@login_required
def vacation_edit(request, year, vac_id):
    if not vac_access_check(request):  
        return render(request, 'no_rights.html')

    vac = get_object_or_404(Vacation, id=vac_id)

    if vac.day_start and vac.day_end:
        delta_days = (vac.day_end - vac.day_start).days
        working_days = 0
        current_date = vac.day_start

        while current_date <= vac.day_end:
            if current_date not in holidays.get(year, []): 
                working_days += 1
            current_date += timedelta(days=1)

        vac.how_long = working_days

    vac.day_start = str(vac.day_start)[:-15]
    vac.day_end = str(vac.day_end)[:-15]

    form = VacationForm(request.POST or None, files=request.FILES or None, instance=vac)

    # Получаем имя и должность сотрудника, связанного с текущим отпуском
    employee_name = vac.user.get_full_name()
    employee_position = None
    if hasattr(vac.user, 'user_info'):
        user_info = vac.user.user_info.first() 
        if user_info and user_info.position:
            employee_position = user_info.position.position

    if form.is_valid():
        vac = form.save(commit=False)

        if vac.day_end:
            vac.day_end += timedelta(days=1)
        elif vac.day_start and vac.how_long:
            current_date = vac.day_start
            remaining_days = int(vac.how_long)

            while remaining_days > 0:
                current_date += timedelta(days=1)
                if current_date not in holidays.get(year, []): 
                    remaining_days -= 1

            vac.day_end = current_date
        elif vac.day_start and vac.day_end:
            delta_days = (vac.day_end - vac.day_start).days
            working_days = 0
            current_date = vac.day_start

            while current_date < vac.day_end:
                if current_date not in holidays.get(year, []):  
                    working_days += 1
                current_date += timedelta(days=1)

            vac.how_long = working_days

        if vac.day_start:
            vac.day_start += timedelta(days=1)

        if vac.day_start >= vac.day_end:
            return render(
                request,
                'vacation_edit.html',
                {
                    'form': form,
                    **rights(request),
                    'vac_id': vac_id,
                }
            )

        vac.save()
        from_param = request.GET.get('from')

        if from_param == 'calendars':
            return redirect('vac_2', year=year, otd=0)
        elif from_param == 'all_vacations':
            return redirect(f'{reverse("vac_all_vacations")}?user={employee_name}')
        else:
            return redirect('vac_my_vacations')

    current_holidays = holidays.get(year, {})
    holidays_json = json.dumps(current_holidays)
    
    return render(
        request,
        'vacation_edit.html',
        {
            'form': form,
            'user': request.user,
            'edit': True,
            **rights(request),
            'vac_id': vac_id,
            'year': year,
            'value': vac,
            'employee_name': employee_name,
            'employee_position': employee_position, 
            'navbar_style': 'custom-navbar',
            'bosses': list(bosses.keys()),
            'redact_vac': True,
            'show_button': True,
            'holidays_json': holidays_json,
        }
    )

@login_required
def vacation_delete(request, vac_id):
    if not vac_access_check(request):
        return render(request, 'no_rights.html',)
    
    redirect_from = request.GET.get('from', None)

    vac = get_object_or_404(Vacation, id=vac_id)
    year = vac.day_start.year
    vac.delete()

    if redirect_from == 'calendars':
        return redirect('vac_2', year=year, otd=0)
    elif redirect_from == 'all_vacations':
        return redirect('vac_all_vacations') 
    else:
        return redirect('vac_my_vacations')