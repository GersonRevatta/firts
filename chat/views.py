from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm
# Create your views here.

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

def chat_room(request, label):
    room, created = Room.objects.get_or_create(label=label)   
    
    
    messages = reversed(room.messages.order_by('-timestamp')[:50])
    context = {
        'room': room,
        'messages': messages
    }

    return render(request, 'room.html', context)




from django.shortcuts import render, redirect #puedes importar render_to_response
#from .form import cursos ,capitulos , CommentForm ,ReplyForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from usuario.models import usuario
from django.core.urlresolvers import reverse
#from .models import Cursos ,Comment

from django.template.context_processors import csrf
from django.shortcuts import  get_object_or_404
from django.contrib.auth.decorators import login_required
from almacen.models import Curso , Tema , Video ,Comment,Categoria
from almacen.form import CursoForm,TemaForm,VideoForm,CommentForm,CategoriaForm
from django.db.models import Q
#from .models import Document

def mostrarVideos(request,id_video, slug ):
    c = Tema.objects.get(id=id_video)
    #
    room, created = Room.objects.get_or_create(label=slug)   
    
    messages = reversed(room.messages.order_by('-timestamp')[:50])

    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid() :

            b=form.save()
            comment = usuario.objects.get(username=request.session['userr'])
            b.user = comment.username
            b.email = comment.email
            a= Tema.objects.filter(codigo=c.codigo)
            for repo in a:
                b.tema = get_object_or_404(Tema,id=repo.id)
                
            b.save()    
    form=CommentForm()  
    d = Tema.objects.filter(codigo=c.codigo)
    vi = Video.objects.get(id=id_video)
    co = Comment.objects.filter(tema=vi.id)
    context = {'c':c,'d':d,'vi':vi,'form':form,'co':co,'room':room,'messages':messages}
    return render(request,'video.html',context)