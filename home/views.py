from django.shortcuts import render

def index(request):
    return render(request, 'home/index.html', context=data())

def news(request):
    return render(request, 'home/news.html', context=data())

def about(request):
    return render(request, 'home/about.html', context=data())

def resources(request):
    return render(request, 'home/resources.html', context=data())

def faq(request):
    return render(request, 'home/faq.html', context=data())

def contact(request):
    return render(request, 'home/contact.html', context=data())

def data():
    return {
        'site': {
            'title': 'Math Orientation 2016: Mathemagical Kingdoms',
            'email': 'mathorientation@uwaterloo.ca',
            'description': """
                Official website of the Univeristy of Waterloo Math Faculty Orientation Week
            """,
            'baseurl': "", # the subpath of your site, e.g. /blog
            'url': "http://orientation.math.uwaterloo.ca/", # the base hostname & protocol for your site
            'twitter_username': 'MATHOrientation',
        }
    }
