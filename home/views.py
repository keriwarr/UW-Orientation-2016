from django.shortcuts import render
from django.conf import settings
from datetime import datetime
import requests
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

def index(request):
    data = getData()
    news = getNews(limit = 1)
    latestnews = False

    if 'data' in news and len(news['data']) > 0:
        latestnews = news['data'][0]

    data.update({
        'latestnews': latestnews
    })

    return render(request, 'home/index.html', context=data)

def news(request):
    data = getData()
    news = getNews()

    if 'error' in news or 'data' not in news:
        # TODO: We should probably notify someone about this
        logger.error('Could not load news from the Facebook API')
        raise Exception("Could not load news at this time. Please try again later.")

    data.update({
        'page': {
            'title': 'News and Announcements',
            'news': news['data']
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
            'title': 'Frequently Asked Questions'
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

# TODO: Use a proper Facebook API client instead
def getNews(limit = 15):
    params = {
        'access_token': "%s|%s" % (settings.FACEBOOK_APP_ID, settings.FACEBOOK_APP_SECRET),
        'limit': limit,
        'format': 'json',
        'since': "%d-01-01" % datetime.now().year,
        'fields': ','.join([
            'message',
            'created_time',
            'permalink_url',
            'link',
            "attachments{%s}" % ','.join([
                'media',
                'url',
                'title',
                'type'
            ]),
        ])
    }

    # Get results from the Official Math Orientation Facebook page
    # https://www.facebook.com/MathOrientation/
    r = requests.get('https://graph.facebook.com/v2.7/176229899139398/feed', params = params)
    return r.json()
