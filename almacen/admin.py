from django.contrib import admin

# Register your models here.
from .models import Curso ,Tema ,Categoria , Comment
from usuario.models import usuario
#correcto
#class AdminCurso(admin.ModelAdmin):
#	fields = ["name"]
#	list_display = ["name","descripcion"]
#	list_filter = ["categoria"]
#	search_fields = ['name']
#	class Meta:
#		model = Curso

#admin.site.register(Curso,AdminCurso)	



#admin.site.register(Tema , AdminCurso)	
#para queu los campos no se puedan editar
#readonly_fields 




class AdminTema(admin.ModelAdmin):
	list_display = ['curso_name','titulo','descripcion']
	list_filter = ['curso__name']
	search_fields = ['titulo']
	def curso_name(self, obj):
		#usuario.username.short_username = 'The Author Description'
		return obj.curso.name
	

class AdminCurso(admin.ModelAdmin):
	fields = ['name','descripcion','accesoCurso']
	list_display = ['name', 'descripcion', 'usuario_username','accesoCurso']
	list_filter = ['categoria__nombre']
	search_fields = ['name']
	def usuario_username(self, obj):
		
		#usuario.username.short_username = 'The Author Description'
		return obj.usuario.username
	
	#def categoria_nombre(self, obj):
	 #   return obj.categoria.nombre   
	#categoria_nombre.short_description = 'The Author Description'

	usuario_username.short_description = 'Author'

class AdminComment(admin.ModelAdmin):
	fields = ['user','email','body']
	list_display=['tema_titulo','body','user','tema_curso_name']
	#list_filter =['tema__titulo']
	list_filter =['tema__curso__name']
	search_fields = ['tema__titulo']
	def tema_titulo(self, obj):
		
		#usuario.username.short_username = 'The Author Description'
		return obj.tema.titulo
	def tema_curso_name(self, obj):
		
		#usuario.username.short_username = 'The Author Description'
		return obj.tema.curso.name
admin.site.register(Comment,AdminComment)	
admin.site.register(Curso,AdminCurso)	
admin.site.register(Tema,AdminTema)	

#admin.site.register(usuario,AdminCurso)	


