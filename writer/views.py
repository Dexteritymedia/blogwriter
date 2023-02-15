from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .functions import *

# Create your views here.

@login_required
def home(request):
    if request.method == 'POST' and 'outline' in request.POST:
        title = request.POST['title']
        audience = request.POST['audience']
        if title and audience:
            request.session['title'] = title
            request.session['audience'] = audience
            print(request.session['title'])
        else:
            pass
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
        context['title'] = request.session['title']
        context['audience'] = request.session['audience']
        print(request.session['blog_outline'])
        return render(request, 'home.html', context)

    if request.method == 'POST' and 'retry' in request.POST:
        title = request.session.get('title')
        audience = request.session.get('audience')
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
        print(request.session['blog_outline'])
        return render(request, 'home.html', context)
    
    if "post" in request.POST:
        outline = request.session['blog_outline']
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

    if "meta" in request.POST:
        title = title
        print(title)
        meta_description = generatemetadescription(outline)
        if meta_description:
            request.session['meta_description'] = meta_description
        else:
            messages.error(request, 'Oops we could not generate any meta description for you, please try again.')
        
        if 'meta_description' in request.session:
            pass
        else:
            
            messages.error(request, 'Start by asking a question')

        context = {}
        context['meta_description'] = request.session['meta_description']
        return render(request, 'home.html', context)
        

    return render(request, 'home.html',)

@login_required
def retry_outline(request):
    if request.session['title'] and request.session['audience']:
        title = request.session['title']
        audience = request.session['audience']
        blog_outline = generateblogoutline(audience, title)
    if blog_outline:
        request.session['blog_outline'] = blog_outline
    context = {}
    context['blog_outline'] = request.session['blog_outline']
    return render(request, 'home.html', context)

@login_required
def blogpost(request):

    if request.session['blog_outline']:
        try:
            
            outline = request.session['blog_outline']
            blog_post = generateblogpost(outline)
        except KeyError:
            
            messages.error(request, 'Oops we could not generate any blog post for you, please try again.')
            return redirect('home')
    
    if blog_post:
        request.session['blog_post'] = blog_post
    else:
        messages.error(request, 'Oops we could not generate any blog post for you, please try again.')
        return redirect('home')
        
    if 'blog_post' in request.session:
        pass
    else:     
        messages.error(request, 'Start by creating a blog outline')
        return redirect('home')

    context = {}
    context['blog_post'] = request.session['blog_post']
    return render(request, 'home.html', context)


@login_required
def rewrite_blogpost(request):
    rewrite_blog_post = request.session['blog_post']
    rewrite_post = regenerateblogpost(rewrite_blog_post)
    if rewrite_post:
        
        request.session['rewrite_post'] = rewrite_post
    else:
        
        messages.error(request, 'Oops we could not generate any meta description for you, please try again.')
        return redirect('home')
        
    if 'rewrite_post' in request.session:    
        pass
    else:
        messages.error(request, 'Start by creating a blog outline')
        return redirect('home')

    context = {}
    context['rewrite_post'] = request.session['rewrite_post']
    return render(request, 'home.html', context)


@login_required
def meta_description(request):
    meta_description = request.session['blog_post']
    print(meta_description)
    meta_description = generatemetadescription(meta_description)
    if meta_description:
        
        request.session['meta_description'] = meta_description
    else:
        
        messages.error(request, 'Oops we could not generate any meta description for you, please try again.')
        return redirect('home')
        
    if 'meta_description' in request.session:    
        pass
    else:
        messages.error(request, 'Start by creating a blog outline')
        return redirect('home')

    context = {}
    context['meta_description'] = request.session['meta_description']
    return render(request, 'home.html', context)


@login_required
def youtube_link(request):
    if request.method == 'POST':
        
        topic = request.POST['topic']
        print(topic)
        youtube_link = generateyoutubelink(topic)
        print(youtube_link)
        if youtube_link:
        
            request.session['youtube_link'] = youtube_link
        else:
        
            messages.error(request, 'Oops we could not generate any meta description for you, please try again.')
            return redirect('login')
        
        if 'youtube_link' in request.session:    
            pass
        else:
            messages.error(request, 'Start by creating a blog outline')
            return redirect('home')

        context = {}
        context['youtube_link'] = request.session['youtube_link']
        context['is_htmx'] = request.headers.get('HX-Request') == 'true'
        return render(request, 'home.html', context)


@login_required
def add_youtube_link(request):
    youtube_link = request.POST.get('youtube_link')
    blog_post = request.session['blog_post']
    print(youtube_link)
    index = blog_post.find('Table of Contents')
    youtube_blog_link = blog_post
    
    mylines = []
    flag = False
    for line in blog_post:
        if flag == False and "Table of Contents".lower() in line.strip().lower():
            flag = True
        if flag:
            mylines.append(line)
            if "</ul>".lower() in line.strip().lower():
                flag = False
    print(''.join(mylines))
    print(mylines)
                
    if youtube_blog_link:
        
        request.session['youtube_blog_link'] = youtube_blog_link
    else:
        
        messages.error(request, 'Oops we could not generate any meta description for you, please try again.')
        return redirect('home')
        
    if 'youtube_blog_link' in request.session:    
        pass
    else:
        messages.error(request, 'Start by creating a blog outline')
        return redirect('home')

    context = {}
    
    youtube_blog = request.session['youtube_blog_link'].find('Table of Contents')
    context['blog_post_1'] = request.session['youtube_blog_link'][:index]
    context['youtube_add_link'] = youtube_link
    context['blog_post_2'] = request.session['youtube_blog_link'][index:]
    
    return render(request, 'home.html', context)
    
