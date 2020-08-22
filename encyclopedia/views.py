from markdown2 import Markdown
# import markdown2
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def article(request, entry):

    converter = Markdown()
    the_entry = util.get_entry(entry)
    if(the_entry == None):
        return render(request, "encyclopedia/error.html", {
            "entry": entry
        })

    html = converter.convert(the_entry)
    # TODO continue here
    # if request.method == "POST":

    return render(request, "encyclopedia/article.html", {
        "entry": html
        # "entry": util.get_entry(entry)
    })
