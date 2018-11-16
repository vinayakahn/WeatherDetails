from django.shortcuts import render
from django.http import HttpResponseRedirect
import requests
from .models import City
from .forms import CityForm

from django.urls import reverse
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def user_login(request):
	context={}
	if request.method == 'POST':
		username=request.POST['username']
		password=request.POST['password']
		user = authenticate(request,username=username,password=password)

		if user:
			login(request, user)
			return HttpResponseRedirect('/weather/weather.html')
		else:
			context["error"]="Provide valid credentials !!!"
			return render(request, 'weather/login.html',context)


	else:
		return render(request, 'weather/login.html',context)



def user_success(request):
	context={}
	context["user"]= request.user
	return render(request, 'weather/weather.html',context)


#Below is Weather report saving code
def index(request):
	url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=eb2852a2e040ab598ac2e7942ca4575b'
	
	if request.method == 'POST':
		form = CityForm(request.POST)
		form.save()

	form = CityForm()	

	cities = City.objects.all()
	weather_data = []

	for city in cities:

		r = requests.get(url.format(city)).json()

		#print(r)

		city_weather = {

				'city' :city ,
				'temperature' : r['main']['temp'],
				'description' : r['weather'][0]['description'],
				'icon' : r['weather'][0]['icon'],
				
		}

		weather_data.append(city_weather)

		#print(weather_data)

	#print(city_weather)

	context={'weather_data' : weather_data, 'form' : form}
	return render(request,'weather/weather.html',context)	
