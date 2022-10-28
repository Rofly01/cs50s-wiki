from django.forms import CharField
from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect

from . import util

class Form_Create(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, min_length=3)

class Form_Edit(forms.Form):
    def __init__(self, *args,**kwargs):
        self.content = kwargs.pop('initial_content')
        super(Form_Edit,self).__init__(*args,**kwargs)
        self.fields["edit"] = CharField(widget=forms.Textarea, initial=self.content, min_length=3)
        
        

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, entry):
    if page := util.get_html(entry):
        return render(request, "encyclopedia/page.html", {
            "content": page,
            "title": entry
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "code": 404,
            "about": "Page not found"
        })


def search(request):
    try:
        query = request.GET.__getitem__("q")
        if page := util.get_html(query):
            return HttpResponseRedirect(reverse('entry', args=(query,)))
        else:
            researches = []

            for entry in util.list_entries():
                if query.lower() in entry.lower():
                    researches.append(entry)

            return render(request, "encyclopedia/search.html", {
                "query": query.capitalize(),
                "entries": researches
            })
    except:
        return entry_page(request, "search")



def create(request):
    if request.method == 'POST':
        form = Form_Create(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if not util.get_entry(title):
                content = form.cleaned_data["content"]
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse('entry', args=(title,)))
            else:
                return render(request, "encyclopedia/error.html", {
                "code": 409,
                "about": "The page already exists"
                })
            
    return render(request, "encyclopedia/create.html", {
        'form': Form_Create()
    })
    
    
def edit(request, page):
    if request.method == "POST":
        form = Form_Edit(request.POST, initial_content=None)
        if form.is_valid():
            edit = form.cleaned_data["edit"]
            if util.get_entry(page):
                util.save_entry(page, edit)
                return HttpResponseRedirect(reverse("entry", args=(page,)))

    return render(request, "encyclopedia/edit.html", {
        "page": page,
        "form": Form_Edit(initial_content=util.get_entry(page))
    })
    
def random(request):
    list = util.list_entries()
    choice = util.random_choice(list)
    return HttpResponseRedirect(reverse('entry', args=(choice,)))