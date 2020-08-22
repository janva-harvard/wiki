from markdown2 import Markdown
# import markdown2
from django.shortcuts import render

from . import util
from django import forms
from django.http import HttpResponseRedirect


class SearchForm(forms.Form):
    search_query = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'search'}))


def index(request):
    if request.method == "POST":
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            query = search_form.cleaned_data["search_query"]
            return article(request, query)

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "search_form": SearchForm()
    })


def article(request, entry):

    converter = Markdown()
    the_entry = util.get_entry(entry)
    if(the_entry == None):
        return render(request, "encyclopedia/error.html", {
            "entry": entry
        })

    html = converter.convert(the_entry)

    return render(request, "encyclopedia/article.html", {
        "entry": html
        # "entry": util.get_entry(entry)
    })
