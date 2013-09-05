import re
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from django.core.context_processors import csrf
from django.core.paginator import Paginator
from quotedb.forms import QuoteForm
from quotedb.models import Quote
from django.conf import settings

# Create your views here.
def main(request):
  
   # Get list of quotes to show
   textSearchArg = request.GET.get("q")
   authorSearchArg = request.GET.get("author")
   quote_list = Quote.objects.all().order_by("-created_at")
   
   # -- Text search
   if textSearchArg and len(textSearchArg) != 0:
      quote_list = quote_list.filter(quote_text__icontains=textSearchArg)
      
   # -- Author search
   if authorSearchArg and len(authorSearchArg) != 0:
      quote_list = quote_list.filter(quote_source__icontains=authorSearchArg)
  
   # Get paginator and page
   page = 1
   pageArg = request.GET.get("page")
   if pageArg and pageArg.isdigit():
      page = int(pageArg)
   paginator = Paginator(quote_list, settings.QUOTES_PER_PAGE)
   page = min(paginator.num_pages, page)
   page = max(1, page)
   quotePage = paginator.page(page)
   
   return render_to_response('quotedb/main.html',{"section":"intranet","page":"quotedb","quotePage":quotePage,"request":request,"searchArg":textSearchArg},context_instance=RequestContext(request))

def add(request):

   if request.method == 'POST':

      #-- Handle new quotes --
      # Save quote
      quoteForm = QuoteForm(request.POST)
      quoteForm.save()

      return main(request)
   else:
   
      # -- Handle quote adding --
      return render_to_response('quotedb/add.html',{"section":"intranet","page":'quotedb',"form":QuoteForm},context_instance=RequestContext(request))
