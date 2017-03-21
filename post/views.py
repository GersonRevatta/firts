from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.db.models import Max
from .models import Liveblog


def index(request):
    """
    Root page view. Just shows a list of liveblogs.
    """
    # Get a list of liveblogs, ordered by the date of their most recent
    # post, descending (so ones with stuff happening are at the top)
    liveblogs = Liveblog.objects.annotate(
        max_created=Max("posts__created")
    ).order_by("-max_created")

    # Render that in the index template
    return render(request, "index.html", {
        "liveblogs": liveblogs,
    })


def liveblog(request, slug):
    """
    Shows an individual liveblog page.
    """
    # Get the liveblog by slug
    blog = get_object_or_404(Liveblog, slug=slug)

    # Render it with the posts ordered in descending order.
    # If the user has JavaScript enabled, the template has JS that will
    # keep it updated.
    return render(request, "liveblog.html", {
        "liveblog": blog,
        "posts": blog.posts.order_by("-created"),
    })

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

    #room, created = Room.objects.get_or_create(label=slug)   
    #messages = reversed(room.messages.order_by('-timestamp')[:50])
    blog = get_object_or_404(Liveblog, slug=slug)
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
    context = {'c':c,'d':d,'vi':vi,'form':form,'co':co,'liveblog':blog,'posts':blog.posts.order_by("-created")}
    return render(request,'video.html',context)

