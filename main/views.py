from django.shortcuts import render ,redirect
from django.urls import reverse
from bs4 import BeautifulSoup as bs
from django.http import HttpResponseRedirect
import requests
from . models import *
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User , auth
from django.contrib import messages



def clear(request):
    
    News_data.objects.all().delete()
    
    return HttpResponseRedirect(reverse("xeber_panel"))


def xeber_panel(request):

    news = News_data.objects.all()
    
    count = News_data.objects.all().count()
    
    context = {
        
        'news': news,
        'count': count,
        
        
    }
    return render(request, "main/xeber_panel.html",context)



def news_bot(request):

    data = requests.get("https://lent.az")

    url = bs(data.text,"html.parser")

    soup = url.find("div",class_ = "all-news-wrapper")

    for x in soup:
        
        
        try:
            
            link = x["href"]
            
            data1 = requests.get(link)
            
            soup1 = bs(data1.text,"html.parser")
            
            category = soup1.find("div",class_ = "breadcrumb_row").find('h3').text
            
            date = soup1.find("div",class_ = "overlay").text.replace("(UTC +04:00)","")
            
            title = soup1.find("h1",class_ = "news_title").text
            
            text = soup1.find("div",class_ = "news_content").text
          
            image = soup1.find("div",class_ = "news_img").find("img")
            
            image = image["src"]
            
            weather = soup1.find("div",class_ = "top_section").find_all("li")[3].text            

            News_data(text=text,title=title,date=date,category=category,weather=weather,img=image).save()

        except:TypeError
        

    return HttpResponseRedirect(reverse("xeber_panel"))


def home(request):
    
    idman = News_data.objects.raw("SELECT * FROM main_news_data WHERE category == 'İDMAN' ")
    
    category = Test.objects.all().distinct()
    
    latest = News_data.objects.all()[3:7]
    
    news01 = News_data.objects.all()[0:1]
    
    news02 = News_data.objects.all()[1:3]

    data = News_data.objects.all()[0:4]
    food = News_data.objects.all()[4:7]
    news03 = News_data.objects.all()[3:4]
    news04 = News_data.objects.all()[4:8]
    news05 = News_data.objects.all()[2:3]
    news06 = News_data.objects.all()[7:8]
    news07 = News_data.objects.all()[9:13]
    news08 = News_data.objects.all()[13:14]
    news09 = News_data.objects.all()[14:15]
    news10 = News_data.objects.all()[6:10]
    context = {
        
        "data":data,
        'news01':news01,
        "news02":news02,
        "news03":news03,
        "news04":news04,
        "news05":news05,
        "news06":news06,
        "news07":news07,
        "news08":news08,
        "news09":news09,
        "news10":news10,
        "latest":latest,
        'category':category,
        "idman":idman,
        "food":food,
        
        
        
    }
    return render(request,"main/home.html",context)


def news_single(request,id):
    
    news = News_data.objects.filter(id=id)
    
    context = {
        
        'news':news
        
    }
    return render(request,"main/news-single.html",context)


def about(request):
    
    return render(request,"main/about.html")



def contact(request):
    
    return render(request,"main/contact.html")

def login(request):
    
    if request.method == 'POST':
        form = News_data(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        
        
        user =  authenticate(username=username, password = password,request=request)
        
        if user is not None:
            auth.login(request,user)
            if not request.POST.get('remember_me'):
                request.session.set_expiry(0)
            return redirect('home')
           
    else:
        form = News_data   
    
    return render( request, 'main/login.html',{'form':form})


def register(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['pass1']
        password2 = request.POST['pass2']
    
        if password1 == password2:
            
            if User.objects.filter(username=username).exists():
                
                messages.info(request, 'This username alredy exists!!')
                
            else:
                
                User.objects.create_user(username=username,email=email, password=password1)
                return redirect('login')
                
        else: 
            messages.info(request, 'Passwords are not same!!')
    
    
            
    return render( request , 'main/register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')