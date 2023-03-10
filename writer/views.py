import textwrap

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .functions import *

# Create your views here.

@login_required
def home(request):
    if request.method == 'POST':
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
            
            messages.error(request, 'Start by writing a title')

        context = {}
        context['blog_outline'] = request.session['blog_outline']
        context['title'] = request.session['title']
        context['audience'] = request.session['audience']
        print(request.session['blog_outline'])
        context['is_htmx'] = request.headers.get('HX-Request') == 'true'
        return render(request, 'blog_outline.html', context)
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
    #context['is_htmx'] = request.headers.get('HX-Request') == 'true'
    return render(request, 'blogpost_page.html', context)



@login_required
def rewrite_blogpost(request):
    try:
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
        context['is_htmx'] = request.headers.get('HX-Request') == 'true'
        return render(request, 'home.html', context)
    except:
        messages.error(request, 'Start by creating a blog post')
        return redirect('home')


@login_required
def rewrite_post(request):
    alltext = request.session['blog_post']
    chunks = textwrap.wrap(alltext, 2000)
    results = list()
    for chunk in chunks:
        prompt = chunk
        text = gpt_completion(prompt)
        results.append(text)
    context = {}
    context['results'] = results
    #context['is_htmx'] = request.headers.get('HX-Request') == 'true'
    return render(request, 'rewrite_post.html', context)



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
    #context['is_htmx'] = request.headers.get('HX-Request') == 'true'
    return render(request, 'meta_description.html', context)


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
        return render(request, 'youtube_link.html', context)


def get_youtube_link(request):
    youtube_link = request.POST.get('youtube_link')
    context = {}
    if youtube_link:
        query = youtube_link.replace(' ', '+')
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query="+query)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode()) 
        print(video_ids)
        remove_duplicates = list(set(video_ids))#To remove duplicates from the results
        print(remove_duplicates)
        print(len(remove_duplicates))
        print(list(dict.fromkeys(video_ids)))#To remove duplicates from the results and sort them out
        context['youtube_link'] = video_ids[:3]
        context['youtube_link2'] = remove_duplicates[:10]
        context['is_htmx'] = request.headers.get('HX-Request') == 'true'
        return render(request, 'youtube_results.html', context)
    return render(request, 'youtube.html', context)


@login_required
def add_youtube_link(request):
    youtube_link = request.POST.get('youtube_link')
    blog_post = request.session['blog_post']
    print(youtube_link)
    index = blog_post.find('<h2>Table of Contents')
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
    context['is_htmx'] = request.headers.get('HX-Request') == 'true'
    
    return render(request, 'youtube_blog_link.html', context)
    
