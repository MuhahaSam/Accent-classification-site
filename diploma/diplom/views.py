from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from .forms import *
from django.contrib.auth import authenticate
from django.conf import settings
import os
from .DataProcss import *
from os.path import join
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages



# Create your views here.
class Base(View):
    def get(self, request):
        return render(request, 'base.html', context = {})

class AccentC(View):
    def get(self, request):
        return render(request, 'AccentC.html')

class New_user(View):
    def get(self, request):
        userf = UserForm
        return render(request, 'registr.html',  context={'form': userf})

    def post(self, request):
        bound_form = UserForm(request.POST)
        if bound_form.is_valid():
            bound_form.save()
            return HttpResponseRedirect('/')
        return render(request, 'registr.html', context={'form': bound_form, 'error':True})




class Login(View):

    def get(self, request):
        return render(request, 'base.html')

    def post(self, request):
        user = authenticate(username=request.POST.get('login'), password=request.POST.get('passwd'))
        if user is not None:
            login(request,user)
            request.session['user'] = request.POST.get('login')
            return render(request, 'audio.html', context={'error': False})
        return HttpResponseRedirect('/')

class Audio(View):
    def get(self, request):
        data = Data
        return render(request, 'audio.html', context={'error':False})

    def post(self, request):
        if (request.FILES.get('file') is not None) and ('.wav' in request.FILES.get('file').name):
            logined_user = User.objects.get(username=request.session['user'])
            data = Data(record=request.FILES.get('file'), data_id = logined_user)
            data.save()
            for i in Data.objects.all():
                last_one = i.record.path
                request.session['last_one'] = last_one
                break
            data_cut = AccentRec(last_one)
            mask = data_cut.energy(0.001)
            indexes = data_cut.index_selecting(mask)
            indexes = data_cut.delete_to_short(indexes)
            request.session['indexes'] = indexes.tolist()
            #print('\n')
            #print(request.session['indexes'])
            request.session['file_name'] = str(request.FILES.get('file').name[:-4])
            return HttpResponseRedirect('dproc')
        return render(request, 'audio.html', context={'error':True})

class DataCutting(View):
    def get(self, request):
        indexes = np.array(request.session['indexes'])
        last_one = request.session['last_one']
        data_cut = AccentRec(last_one)
        data_cut.setense_split(indexes, request.session['file_name'])
        return HttpResponseRedirect('class')

class DataPredict(View):
    def get(self, request):
        datas = os.scandir(join(settings.MEDIA_ROOT, 'spectogram'))
        model = load_model(join(settings.MEDIA_ROOT, 'model', 'CNN Sam two.h5'))
        dpath = join(settings.MEDIA_ROOT,'spectogram')
        df = os.listdir(dpath)
        data_gen = Image_bath_gen(df, 3, dpath)
        result = model.predict(data_gen)
        accent = round(np.mean(result)*100, 3)
        logined_user = User.objects.get(username=request.session['user'])
        memory = Result(result=accent, data_id=logined_user)
        memory.save()
        with datas as data:
            for i in data:
                os.remove(i)
        return render(request, 'dprocss.html', context={'accent':accent})


class History(View):
    def get(self, request):
        history = Result.objects.all()
        return render(request, 'history.html', context={'his':history})


class Logout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')





class Classificate(View):
    def get(self, request):
        render(request, 'AccentC.html')
















    #def post(self, request):








