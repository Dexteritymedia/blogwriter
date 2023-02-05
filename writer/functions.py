import os
from django.conf import settings
import openai

openai.api_key = settings.OPENAI_API_KEY

def generateblogoutline(audience, title):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Generate a blog outline for {} based on this\nTitle: {}".format(audience, title),
        temperature=0.7,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)

    return response['choices'][0]['text'].replace('\n','<br/>')

def generateblogpost(outline):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Write a 1000-1500 words blog post explaining each outlines, headings and subtitles in 3-5 paragraphs including appropriate html tags and a clickable table of contents:\n\n{}".format(outline),
        temperature=0.85,
        max_tokens=2500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)

    return response['choices'][0]['text']

def regenerateblogpost(blog_post):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Rewrite and paraphase the article below, add appropriate html tags and a clickable table of contents\nArticle:{}".format(blog_post),
        temperature=0.85,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)

    return response['choices'][0]['text']


def generatemetadescription(title):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Create an SEO meta description for this blog post {}".format(title),
        temperature=0.7,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)

    return response['choices'][0]['text']


def generateyoutubelink(topic):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Generate 3 active youtube links in html tags with complete url on the following topic separate each video link with the tag <br/>\nTopic: {}".format(topic),
        temperature=0.7,
        max_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)

    return response['choices'][0]['text']


def addyoutubelink(link, post):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Add this youtube link {} to the appropriate section to this blog post:\n {}".format(link, post),
        temperature=0.3,
        max_tokens=2500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0)

    return response['choices'][0]['text']
