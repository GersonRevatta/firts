from django.db import models
from usuario.models import usuario
# Create your models here. 
from django.core.urlresolvers import reverse
from django.template import defaultfilters
from django.template.defaultfilters import slugify
 
class Categoria(models.Model):
	ANIME ='ani'
	VIRTUALIZACION ='vir'
	PROGRAMACION = 'pro'
	CATEGORIES_CHOICES = (
	(ANIME,'anime'),
	(VIRTUALIZACION,'virtualizacion'),
	(PROGRAMACION,'programacion'))
	nombre = models.CharField(choices=CATEGORIES_CHOICES,default=ANIME, max_length=100)

 
class Curso(models.Model):
	categoria= models.ForeignKey(Categoria,null=True, blank=True)
	name = models.CharField(max_length=100)
	descripcion = models.TextField()
	usuario = models.ForeignKey(usuario,null=True, blank=True)
	imagen = models.ImageField(upload_to='imagenes/')
	codigo = models.CharField(max_length=5)
	ACTIVO ='act'
	PENDIENTE ='pen'
	Type_CHOICES = (
	(ACTIVO,'activo'),
	(PENDIENTE,'pendiente'))
	accesoCurso = models.CharField(choices=Type_CHOICES,default=PENDIENTE, max_length=100)

class Tema(models.Model):
	titulo = models.CharField(max_length=100)
	codigo = models.CharField(max_length=5)
	descripcion = models.TextField()
	curso = models.ForeignKey(Curso,null=True, blank=True)
	slug = models.SlugField(max_length=100)
	MOSTRAR ='mos'
	OCULTO ='ocul'
	Type_CHOICES = (
	(MOSTRAR,'mostar'),
	(OCULTO,'oculto'))
	accesoTema = models.CharField(choices=Type_CHOICES,default=MOSTRAR, max_length=100)
	
	def save(self, *args, **kwargs):
		self.slug = defaultfilters.slugify(self.titulo)
		super(Tema, self).save(*args, **kwargs)


	
class Video(models.Model):
	tema = models.ForeignKey(Tema,null=True, blank=True)
	filename = models.CharField(max_length=100)
	#docfile = models.FileField(upload_to='document/')
	docfile=  models.CharField(max_length=100)
	#docfile=  models.BooleanField('Allergies:')
	VIMEO ='vim'
	YOUTUBE ='you'
	Type_CHOICES = (
	(VIMEO,'vimeo'),
	(YOUTUBE,'youtube'))
	tipoArchivo = models.CharField(choices=Type_CHOICES,default=YOUTUBE, max_length=100)

 

class Document(models.Model):
	titulo = models.CharField(max_length=100)


class Comment(models.Model):
	user = models.CharField(max_length=250)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	approved = models.BooleanField(default=False)
	tema =models.ForeignKey(Tema,null=True,blank=True)
	def approved(self):
		self.approved = True
		self.save()
	def __str__(self):
		return self.user
		
class Reply(models.Model):
	comment = models.ForeignKey(Comment,null=True,blank=True)
	user = models.CharField(max_length=250)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	approved = models.BooleanField(default=False)

'''
 
https://blog.enriqueoriol.com/2014/07/upload-de-imagenes-con-django.html
'''
'''class Comment(models.Model):
	post = models.ForeignKey(Document, null=True, blank=True)
	user = models.CharField(max_length=250)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	approved = models.BooleanField(default=False)

	def approved(self):
		self.approved = True
		self.save()
	def __str__(self):
		return self.user
'''
