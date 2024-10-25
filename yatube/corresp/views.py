from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from .forms import CorrespForm, WhoForm
from .models import Corresp, Who
from django.conf import settings
import os
import datetime as dt
from users.models import User_info

# функционал для очистки базы от выполненых бекграунд задач
# from background_task.models import Task
# from background_task.models import CompletedTask
rights = {
    'rights': settings.RIGHTS,
    'storage_rights': settings.STORAGE_RIGHTS,
    'sadec_rights': settings.SADEC_RIGHTS,
    'pro_rights': settings.PRO_RIGHTS,
    'page_name': 'Корреспонденция',
}
urls = {'corresp_urls': {'all_corresp', 'corresp_new', }, }



def corr_access_check(request):
    return get_object_or_404(User_info, user_id=request.user.id).corr_access


# Главная страница
def all_corresp(request):
    if not corr_access_check(request):
        return render(request, 'no_rights.html',)

    corresps = Corresp.objects.all()
    paginator = Paginator(corresps, settings.POSTS_IN_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    #print(len(CompletedTask.objects.all()))
    #if len(CompletedTask.objects.all()) > 200:
    #    CompletedTask.objects.filter(id__lt=CompletedTask.objects.latest('id').id - 200).delete()
    #print(len(CompletedTask.objects.all()))
    return render(
        request,
        'corresp.html', {
            **rights,
            **urls,
            'page_name': 'Корреспонденция',
            'page': page,
        }
    )


def all_corresp_sort(request, cor_type_id,  in_out_id):
    if not corr_access_check(request):
        return render(request, 'no_rights.html',)

    corresps = Corresp.objects.filter(in_out_id=in_out_id, cor_type_id=cor_type_id)
    paginator = Paginator(corresps, settings.POSTS_IN_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'corresp.html', {
            **rights,
            **urls,
            'page_name': 'Корреспонденция',
            'page': page,
        }
    )


@login_required
def corresp_new(request, cor_type_id):
    if not corr_access_check(request):
        return render(request, 'no_rights.html',)

    cor_types = {1:'СЗ', 2:'Письмо', 3:'Меморандум',}

    cor = Corresp()
    cor.cor_type_id = cor_type_id
    cor.author = request.user
    form = CorrespForm(
        request.POST or None,
        files=request.FILES or None,
        instance=cor
    )

    if form.is_valid():
        cor = form.save(commit=False)
        cor.day += dt.timedelta(days=1)
        cor.save()
        return redirect('all_corresp')
    return render(
        request,
        'corresp_new.html', {
            'page_name': 'Корреспонденция',
            'form': form,
            'types': cor_types[cor_type_id],
            **rights, **urls,
        }
    )

@login_required
def who_new(request):
    if not corr_access_check(request):
        return render(request, 'no_rights.html',)

    cor_types = {1:'СЗ', 2:'Письмо', 3:'Меморандум',}

    form = WhoForm(
        request.POST or None,
        files=request.FILES or None,
    )

    if form.is_valid():
        form.save()
        return redirect('all_corresp')
    return render(
        request,
        'corresp_new.html', {
            'page_name': 'Корреспонденция',
            'form': form,
            **rights, **urls,
        }
    )

@login_required
def corresp_delete(request, cor_id):
    if not corr_access_check(request):
        return render(request, 'no_rights.html',)

    cor = Corresp.objects.filter(id=cor_id)[0]  
    cor_path = settings.BASE_DIR + "/posts/static" + str(cor.file.url)
    try:
        os.remove(cor_path)
    except:
        print('file problem')
    cor.delete()
    return redirect('all_corresp')


@login_required
def corresp_edit(request, cor_id):
    if not corr_access_check(request):
        return render(request, 'no_rights.html',)

    cor = get_object_or_404(Corresp, id=cor_id)
    cor.day = str(cor.day)[:-15]

    form = CorrespForm(
        request.POST or None,
        files=request.FILES or None,
        instance=cor
    )

    if form.is_valid():
        cor = form.save(commit=False)
        cor.day += dt.timedelta(days=1)
        cor.save()
        return redirect('all_corresp')
    return render(
        request,
        'corresp_new.html',
        {
            'form': form,
            'page_name': 'Корреспонденция',
            'edit': True,
            **rights, **urls,
        }
    )