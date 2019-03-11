import  json , sys, time
import paho.mqtt.client as mqtt
import subprocess
import threading
from multiprocessing import process
# from rest_framework import serializers
from django.shortcuts import render
from django.http import HttpResponseRedirect
# from .forms import HomeForm, SnippetForm, UserReqForm
from .forms import HomeForm
# Create your views here.

posts = [ {
            'author': 'vikas',
        'title': 'blog post 1',
        'content': 'my first article on the blog',
        'date_posted': 'August 27, 2018'
    },
    {
        'author': 'bharat',
        'title': 'blog post 2',
        'content': 'Cooooooool..........',
        'date_posted': 'August 28, 2018'
    }
]
def register(request):

    return render(request,'blog/register.html')

def login(request):

    return render(request,'blog/login.html')



def home(request):
    # context = {
    #     'posts': posts
    # }
    if request.method == 'POST' :
        form = HomeForm(request.POST)
        if form.is_valid():
            # name = form.cleaned_data['name']
            # email = form.cleaned_data['email']
            # status = form.cleaned_data['status']
            # print(name)
            # print(status)
            with open('file.json', 'w') as f:
                json.dump(form.cleaned_data, f)

    else:
        form = HomeForm()

    return render(request, 'blog/test4.html', {'form': form})


def Snippet_detail(request):
    if request.method == 'POST' :
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()

    else:
       form = SnippetForm()
    return render(request, 'blog/home.html', {'form': form})


def UserReq_detail(request,):
    if request.method == 'POST' :
        form = UserReqForm(request.POST)
        if form.is_valid():
            print("valid")
            form.save()
            with open('file.json', 'w') as f:
                json.dump(form.cleaned_data, f)

        else:
            print('not valid')
            with open('file.json', 'w') as f:
                json.dump(form.cleaned_data, f)
    else:
        form = UserReqForm()

    return render(request, 'blog/test5.html', {'form': form})




def about(request):
    # return HttpResponse('<h1> Blog about </h1>')


    # print(status)
    return render(request, 'blog/about.html', {'title': 'About'})





def startlogging( data ):


    process = subprocess.Popen(["python", "/home/vikas/git/django_project/monitor/userReq.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout = process.communicate(str.encode(data))[0]
    time.sleep(2)
    process.kill()
    # sta = 'STDOUT:{}'.format(stdout)

    # pid = subprocess.Popen(["python", "/home/vikas/Desktop/Desk/userReq.py"]).pid

    # pidid = str(process)

    # with open('userReqSubprocess.pid_file', "w") as f:
    #     wtrite_data = f.write(pidid)
    #     f.close()
    return stdout


# def renderit(request,str):


def dict_to_binary(the_dict):
    str = json.dumps(the_dict, cls=JSONEncoder)
    binary = ' '.join(format(ord(letter), 'b') for letter in str)
    return binary

def start(request):
    if request.method == 'POST' :
        form = HomeForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            print('is valid')
            # name = form.cleaned_data['name']
            # email = form.cleaned_data['email']
            # status = form.cleaned_data['status']
            # print(name)
            # print(status)
            # with open('file.json', 'w') as f:
            #     json.dump(form.cleaned_data, f, cls=JSONEncoder)
            #     f.close()
            # print(form.cleaned_data)
            bin = dict_to_binary(form.cleaned_data)
            # print(type(bin))
            # print('this is binary '+bin)

            stdout = startlogging(bin)
            str = stdout.decode("utf-8")
            typ = type(str)
            # st = stdout.str()
            # s = stdout.split("\n")
            d = 11
            context= {
                'a': stdout[:40].decode("utf-8"),
                'b': stdout[40:81].decode("utf-8"),
                'c': stdout[81:125].decode("utf-8"),
                'd': stdout[125:180].decode("utf-8"),
                'e': stdout[180:223].decode("utf-8"),
                'f': stdout[223:].decode("utf-8"),
                'form': form,
                'color': 'white',
                }
        else:
            print('not valid')
            context= {
                'a': "- You have entered invalid data",
                'b': '- Enter the values properly',
                'c': '',
                'd': '',
                'form': form,
                'color': 'red'
                }
            # return render(request, 'blog/test4.html', context)
        # status = form.cleaned_data['status']
        # print(status)
        # with open('file.json', 'w') as f:
        #         json.dump(form.cleaned_data, f)

    else:
        form = HomeForm()
        context = {'form': form}
    # return HttpResponseRedirect('/')


    return render(request, 'blog/test4.html', context)

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'isoformat'): #handles both date and datetime objects
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)
