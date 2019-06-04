import importlib
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .forms import SearchForm
from .main import search


def get_text(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid() and 'search_text' in request.GET:
            classes=['title','year','directors','rating','category','plot','actors']
            info = "You searched for: %r" % request.GET['search_text'] + "<br><br>"
            info += "<div class=\"container\"><table>\n" + "\t<tr>\n" + "\t\t<th class=\"title\">Title</th>\n" + \
                    "\t\t<th class=\"year\">Year</th>\n" + "\t\t<th class=\"directors\">Directors</th>\n" + \
                    "\t\t<th class=\"rating\">Rating</th>\n" + "\t\t<th class=\"category\">Category</th>\n" + \
                    "\t\t<th class=\"plot\">Plot</th>\n" + "\t\t<th class=\"actors\">Actors</th>\n" + "\t</tr>\n"

            message = ""
            table = search(request.GET['search_text'])
            for row in table:
                message += "\t<tr>\n"
                for col in range(len(row)):
                    if str(row[col]) == "nan":
                        row[col] = ""
                    message += f"\t\t<td class=\"{str(classes[col])}\"><div class=\"{str(classes[col])}\">" \
                               f"{str(row[col])}</div></td>\n"
                message += "\t</tr>\n"
            return render(request, 'index.html', {'form': form, 'table': message, 'info': info})
    else:
        form = NameForm()

    return render(request, 'index.html', {'form': form})
