from django.shortcuts import render 
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Contents
from django.template.loader import get_template
from django.template import Context

FORMULARIO = """
<form action="" method="POST">
    Puede modificar el contenido aquí: <br>
    Contenido: <input type="text" name="content"<br>
    <input type = "submit" value = "Enviar"> 
</form>
"""

#Funcion de ayuda para no repetir código
def process(request,response):
    res = ""
    log = ""
    user = ""
    if request.user.is_authenticated():
        res = '/logout'
        log = 'Logout'
        user = 'Logged in as ' + request.user.username
    else:
        res = '/login'
        log = 'Login'
        user = 'Not logged in'
    c = Context({'content' : response, 'resource' : res, 'log_status' : log, 'username' : user})
    return c

# Create your views here.
def barra(request):
    if request.user.is_authenticated():
        logged = 'Logged in as ' + request.user.username 
        logged += '. <a href=/logout>Logout</a><br>'
    else:
        logged = 'Not logged in.' + '<a href=/login>Login</a><br>'

    if request.method == 'GET':
        all_contents = Contents.objects.all()
        response = '<h1>Contenidos random</h1><br>'
        response += '<h2>Pinche en uno de los nombres para ver los contenidos</h2>'
        response += '<ul>'
        for one_content in all_contents:
            response += '<li>' + '<a href = /' + str(one_content.id) + ">" + one_content.name + "</a>"
        response += '</ul><br>'
        new_version = '<a href = /annotated/> Version 2.0 </a>'     
        return HttpResponse(response + logged + new_version)
    else:
        return HttpResponse('<h2>405 Method Error</h2>')

@csrf_exempt
def content(request, num):
    if request.method == 'POST':
        try:
            this_content = Contents.objects.get(id = int(num))
            this_content.content = request.POST['content']
            this_content.save()
        except Contents.DoesNotExist:
            return HttpResponse('<h2>404 Not Found</h2>')
        response = '<h2>El contenido ha sido modificado con éxito</h2><br>'
        response += '<a href = />Volver a la página principal</a><br>'
        response += '<a href = /annotated/> Version 2.0 </a><br>' 
        return HttpResponse(response)
    elif request.method == 'GET':
        try:
            request_content = Contents.objects.get(id =  int(num))
        except Contents.DoesNotExist:
            return HttpResponse('<h2>404 Not Found</h2>')
        response = 'Titulo: ' + request_content.name +'<br>'
        response += 'Contenido: ' + request_content.content + '<br>'
        if request.user.is_authenticated():
            response += FORMULARIO
        response += "<a href=/> Volver a la página principal </a><br>"
        response += '<a href = /annotated/> Version 2.0 </a><br>' 
        return HttpResponse(response)
    else:
        return HttpResponse('<h2>405 Method Error</h2>')

def annotated(request):
    response = ""
    if request.method == 'GET':
        all_contents = Contents.objects.all()
        for one_content in all_contents:
            response += '<li>' + '<a href = /annotated/' + str(one_content.id) + ">" + one_content.name + "</a>"
        response += '</ul><br>'     
    else:
        response = '<h2>405 Method Error</h2>'
        response += '<a href = /annotated/>Volver a la página principal</a><br>'

    template = get_template('Rounded_2/index.html')
    c = process(request,response)
    return HttpResponse(template.render(c))

@csrf_exempt
def annotated_content(request, num):
    template = get_template('Rounded_2/index_2.html')
    response = ""
    if request.method == 'POST':
        try:
            this_content = Contents.objects.get(id = int(num))
            this_content.content = request.POST['content']
            this_content.save()
        except Contents.DoesNotExist:
            response = '<h2>404 Not Found</h2><br>'
            response += '<a href = /annotated/>Volver a la página principal</a><br>'
            c = process(request,response)
            return HttpResponse(template.render(c))
        response = '<h2>El contenido ha sido modificado con éxito</h2><br>'
        response += '<a href = /annotated/>Volver a la página principal</a><br>'
    elif request.method == 'GET':
        try:
            this_content = Contents.objects.get(id =  int(num))
        except Contents.DoesNotExist:
            response = '<h2>404 Not Found</h2><br>'
            response += '<a href = /annotated/>Volver a la página principal</a><br>'
            c = process(request,response)
            return HttpResponse(template.render(c))
        response = 'Titulo: ' + this_content.name +'<br>'
        response += 'Contenido: ' + this_content.content + '<br>'
        if request.user.is_authenticated():
            response += FORMULARIO
        response += "<a href=/annotated/> Volver a la página principal </a><br>"
    else:
        response = '<h2>405 Method Error</h2>'
        response += '<a href = /annotated/>Volver a la página principal</a><br>'
    c = process(request,response)
    return HttpResponse(template.render(c))
