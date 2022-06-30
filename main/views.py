from django.shortcuts import render, redirect, get_object_or_404
from .forms import Reader_Register_Form, Poster_Register_Form, Comments_Form
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import User, Posts, Category, Comments, Notes
from django.forms import modelform_factory
from django.contrib import messages
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator 
from django.http import HttpResponseForbidden #import the HttpResponseForbidden page

# Create your views here.

class OwnerProtectMixin(object):
    def dispatch(self, request, *args, **kwargs):
        objectUser = self.get_object()
        try:
            if objectUser.name != self.request.user:
                return HttpResponseForbidden()
        except:
            if objectUser.user != self.request.user:
                return HttpResponseForbidden() 
        return super(OwnerProtectMixin, self).dispatch(request, *args, **kwargs)

def home(req, slug=None):
    category=None
    categories=Category.objects.all()
    current_posts_all=Posts.objects.all()

    if slug:
        category=get_object_or_404(Category, slug=slug)
        current_posts_all=Posts.objects.filter(category=category)
        posts_all=current_posts_all
        
    if req.method=='POST':
        search =req.POST.get('search')
        field=req.POST.get('field')
        if field=='title':
            result=Posts.objects.filter(title__contains=search)
        elif field=='description':
            result=Posts.objects.filter(description__contains=search)
        else:
            result=Posts.objects.filter(creater__username__icontains=search)
        posts_all=result
    else:
        posts_all=current_posts_all     
    return render(req, 'main/home.html', {'posts':posts_all, 'categories':categories, 'category':category})


#About Accounts

def sign_up_reader(req):
    if req.method=='POST':
        form=Reader_Register_Form(req.POST, req.FILES)
        if form.is_valid():
            user=form.save()
            login(req, user)
            return redirect('/home')
        else:
            messages.info(req, 'Invalid Input.')
    else:
        form=Reader_Register_Form()    
    return render(req, 'registration/signup_reader.html', {'form':form})


def sign_up_poster(req):
    if req.method=='POST':
        form=Poster_Register_Form(req.POST, req.FILES)
        if form.is_valid():
            user=form.save()
            login(req, user)
            return redirect('/home')
        else:
            messages.info(req, 'Invalid Input.')
    else:
        form=Poster_Register_Form()    
    return render(req, 'registration/signup_writer.html', {'form':form})


@login_required(login_url="/accounts/login")
def user_profile(req, id):
    current_user=get_object_or_404(User, pk=id)
    current_posts=req.user.posts_set.all()
    created_posts=Posts.objects.filter(creater=req.user)
    if req.method=='POST':
        email_new =req.POST.get('update-email')
        if email_new is not None:
            current_user.email=email_new
            current_user.save(update_fields=['email'])
            return redirect("/user-profile/{}/".format(id))      
    return render(req, 'main/userprofile.html', {'current_user':current_user, 'posts':current_posts, 'created_posts':created_posts})


class ProfileUpdateView(UpdateView):
    model = User
    fields = ['username', 'avatar', 'first_name', 'last_name', 'email']
    template_name= 'registration/update-profile.html'


@login_required(login_url="/accounts/login")
def password_update(req, id):   
    if req.method=='POST':
        password_new=req.POST.get('Password_new')
        password_old=req.POST.get('Password_old')
        if  req.user.check_password(password_old):

            if password_new is not None:
                current_user.set_password(password_new)
                current_user.save()
                print('password changed')           
            return redirect('/')
        else:
            messages.warning(req, 'current password is wrong')
            return redirect(req.META['HTTP_REFERER'])
    return render(req,'registration/update-password.html' )


@login_required(login_url="/accounts/login")
def user_delete(req, id):
    current_user=get_object_or_404(User, pk=id)
    current_user.delete()
    return redirect("/")


# About Posts 

