from markdown2 import Markdown
# import markdown2
from django.shortcuts import render

from . import util
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse


class SearchForm(forms.Form):
    search_query = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'search'}))


class newWikiForm(forms.Form):
    titleField = forms.CharField(label="Wiki title")
    textArea = forms.CharField(label="",
                               widget=forms.Textarea(attrs={'rows': 1,
                                                            'cols': 40,
                                                            'style': 'height: 5em;'}))


def handleSearchRequest(request):
    search_form = SearchForm(request.POST)
    # ugh uggly
    if search_form.is_valid():
        query = search_form.cleaned_data["search_query"]
        if util.get_entry(query) != None:
            # specs say redirect so that what i'll do
            return HttpResponseRedirect(query)
            # return article(request, query)
            # return handle_search(request, query)
        else:
            heading = "No exact match found. Maybe you can try.."
            near_matches = list(
                filter(lambda entry: query.lower() in entry.lower(), util.list_entries()))
            if not near_matches:
                heading = "Can't find close match try annother query!"

            # code duplication fixme refactor
            return render(request, "encyclopedia/index.html", {
                "entries": near_matches,
                "search_form": SearchForm(),
                "heading": heading})


def index(request):
    if request.method == "POST":
        return handleSearchRequest(request)
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "search_form": SearchForm(),
            "heading": "All Pages "
        })


def article(request, entry):
    print("called")
    converter = Markdown()
    the_entry = util.get_entry(entry)
    if(the_entry == None):
        return render(request, "encyclopedia/error.html", {
            "entry": entry,
            "search_form": SearchForm(),
        })
    html = converter.convert(the_entry)

    return render(request, "encyclopedia/article.html", {
        # code duplication search_form attribute potential issue
        "entry": html, "search_form": SearchForm()
        # "entry": util.get_entry(entry)
    })


def newwiki(request):
    return render(request, "encyclopedia/newwiki.html", {
        "search_form": SearchForm(),
        "new_form":  newWikiForm()
    })
