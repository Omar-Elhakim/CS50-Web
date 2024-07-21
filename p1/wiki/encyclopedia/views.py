from django.http import HttpResponse
from django.shortcuts import render, redirect
from . import util
import markdown2
from random import choice


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, entry):
    markdown_content = util.get_entry(entry)
    if markdown_content:
        return render(
            request,
            "encyclopedia/entry.html",
            {
                "entry": entry,
                "html": markdown2.markdown(markdown_content),
            },
        )
    else:
        return render(request, "encyclopedia/notFound.html")


def Random(request):
    entry = choice(util.list_entries())
    return redirect("entry", entry=entry)


def newEntry(request):
    entryTitle = request.POST.get("entryTitle", "")
    entryData = util.get_entry(entryTitle) if util.get_entry(entryTitle) != None else ""
    return render(
        request,
        "encyclopedia/newFile.html",
        {
            "entryTitle": entryTitle,
            "entryData": entryData,
            "editFlag": entryTitle != "",
        },
    )


def submit(request):
    entryTitle = request.POST.get("entryTitle", "")
    entryData = request.POST.get("entryData", "")
    if (entryTitle in util.list_entries()) and request.POST.get(
        "editFlag", ""
    ) == "False":
        return render(request, "encyclopedia/duplicateEntries.html")
    util.save_entry(entryTitle, entryData)
    return redirect("entry", entry=entryTitle)


def search(request):
    searchedEntry = request.POST.get("searchedEntry", "")
    if searchedEntry in util.list_entries():
        return redirect("entry", entry=searchedEntry)
    else:
        entries = []
        for entry in util.list_entries():
            if searchedEntry.lower() in entry.lower():
                entries.append(entry)
        if not entries:
            return render(request, "encyclopedia/notFound.html")
        else:
            return render(
                request, "encyclopedia/searchResults.html", {"entries": entries}
            )