PostForm=modelform_factory(Posts, exclude=["creater", "reader", "date","add_like", "set_public"])
@login_required(login_url="/login")
def new_post(req, id):
    if req.method=='POST':
        form=PostForm(req.POST, req.FILES)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.creater=req.user
            instance.save()
            print('record saved')
            return redirect("/user-profile/{}/".format(id))
        else:
            print('not Saved!')
    else:
        form=PostForm()
    return render(req, 'main/create-posts.html', {"form":form})


@login_required(login_url="/accounts/login")
def add_favorite(req, id):
    current_posts_all=Posts.objects.all()
    post_add=get_object_or_404(Posts,id=id)
    fav=False   
    if req.user not in post_add.reader.all():
        post_add.reader.add(req.user.id)
        post_add.add_like+=1      
        post_add.save()#['add_like']
        fav=True       
    else:
        post_add.reader.remove(req.user.id)      
        post_add.add_like-=1
        post_add.save()
        fav=False
    return redirect(req.META['HTTP_REFERER'])


def post_delete(req, id):
    current_post=get_object_or_404(Posts, pk=id)
    current_post.delete()
    return redirect(req.META['HTTP_REFERER'])


def article_detail(req, id):
    current_post=get_object_or_404(Posts, id=id)
    comments_on=current_post.comments_on.all()
    num=current_post.add_like
    fav=False
    this_note=None
    if req.user.is_authenticated:
        user_note=Notes.objects.filter(name=req.user)
        this_note=user_note.filter(post=current_post)
    
    #Different requests 
    # 1) show post status of add_like
    if req.user not in current_post.reader.all():
        fav=False
    else:
        fav=True
    #2) Form submitting
    if req.method=='POST':
        #a) Add Note form
        if 'note' in req.POST:
            text=req.POST.get("note_new")
            tag=req.POST.get("note_tag")
            if text != "":
                note_new= Notes.objects.create(name=req.user, post=current_post, text=text, tag=tag)
                note_new.save()
                print(text)
                return redirect(req.META['HTTP_REFERER'])
            else:
                return redirect(req.META['HTTP_REFERER'])
        #b) Add comment
        if 'comment' in req.POST:
            #Returns a callable view that takes a request and returns a response
            Comments_view.as_view()(req, pk=id)        
        #c) Add replied Comment
        if 'reply' in req.POST:
            Comments_view.as_view()(req, pk=id)
        # if 'delete' in req.POST:
        #     id_delete=int(req.POST.get("delete_id"))
        #     current_comment=Comments.objects.filter(id=id_delete)
        #     print(current_comment)
        #     current_comment.delete()
        #     print('delete')
                  
    return render(req, 'main/detail.html', {'post':current_post, 'fav':fav, 'num':num, 'comments':comments_on, 'notes':this_note,  'form':Comments_Form}) #'comment_form':Comments_Form,


def article_status(req, id):
    current_post=get_object_or_404(Posts, id=id)
    public=bool
    if current_post.set_public:
        public=False
    else:
        public=True    
    current_post.set_public=public
    current_post.save(update_fields=['set_public'])
    return redirect("/")


class PostUpdateView(UpdateView):
    model = Posts
    fields = ['title','content', 'cover']
    template_name= 'main/update-posts.html'



def note_delete(req, id):
    current_note=get_object_or_404(Notes, pk=id)
    current_note.delete()
    return redirect(req.META['HTTP_REFERER'])


class Comments_view(CreateView):
    model=Comments
    form_class=Comments_Form

    def form_valid(self, form):
        form.instance.post_id=self.kwargs['pk']
        if self.request.user.is_authenticated:
            form.instance.name=self.request.user
        else:
            form.instance.name=None
        try:
            form.instance.parent_id=self.request.POST.get("parent_id")
        except:
            form.instance.parent_id=None
        return super().form_valid(form)


@method_decorator(login_required,name='dispatch' )#
class Comment_delete_view(OwnerProtectMixin, DeleteView):
    model=Comments
    form_class=Comments_Form
    template_name="main/comments_confirm_delete.html"
    success_url="/"

