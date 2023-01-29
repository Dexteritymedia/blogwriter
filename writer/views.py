from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .functions import *

# Create your views here.

@login_required
def home(request):
    if request.method == 'POST' and 'outline' in request.POST:
        title = request.POST['title']
        audience = request.POST['audience']
        blog_outline = generateblogoutline(audience, title)
        if blog_outline:
            request.session['blog_outline'] = blog_outline
        else:
            messages.error(request, 'Oops we could not generate any blog outline for you, please try again.')
        
        if 'blog_outline' in request.session:
            pass
        else:
            
            messages.error(request, 'Start by asking a question')

        context = {}
        context['blog_outline'] = request.session['blog_outline']
        return render(request, 'home.html', context)
    
    if request.method == "POST" and "post" in request.POST:
        outline = request.session['title']
        blog_post = generateblogpost(outline)
        if blog_post:
            request.session['blog_post'] = blog_post
        else:
            messages.error(request, 'Oops we could not generate any blog post for you, please try again.')
        
        if 'blog_post' in request.session:
            pass
        else:
            
            messages.error(request, 'Start by asking a question')

        context = {}
        context['blog_post'] = request.session['blog_post']
        return render(request, 'home.html', context)
        

    return render(request, 'home.html',)
