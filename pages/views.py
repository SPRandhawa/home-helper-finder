from django.shortcuts import render

def home(request):
	return render(request, 'pages/home.html', {'active_page': 'home'})


def about(request):
	return render(request, 'pages/about.html', {'active_page': 'about'})


def contact(request):
	return render(request, 'pages/conatct.html', {'active_page': 'contact'})


def help_guide(request):
	return render(request, 'pages/help.html', {'active_page': 'help'})


def search(request):
	query = request.GET.get('q', '').strip()
	return render(request, 'pages/search.html', {'query': query, 'active_page': 'search'})
