import importlib
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .forms import SearchForm
from .main import search


def get_text(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid() and 'search_text' in request.GET:
            info = "You searched for: %r" % request.GET['search_text'] + "<br><br>"
            info += "<table>\n" + "\t<tr>\n" + "\t\t<th>Title</th>\n" + "\t\t<th>Year</th>\n" + \
                    "\t\t<th>Directors</th>\n" + "\t\t<th>Rating</th>\n" + "\t\t<th>Category</th>\n" + \
                    "\t\t<th>Plot</th>\n" + "\t\t<th>Actors</th>\n" + "\t</tr>\n"

            message = ""
            table = search(request.GET['search_text'])
            for row in table:
                message += "\t<tr>\n"
                for col in row:
                    if str(col) == "nan":
                        col = ""
                    message += f"\t\t<td>{str(col)}</td>\n"
                message += "\t</tr>\n"
            return render(request, 'index.html', {'form': form, 'table': message, 'info': info})
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
