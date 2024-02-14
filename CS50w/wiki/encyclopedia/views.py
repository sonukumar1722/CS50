from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import randint
from . import util
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from markdown2 import markdown
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# fetch pages data form the get_entry function

def get_page(request, entry):

    return render(request,  "encyclopedia/pages.html" , {
    "pages": markdown(util.get_entry(entry)),
    "title":entry
    })


def random_page(request):
    # get random page data
    entry =  util.list_entries()[randint(0, len(util.list_entries())-1)]
    return get_page(request, entry)

@csrf_exempt
def create_page(request):
    if request.method == "POST":

        # fetch the input data form the form
        title = request.POST.get("title")
        content = request.POST.get("content")

        # validate that title is not empty
        if title:

            # checks is title exist
            if title.capitalize() in util.list_entries():
                return render(request, "encyclopedia/pages.html",{
                "pages": "<h2 style= \"font-fmily:san-serif; color:red; \"> Error! Title already exist, please enter diffrent title for the page.<h2>",
                "title": title
                })

                # If title not eixst it save the pages
            else:
                util.save_entry(title.capitalize(), content)
                return HttpResponseRedirect(f"wiki/{title}")
        else:
            return HttpResponseRedirect(reverse("create"))

    return render(request, "encyclopedia/create.html")


def search_page(request):
    is_title = None
    list_page = []

    # get the quries inpute from the form
    string = request.GET.get("q")

    # fetch the page list form the file
    titles = util.list_entries()

    # checks if title exists
    for title in titles:
        if string.lower() == title.lower():
            is_title = title
            break

        # checks if substring of the title exists
        elif string.lower() in title.lower():
            list_page.append(title)

    # check if title already present it redirect he user to that page
    if is_title:
        return HttpResponseRedirect(f"wiki/{title}")

    # checks if the title includes the substr and lists all the titles
    elif len(list_page) > 0:
        return render(request, "encyclopedia/index.html", {
        "entries": list_page
    })

    # if no result found
    else:
            return render(request, "encyclopedia/index.html", {
            "no_search": "No Search result!"
    })

@csrf_exempt
def edit_page(request,entry):

    # Checks for request method  = POST
    if request.method == "POST":

        # access the file in the entries folder
        filename = f"entries/{entry}.md"

        # get the data form the form
        content = request.POST.get("content")

        # checks for the file name in the directory
        if default_storage.exists(filename):
            default_storage.delete(filename)

        # save the content to the file in the directory
        default_storage.save(filename, ContentFile(content))

        # redirect the user to get_page function
        return HttpResponseRedirect(reverse('get_page', args=(entry,)))
    else:
        return render(request, 'encyclopedia/edit.html',{
            "content" : util.get_entry(entry),
            "entry": entry
        })


