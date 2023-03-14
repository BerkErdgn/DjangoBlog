from django.shortcuts import render,HttpResponse,redirect,get_object_or_404,reverse
from django.contrib import messages
from .forms import ArticleForm
from .models import Article,Comment
from django.contrib.auth.decorators import login_required
# Create your views here.


def articles(requrest):
    keyword = requrest.GET.get("keyword")

    if keyword:
        articles = Article.objects.filter(title__contains = keyword)
        return render(requrest,"articles.html",{"articles": articles})
    
    articles = Article.objects.all()


    return render(requrest,"articles.html",{"articles": articles})

def index(request):
    return render(request,"index.html")

def about(request):
    return render(request, "about.html")

@login_required(login_url="user:login")
def dashboard (request):
    articles = Article.objects.filter(auther = request.user)
    context = {
        "articles": articles
    }

    return render(request,"dashboard.html",context)

@login_required(login_url="user:login")
def addArticle (request):
    form = ArticleForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        article = form.save(commit= False)
        article.auther = request.user
        article.save()


        messages.success(request,"Makale Başarıyla oluşturuldu.")
        return redirect("article:dashboard")

    return render(request,"addArticle.html",{"form":form})

def detail (request, id):
    #article = Article.objects.filter(id = id).first()
    article = get_object_or_404(Article, id =id )

    comments = article.comments.all()
    return render(request,"detail.html",{"article": article,"comments":comments})

@login_required(login_url="user:login")
def updateArticle(request,id):
    article = get_object_or_404(Article,id= id)
    form = ArticleForm(request.POST or None , request.FILES or None, instance = article)
    if form.is_valid():
        article = form.save(commit= False)
        article.auther = request.user
        article.save()


        messages.success(request,"Makale Başarıyla Güncellendi.")
        return redirect("article:dashboard")


    return render (request, "update.html",{"form":form})

@login_required(login_url="user:login")
def deleteArticle(request,id):
    article = get_object_or_404(Article,id=id)
    article.delete()

    messages.success(request,"Makale Başarıyla silindi.")
    return redirect ("article:dashboard")

def addComment(request, id):
    article = get_object_or_404(Article,id=id)
    
    if request.method =="POST":
        comment_outher = request.POST.get("comment_outher")
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_outher= comment_outher, comment_content= comment_content)
        newComment.articel = article
        newComment.save()
    return redirect(reverse("article:detail", kwargs={"id":id}))

        
