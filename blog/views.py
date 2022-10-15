from datetime import date
from re import S
from turtle import pos
from django.shortcuts import render,get_object_or_404
from .models import Post
from .forms import CommentsForm

from django.views.generic import ListView , DetailView
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.urls import reverse


all_posts = [
   
]

def get_date(post):
    return post['date']

# Create your views here.
def starting_page(request):

    latest_post=Post.objects.all().order_by("-date")[:3]
    
    return render(request,'blog/index.html', {
        "posts":latest_post
    })

def posts(request):
    all_posts= Post.objects.all().order_by("-date")
    return render(request,"blog/all-post.html", {
        "posts" : all_posts
    })

def post_detaials(request,slug):
    
    identified_post = get_object_or_404(Post,slug=slug)
    return render(request, "blog/post-detail.html",{
        "post": identified_post,
        "tags": identified_post.tag.all()
    })

class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"


    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data
    

class PostsView(ListView):
    template_name = "blog/all-post.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"



class PostsDetailView(View):

    def is_stored_post(self, request, post_id):
         stored_posts = request.session.get("stored_posts")
         if stored_posts is not None  :
            is_saved_for_later = post_id in stored_posts
         else:
            is_saved_for_later = False

         return is_saved_for_later




    def get(self,request,slug):
         post=Post.objects.get(slug=slug)
         
         context ={
            "post":post,
            "tags":post.tag.all(),
            "comment_form": CommentsForm(),
            "comments":post.comments.all().order_by("-id"),
            "is_saved_for_later": self.is_stored_post(request, post.id)
         }

         return render(request, "blog/post-detail.html",context)

    def post(self,request,slug):
        comment_form = CommentsForm(request.POST)
        post=Post.objects.get(slug=slug)
        print("i am here")
        if comment_form.is_valid():
            print("how its validated")
            comment=comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-details-page", args=[slug]))
        else:
            
            context ={
            "post":post,
            "tags":post.tag.all(),
            "comment_form": comment_form,
            "comments":post.comments.all().order_by("-id"),
            "is_saved_for_later": self.is_stored_post(request, post.id)
            }

            return render(request, "blog/post-detail.html",context)


    

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["tags"] = self.object.tag.all()
    #     context["comment_form"]= CommentsForm()

    #     return context
    


    
class ReadLaterView(View):
    def get(self, request):
        stored_post = request.session.get("stored_posts")
        context = {}
        if stored_post is None or len(stored_post)==0:
            context["posts"] = []
            context["has_post"]= False
            print("babaji ")
        else:
            posts=Post.objects.filter(id__in=stored_post)
            context["posts"]=posts
            context["has_post"] =True
            print("ghantat")
           
        print("in get")
        return render(request, "blog/stored-post.html",context)

    def post(self,request):
        stored_post = request.session.get("stored_posts")

        if stored_post is None:
            stored_post = []
        post_id =int(request.POST["post_id"])
        if post_id  not in stored_post:
             stored_post.append(post_id)
             print("added")
             
        else:
            stored_post.remove(post_id)
        request.session["stored_posts"] = stored_post
        return HttpResponseRedirect("/")


