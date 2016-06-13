from django.shortcuts import render

def index(request):
    return render(request, 'home/index.html', context=data())

def data():
    return {
        'site': {
            'title': 'Math Orientation 2016',
            'email': 'mathorientation@uwaterloo.ca',
            'description': """
                Official website of the Univeristy of Waterloo Math Faculty Orientation Week
            """,
            'baseurl': "", # the subpath of your site, e.g. /blog
            'url': "http://orientation.math.uwaterloo.ca/", # the base hostname & protocol for your site
            'twitter_username': 'MATHOrientation',
        }
    }
