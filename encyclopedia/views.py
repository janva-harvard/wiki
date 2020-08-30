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
    wikiTitle = forms.CharField(label="Wiki title")
    wikiContent = forms.CharField(label="",
                                  widget=forms.Textarea(attrs={'rows': 1,
                                                               'cols': 40,
                                                               'style': 'height: 5em;'}))


class EditForm(forms.Form):
    wikiContent = forms.CharField(label="",
                                  widget=forms.Textarea(attrs={'rows': 1,
                                                               'cols': 40,
                                                               'style': 'height: 10em;'}))


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
            title = "No exact match found. Maybe you can try.."
            near_matches = list(
                filter(lambda entry: query.lower() in entry.lower(), util.list_entries()))
            if not near_matches:
                title = "Can't find close match try annother query!"

            # code duplication fixme refactor
            return render(request, "encyclopedia/index.html", {
                "entries": near_matches,
                "search_form": SearchForm(),
                "title": title})


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
    request.session["article"] = entry
    converter = Markdown()
    the_entry = util.get_entry(entry)
    if(the_entry == None):
        return render(request, "encyclopedia/error.html", {
            "entry": entry,
            "search_form": SearchForm(),
        })
    entry_as_html = converter.convert(the_entry)

    return render(request, "encyclopedia/article.html", {
        # code duplication search_form attribute potential issue
        "entry": entry_as_html, "search_form": SearchForm()
        # "entry": util.get_entry(entry)
    })


def newwiki(request):
    if request.method == "POST":
        form = newWikiForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["wikiTitle"]
            content = form.cleaned_data["wikiContent"]
            content = "#"+title+"\n"+content
            # check for duplicates
            if util.get_entry(title) == None:
                # save to db
                util.save_entry(title, content)
            else:
                # Hmm might be a problem
                return render(request, "encyclopedia/newwiki.html", {
                    "search_form": SearchForm(),
                    "new_form":  newWikiForm(),
                    "duplicateError": True
                })
            return HttpResponseRedirect(reverse("wiki:entry", kwargs={'entry': title}))

            # return HttpResponseRedirect(reverse("wiki:index"), {
            #     "duplicateError": False
            # })

    else:
        return render(request, "encyclopedia/newwiki.html", {
            "search_form": SearchForm(),
            "new_form":  newWikiForm(),
            "duplicateError": False
        })


def edit(request):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            article = form.cleaned_data["wikiContent"]
            title = request.session["article"]
            util.save_entry(title, article)
            return HttpResponseRedirect(reverse("wiki:entry", kwargs={'entry': title}))

    return render(request, "encyclopedia/edit_entry.html", {
        "editForm": EditForm({"wikiContent": util.get_entry(request.session["article"])}),
        "title": request.session["article"],
    })


def random_entry(request):
    entry = util.get_random_entry()
    return article(request, entry)
