from django import forms
from .models import Curso , Tema , Video ,Comment ,Categoria

#from .models import Cursos,Document,Comment

 

   
class CursoForm(forms.ModelForm):
	class Meta:
		model=Curso
		fields=['name','descripcion','imagen']
		
		widgets = {
			'name' : forms.TextInput(attrs = {'placeholder': 'Nombre del Curso','class':'form-control','style':'text-transform:uppercase','onkeyup':'javascript:this.value=this.value.toUpperCase();'}),	
			'descripcion' : forms.Textarea(attrs = {'placeholder': 'Detalles del Curso','rows':'2','class':'form-control'}),	
			'imagen' : forms.FileInput(attrs = {'accept': 'image/gif, image/jpeg, image/png'}),
		}

             
	
									
class TemaForm(forms.ModelForm):
	class Meta:
		model=Tema
		fields=['titulo','descripcion','accesoTema']
		widgets = {
			'titulo' : forms.TextInput(attrs = {'placeholder': 'Nombre del tema','class':'form-control'}),	
			'descripcion' : forms.Textarea(attrs = {'placeholder': 'Detalles sobre el tema','rows':'2','class':'form-control'}),	
		}

class VideoForm(forms.ModelForm):
	class Meta:
		model=Video
		fields=['filename','docfile','tipoArchivo']
		widgets = {
			'filename' : forms.TextInput(attrs = {'placeholder': 'Nombre del Archivo','class':'form-control'}),
			'docfile':	forms.URLInput(attrs = {'placeholder': 'Ingrese la URL','class':'form-control','id':'enlace','pattern':'https:\/\/www.youtube.com\/watch(.+)'}),
			#'tipoArchivo': forms.CharInput(widget=forms.RadioSelect, choices=Video.Type_CHOICES)
			'tipoArchivo': forms.Select(attrs = {'onchange':'ShowSelectedd()','id':'tipoArchivo'}),
			'smart_phone_ownership': forms.Select(attrs = {'name' : 'pos','id':'pos'}),
			
		
		}

class CategoriaForm(forms.ModelForm):
	class Meta:
		model=Categoria
		fields=['nombre']		
'''
class Formcapitulos(forms.ModelForm):
	class Meta:
		model=Document
		fields=['titulo','filename','descripcion','docfile']
'''
class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['body']
		widgets = {

			'body' : forms.Textarea(attrs = {'placeholder': 'Ingresa un comentario','class':'form-control','id':'bodyComment'}),
			
		
		}

class ReplyForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ('user','email','body')	

'''
class Curso(models.Model):
	name = models.CharField(max_length=100)
	descripcion = models.CharField(max_length=100)
	usuario = models.ForeignKey(usuario,null=True, blank=True)
	imagen = models.ImageField(upload_to='imagenes/')
	codigo = models.CharField(max_length=5)
class Tema(models.Model):
	titulo = models.CharField(max_length=100)
	codigo = models.CharField(max_length=5)
	descripcion = models.CharField(max_length=100)
	curso = models.ForeignKey(Curso,null=True, blank=True)
class Video(models.Model):
	filename = models.CharField(max_length=100)
	docfile = models.FileField(upload_to='document/')
'''