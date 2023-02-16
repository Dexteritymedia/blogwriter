import io
import csv
import datetime
from datetime import date

from django.views.generic import TemplateView, View, ListView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.mail import send_mail, send_mass_mail
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.template.loader import get_template

import pandas as pd
from xhtml2pdf import pisa

from .models import AdCopy
from .tasks import *

# Create your views here.

class CsvUploader(TemplateView):
    template_name = 'campaign/csv_uploader.html'

    def post(self, request):
        context = {
            'messages':[]
        }

        csv = request.FILES['csv']
        csv_data = pd.read_csv(
            io.StringIO(
                csv.read().decode("utf-8")
            )
        )

        """
        Make sure the headings in the csv file correspond with
        the model field name i.e name is name while Name isn't the
        same with name an error will occur
        """

        for record in csv_data.to_dict(orient="records"):
            try:
                AdCopy.objects.create(
                    name = record['name'],
                    email = record['email'],
                    product = record['product'],
                    ad_copy = record['ad_copy'],
                    description = record['description']
                )
                #return HttpResponse("Csv file successfully Uploaded")
                context['success'] = "Csv file successfully Uploaded"

            except Exception as e:
                context['exceptions_raised'] = e
                print(context['exceptions_raised'])
                
        return render(request, self.template_name, context)

class HomeView(ListView):
    template_name = 'campaign/home.html'
    model = AdCopy
    context_object_name = 'ad_copy'
    #login_required = True
    paginate_by = 10

    def get_queryset(self):

        """List the First 30 queryset in reverse order"""
        return AdCopy.objects.all()[:30:-1]
        #return AdCopy.objects.all()[:10][::-1]

    def post(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST' and 'ad_copy' in request.POST:
            
            ids = request.POST.getlist('ckeck_user[]')

            for id in ids:
                text = AdCopy.objects.get(pk=id)
                print(text)
                try:
                    ad_copy = generate_ad_copy(text.product)
                    text.ad_copy = ad_copy
                    print(ad_copy)
                    text.save()
                    context['success'] = "Ad copy Successfully Generated"
                except Exception as e:
                    context['exceptions_raised'] = e
                    print(context['exceptions_raised'])
                    
            return redirect('home')

        if request.method == 'POST' and 'send_mail' in request.POST:
            
            user_ids = request.POST.getlist('ckeck_user[]')

            for id in user_ids:
                text = AdCopy.objects.get(pk=id)
                print(text.email)
                try:
                    email = [
                        (
                            
                            text.name, #Subject
                            text.ad_copy, #message
                            settings.EMAIL_HOST_USER, #from/sender
                            [text.email], #to/recipient
                        )
                    ]
                    #send_mass_mail(messages)
                    print(email)
                    text.status = "Sent"
                    date = datetime.datetime.now()
                    today = date.today()
                    today_date = today.strftime("%B %d, %Y")
                    dt = date.strftime("%d/%m/%Y %H:%M:%S")
                    dt_time = date.strftime("%H:%M")
                    text.save()
                    messages.add_message(
                        
                        request, messages.SUCCESS,
                        f"You sent an email to {text.name} on {today_date} at {dt_time}"
                    )
                
                except Exception as e:
                    messages.add_message(
                        
                        request, messages.ERROR,
                        f"We couldn't sent an email to {text.name}, Please try again"
                    )
        
            return redirect('home')

        return redirect('home')


class DeleteFile(DeleteView):
    model = AdCopy
    template_name = 'campaign/delete.html'
    context_object_name = 'ad_copy'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, 'This post has been deleted.')
        return super(DeleteFile, self).form_valid(form)

    
class UpdateFile(UpdateView):
    model = AdCopy
    fields = ['name','email', 'product']
    template_name = 'campaign/edit.html'
    success_url = reverse_lazy('home')
    

def export_csv(request):
    marketing = AdCopy.objects.all()

    #Create the HttpResponse object with the appropriate CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="csv_data.csv"'

    writer = csv.writer(response)
    writer.writerow(['name', 'email', 'product', 'ad_copy', 'description'])

    for record in marketing:
        writer.writerow([record.name, record.email, record.product, record.ad_copy, record.description])

    return response

def generate_pdf(request, blog_id):
    
    ad_copy = get_object_or_404(AdCopy, id=blog_id) #Will return Page not found
    #ad_copy = AdCopy.objects.get(id=blog_id) 
    context = {}
    template_path = 'campaign/pdf.html'
    context['ad_copy'] = ad_copy
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    #Use the below code to give each pdf a name
    filename = "Ad_%s.pdf" % ad_copy.name
    content = "attachment; filename='%s'" % filename
    response['Content-Disposition'] = content
    
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        
        html, dest=response,)
    if pisa_status.err:
        
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    
    return response


def generate_all_pdf(request):
    
    ad_copy = AdCopy.objects.all()
    context = {}
    template_path = 'campaign/all_pdf.html'
    context['ad_copy'] = ad_copy
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="all_report.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        
        html, dest=response,)
    if pisa_status.err:
        
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def table__(request):
    return render(request, 'campaign/table.html')
