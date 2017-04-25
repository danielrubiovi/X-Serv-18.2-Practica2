from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from .models import url_original
import urllib
from django.views.decorators.csrf import csrf_exempt

#Create views here

@csrf_exempt

def initmain(request):
	urls_list = url_original.objects.all()
	url_form = 'http://localhost:8000'

	method = request.method

	if method == 'GET':

		#Crear lista con todas las urls de la base de datos!!!!!!!!!!!!!!!!!!!!!!!!
		templates = get_template('initmain.html')

		htmlAnswer = '<body>'

		for url in urls_list:
			idn = url.id
			url = url.url

			htmlAnswer += '<p>' + str(url) + ' ==> http://localhost:8000/' + str(idn) + '</p>'

		htmlAnswe = '</body>'


		lista = {'lista': htmlAnswer}

		return HttpResponse(templates.render(Context(lista))) #El contexto obviamente sera la lista jeje

	elif method == 'POST':

		url_rcv = urllib.parse.unquote (request.POST.get('url'))

		if url_rcv == '':
			htmlAnswer = '<title>Error Formulario</title>'
			htmlAnswer += '<u>No me has dado una url, pincha </u>'
			htmlAnswer += '<a href="' + url_form + '"> aqui para otro formulario</a>'

			return HttpResponse(htmlAnswer)
		else:

			cuerpohttp = url_rcv.split("//")[0]

			if cuerpohttp == 'https:' or cuerpohttp == 'http:':
				url_rcv = str(url_rcv)

			else:
				url_rcv = 'http://' + str(url_rcv)

			try:
				url_in_list = url_original.objects.get(url = url_rcv)
			except url_original.DoesNotExist:

				##Añado a la lista, pq no existe la url en la base de datos
				url_original(url = url_rcv).save()
				id_url = url_original.objects.get(url = url_rcv).id
				url_short = 'http://localhost:8000/' + str(id_url)

				htmlAnswer = '<p>Su url acortada es:  '
				htmlAnswer += '<a href="' + url_short + '">' + url_short + '</a></p>'

				id_context = {'id': htmlAnswer}
				templates = get_template('url_guardada.html') 
				return HttpResponse(templates.render(Context(id_context))) 

			#Si existe ya la url

			identificador = url_in_list.id
			url_short = 'http://localhost:8000/' + str(identificador)
			htmlAnswer = '<title>Url Ya cortada</title>'
			htmlAnswer += '<p><h3>La url ' 
			htmlAnswer += '<a href="' + str(url_in_list.url) + '">' + str(url_in_list.url) + '</a>' 
			htmlAnswer += ' ya ha sido acortada anteriormente ==> '
			htmlAnswer += '<a href="http://localhost:8000/' + str(identificador) + '">' + str(url_short) + '</a></h3></p>'
			htmlAnswer += '<p><h5>Para acortar otra url pincha '
			htmlAnswer += '<a href="' + url_form + '"> AQUI</a></h5></p>'
			return HttpResponse(htmlAnswer)

	else:
		templates = get_template('405_error.html')
		return HttpResponse(templates.render())



def url_cortita (request, identificador):

	try:
		id_found = url_original.objects.get(id = identificador)
	except:
		templates = get_template('404_error.html')
		return HttpResponse(templates.render())

	url = str(id_found.url)

	htmlAnswer = "<p><h5>"'Estas siendo redirigido a: '+ url + "</h5></p>"
	htmlAnswer += "Redirecting... <meta http-equiv='refresh' content='2;"
	htmlAnswer += "URL=" + url + "'></p>"	

	return HttpResponse(htmlAnswer)

