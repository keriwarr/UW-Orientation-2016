from django.shortcuts import render

def index(request):
    data = getData()
    return render(request, 'home/index.html', context=data)

def news(request):
    data = getData()
    data.update({
        'page': {
            'title': 'News and Announcements'
        }
    })
    return render(request, 'home/news.html', context=data)

def about(request):
    data = getData()
    data.update({
        'page': {
            'title': 'About Orientation'
        }
    })
    return render(request, 'home/about.html', context=data)

def resources(request):
    data = getData()
    data.update({
        'page': {
            'title': 'Resources'
        }
    })
    return render(request, 'home/resources.html', context=data)

def faq(request):
    data = getData()
    data.update({
        'page': {
            'title': 'FAQ'
        }
    })
    return render(request, 'home/faq.html', context=data)

def getData():
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
