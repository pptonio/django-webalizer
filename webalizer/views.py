import os
from django.conf import settings
from django.shortcuts import render
from django.views.static import serve
from django.contrib.admin.views.decorators import staff_member_required
from BeautifulSoup import BeautifulSoup as soup




@staff_member_required    
def proxy(request, path):
    """
    Answer requests for webalizer images and monthly reports.
    If an image is requested let django's static.serve view do the work,
    if an html file is requested just insert the content of
    the <body> into the django template.
    
    """
    context = {'title': 'Webalizer'}
    if path is None or path is u'':
        path = 'index.html'
    if settings.WEBALIZER_DIR is not None:
        if path.endswith('.png'): # webalizer generates png images
            return serve(request, path, document_root=settings.WEBALIZER_DIR)
        else:
            try:
                webalizer_index = open(os.path.join(settings.WEBALIZER_DIR, path)).read()
                webalizer_soup = soup(webalizer_index)
                context.update({'data': ' '.join([unicode(x) for x in webalizer_soup.body.contents])})
            except:
                context.update({'data': None})
    return render(request, 'webalizer/index.html', context) 
