from django.shortcuts import render
from .models import usuario,UserProfile
from .form import FormularioRegistro ,FormularioContacto
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import  get_object_or_404
from django.template.context_processors import csrf
# Create your views here.
from django.http import HttpResponse
from almacen.models import Curso ,Document ,Tema ,Categoria
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
import hashlib
import datetime
from django.core.mail import send_mail

import datetime

from django.utils import timezone

import random 
from almacen.form import CursoForm,TemaForm,VideoForm,CommentForm,CategoriaForm
#from urllib.parse import urlparse
from urllib import parse 
from urllib.parse import urlparse
from django.core.urlresolvers import reverse
#from urlparse import parse urlparse_qs

from django.db.models.functions import Upper



#esto lo estoy importando desde chat


def registro(request): 
	user=password=''
	if request.POST:
		frm = FormularioRegistro(request.POST)
		if frm.is_valid():
			#verificacion de email
			validarUsuario = usuario.verificacionUsername(user= request.POST['username'])
			d=usuario.verificacionEmail(email= request.POST['email'])	
			if d==False and validarUsuario==False:
				#creacion del usuario
				a= usuario.crear( user= request.POST['username'], password =request.POST['password'])
				a.first_name = frm.cleaned_data['first_name']
				a.email = frm.cleaned_data['email']
				a.last_name =frm.cleaned_data['last_name']
				a.dni=frm.cleaned_data['dni']
				a.gender=frm.cleaned_data['gender']
				#acceso  por 7 dias
				a.acceso_free = datetime.datetime.today() + datetime.timedelta(7)
				#si el usuario esta isOnline
				a.isOnline = False
				a.save()
				salt = hashlib.sha1(str(random.random()).encode()).hexdigest()[:5]            
				activation_key = hashlib.sha1((salt+a.email).encode()).hexdigest() 
				key_expires = datetime.datetime.today() + datetime.timedelta(2)
				#Obtener el nombre de usuario
				#validarUsuario = usuario.verificacionUsername(user= request.POST['username'])
				user=usuario.objects.get(username=a.username)    				
    				
				#user=usuario.objects.get(username=a.username)
				# Crear el perfil del usuario                                                                                                                                 
				new_profile = UserProfile(user=user, activation_key=activation_key, key_expires=key_expires)
				new_profile.save()

			# Enviar un email de confirmación
				email_subject = 'Account confirmation'
				email_body = "Hola %s, Gracias por registrarte. Para activar tu cuenta da clíck en este link en menos de 48 horas: http://127.0.0.1:8000/accounts/confirm/%s" % (a.username, activation_key)

				send_mail(email_subject, email_body, 'jordyrevatta99@gmail.com',[a.email], fail_silently=False)

				return HttpResponseRedirect(reverse('loguin'))
				
			else:
				return HttpResponseRedirect(reverse('registro'))			
			
	else:   
		frm = FormularioRegistro()

	#args = {}
	#args.update(csrf(request))
	#args['frm'] = frm
	context = {'frm':frm}
	return render (request,'registro.html',context)

def loguin(request):
	user=password=''
	if request.POST:
		c = FormularioRegistro(request.POST)
		if c.is_valid:
			c  =	usuario.verificar( user= request.POST['username'], password =request.POST['password'])

			if c==True:
				#para poder loguearse verifica
				#
				#
				Online= usuario.objects.get(username= request.POST['username'])
				if Online.isOnline == 'False':
					preAcceso = usuario.objects.get(username= request.POST['username'])
					aeiou = preAcceso.id
					pre = UserProfile.objects.get(user=aeiou)
					#agregando la funcionalidad para un solo usuario
					preAcceso.isOnline = 'True'
					preAcceso.save()
					if preAcceso.acceso == 'True':
						z = request.POST['username']		
								#return render(request,test.html,args)
						request.session['userr']=z	
						return HttpResponseRedirect(reverse('index'))
							
					if pre.activacion_url == 'True':
						if preAcceso.acceso_free > timezone.now():
						
							z = request.POST['username']		
								#return render(request,test.html,args)
							request.session['userr']=z	
						else:
							context = {'c':c}
							return render(request,'prueba_terminada.html',context)
							 
					#return HttpResponseRedirect(reverse('create'))
					return HttpResponseRedirect(reverse('index'))
				else:	
					return HttpResponseRedirect(reverse('loguin'))


			else:	

				return  HttpResponseRedirect(reverse('loguin'))
				
	else:
		c=FormularioRegistro()
	
	args = {}
	args.update(csrf(request))
	args['c'] = c
	plantilla = 'loguin.html'
	return render(request,plantilla, args )



def logout(request):
	Online = usuario.objects.get(username=request.session['userr'])
	Online.isOnline = 'False'
	Online.save()
	try:
		del request.session['userr']
	except KeyError:
		pass
	return  HttpResponseRedirect(reverse('index'))
	


def pago(request):
	lis = usuario.objects.get(username=request.session['userr'])
	lis.acceso = True
	lis.save()
	return  HttpResponseRedirect(reverse('index'))
	
def eliminar(request , codigo):
	eliminar = Curso.objects.get(codigo=codigo)
	eliminar.delete()
	return  HttpResponseRedirect(reverse('miscursos'))
	
	
def eliminarTema(request,id_video, slug ):
	eliminar = Tema.objects.get(id=id_video)
	a=eliminar.curso.codigo
	eliminar.delete()
	return  HttpResponseRedirect(reverse('mostrar', args=(a,)))
	
