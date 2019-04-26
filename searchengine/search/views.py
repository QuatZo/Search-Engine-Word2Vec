import importlib
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .forms import SearchForm
from .main import search


def get_text(request):
    # if this is a GET request we need to process the form data
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.GET)
        # check whether it's valid:
        if form.is_valid():
            form = None
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/search/table.html')

    # if a POST (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'index.html', {'form': form})


def get_table(request):
    if request.method == 'GET' and 'search_text' in request.GET:
        info = "You searched for: %r" % request.GET['search_text'] + "<br><br>"
        message = ""
        table = search(request.GET['search_text'])
        for row in table:
            message += "\t<tr>\n"
            for col in row:
                if str(col) == "nan":
                    col = ""
                message += f"\t\t<td>{str(col)}</td>\n"
            message += "\t</tr>\n"
        return render(request, 'table.html', {'table': message, 'info': info})
    else:
        message = "Whoops! Empty form."

    request.GET = None
    return HttpResponse(message)
