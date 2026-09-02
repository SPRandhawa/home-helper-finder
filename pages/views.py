from django.shortcuts import render
from .forms import ContactForm

def home(request):
	return render(request, 'pages/home.html', {'active_page': 'home'})


def about(request):
	return render(request, 'pages/about.html', {'active_page': 'about'})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'contact.html', {'success': True})
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def help_guide(request):
	return render(request, 'pages/help.html', {'active_page': 'help'})


def search(request):
	query = request.GET.get('q', '').strip()
	return render(request, 'pages/search.html', {'query': query, 'active_page': 'search'})


def privacy(request):
	return render(request, 'pages/privacy.html', {'active_page': 'privacy'})