def ocultarTema(request,id_video,slug):
	ocultar = Tema.objects.get(id=id_video)
	a=ocultar.curso.codigo
	if  ocultar.accesoTema == 'mos':
		ocultar.accesoTema = 'ocul'
		
		#return HttpResponse('este tema se  ocultara algo')
		
	elif  ocultar.accesoTema == 'ocul':
		ocultar.accesoTema = 'mos'
		
		#return HttpResponse('este tema se mostrara')
	ocultar.save()	
	return  HttpResponseRedirect(reverse('mostrar', args=(a,)))
'''
MOSTRAR ='mos'
	OCULTO ='ocul'
'''	
		 

	

def index(request):
	try:
		user = usuario.objects.get(username=request.session['userr'])
		a = user
	except KeyError:	
		frm = FormularioRegistro()
		a = frm
	context= {"a":a}
	
	return render (request,'index.html',context)

#^verificado



def mostrarCurso(request):
	try:		
		lis = usuario.objects.get(username=request.session['userr'])
		ls = Cursos.objects.all()	
		if lis.gender == 't':
			return render(request,'cursos.html', {'lis':lis,'ls':ls})
	except :
			pass
	return render(request,'cursos.html', {'ls':ls})	
	

@login_required(login_url='/sesion')
def miscursos(request):
	if request.POST:
		frm=CursoForm(request.POST,request.FILES)
		fr=CategoriaForm(request.POST)
		if frm.is_valid() and fr.is_valid():
			a = frm.save()
			b=fr.save()
			try:
				a.usuario = usuario.objects.get(username=request.session['userr'])
				a.categoria=Categoria.objects.get(id=b.id)

			except KeyError:
				pass
			a.codigo = hashlib.md5(str(a.id).encode()).hexdigest()[:5]	
			a.save()
		
	fr = CategoriaForm()
	frm = CursoForm()
	try:
		listar = usuario.objects.get(username=request.session['userr'])
		alistar = Curso.objects.filter(usuario=listar)
	except KeyError:
		pass
	context = {'alistar':alistar,'frm':frm,'fr':fr}	
	return	render(request,'miscursos.html',context)	

"""

from chat.models import Room
from chat.forms import RoomForm
"""

#
'''
def new_room(request):
    rooms = Room.objects.all()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(chat_room, label=form.data['label'])
    else:
        form = RoomForm()

    context = {
        'rooms': rooms,
        'form': form
    }

    return render(request, 'new_room.html', context )
    '''
#verificando
from post.models import Liveblog

@login_required(login_url='/sesion')
def mostrar(request,codigo):
	if 	request.POST:
		frm=VideoForm(request.POST,request.FILES)
		fr = TemaForm(request.POST)
		#cuarto = RoomForm(request.POST)
		if frm.is_valid() and fr.is_valid():
			b=frm.save()
			a=fr.save()
			#lo de chat
			algo=Liveblog()
			algo.title=a.titulo
			algo.save()
			a.curso = get_object_or_404(Curso,codigo=codigo)
			a.codigo=codigo
			b.tema=get_object_or_404(Tema,id=a.id)
			val=frm.cleaned_data['tipoArchivo']
			value=frm.cleaned_data['docfile']
			if 	val=='you':
				qs = value.split('?')
				video_id = parse.parse_qs(qs[1])['v'][0]
			else:
				qs = value.split('https://vimeo.com/')
				video_id=qs[1]
			b.docfile=video_id
			a.save()
			b.save()
	
	try:
		dato = Curso.objects.get(codigo=codigo)
		#c = Document.objects.filter(curso = codigo)
		c = Tema.objects.filter(codigo=dato.codigo)
		lis = usuario.objects.get(username=request.session['userr'])
		
	except KeyError:
		pass
		
	frm = VideoForm()
	fr = TemaForm()
	#
		
	context = {'c':c,'frm':frm,'fr':fr,'lis':lis,'dato':dato}
	#este es el objeto de Cursos
	#c = Document.objects.filter(curso=dato)
	#return HttpResponseRedirect(reverse('must',args=(a.codigo,)))
	#return render_to_response('receta.html',{'receta':dato,'comentarios':comentarios}, context_instance=RequestContext(request))
	return	render(request,'cursoAlgo.html',context)
'''   
r = reporte.objects.get(codigo=codigo)

	return render (request,'hola.html', {'reporte': r})
'''
#verificado


def contactomail(request):
	if request.method == 'POST':
		formulario = FormularioContacto(request.POST)
		if formulario.is_valid():
			asunto = 'Mensaje de la Aplicacion de django de :'+formulario.cleaned_data['nombre']
			mensaje = formulario.cleaned_data['mensaje']
			mail = EmailMessage(asunto,mensaje,to=['jordyrevatta99@gmail.com'])
			mail.send()
			return HttpResponseRedirect(reverse('index'))
			
	else:	
		formulario = FormularioContacto()
		args = {}
		args.update(csrf(request))
		args['formulario'] = formulario
		return render(request,'contacto.html',args )

def register_confirm(request, activation_key):
	# Verifica que el usuario ya está logeado
	if request.user.is_authenticated():
		HttpResponseRedirect('index')

	# Verifica que el token de activación sea válido y sino retorna un 404
	user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
	user_profile.activacion_url= True
	user_profile.save()
	#hola=user_profile.activacion_url
	#var = UserProfile.activacion(asd=hola)
	#var.save()
	# verifica si el token de activación ha expirado y si es así renderiza el html de registro expirado
	if user_profile.key_expires < timezone.now():
		return HttpResponse('ya expiro el tiempo')
	# Si el token no ha expirado, se activa el usuario y se muestra el html de confirmación
	user = user_profile.user
	user.is_active = True
	user.save()
	return HttpResponse('verificacion de cuenta correcta')