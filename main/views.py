from django.shortcuts import render, redirect, get_object_or_404
from .forms import Reader_Register_Form, Poster_Register_Form, User_update_Form
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import User, Posts
from django.forms import modelform_factory
from django.contrib import messages

# Create your views here.



# @login_required(login_url="/login")
def home(req):
    current_posts_all=Posts.objects.all()

    
    return render(req, 'main/home.html', {'posts':current_posts_all})

@login_required(login_url="/login")
def add_favorite(req, id):
    current_posts_all=Posts.objects.all()
    post_add=get_object_or_404(Posts,id=id)
    fav=False
    
    if req.user not in post_add.reader.all():
        post_add.reader.add(req.user.id)
      
        fav=True
        
    else:
        post_add.reader.remove(req.user.id)
        messages.warning(req, 'Post removed, to Add by re-clicking.')
        # print(post_add.reader.all())
        fav=False

    return redirect(req.META['HTTP_REFERER'])

def sign_up_reader(req):
    if req.method=='POST':
        form=Reader_Register_Form(req.POST, req.FILES)
        if form.is_valid():
            user=form.save()
            login(req, user)
            return redirect('/home')
    else:
        print('invalid')
        form=Reader_Register_Form()
    
    return render(req, 'registration/signup_st.html', {'form':form})

def sign_up_poster(req):
    if req.method=='POST':
        form=Poster_Register_Form(req.POST, req.FILES)
        if form.is_valid():
            user=form.save()
            login(req, user)
            return redirect('/home')
    else:
        print('invalid')
        form=Poster_Register_Form()
    
    return render(req, 'registration/signup_te.html', {'form':form})

def user_profile(req, id):
    current_user=get_object_or_404(User, pk=id)
    current_posts=req.user.posts_set.all()
    created_posts=Posts.objects.filter(creater=req.user)
    if req.method=='POST':
        email_new =req.POST.get('update-email')
        password_new=req.POST.get('update-password')
        if email_new is not None:
            current_user.email=email_new
            current_user.save(update_fields=['email'])
            return redirect("/{}/user-profile".format(id))
        if password_new is not None:
            current_user.set_password(password_new)
            current_user.save()
            return redirect('/') 
       
        
        # return redirect ("/{}/user-profile".format(id))
    return render(req, 'main/userprofile.html', {'current_user':current_user, 'posts':current_posts, 'created_posts':created_posts})



def user_update(req, id):
    current_user=get_object_or_404(User, pk=id)
    current_posts=req.user.posts_set.all()

    if req.method=='POST':
        email_new =req.POST.get('update-email')
        current_user.email=email_new
        current_user.save(update_fields=['email'])
        print(current_user.id)
       
        return redirect ("/{}/user-profile".format(id))
   
    return render(req, 'main/userprofile.html', {'current_user':current_user, 'posts':current_posts})
    

def user_delete(req, id):
    current_user=get_object_or_404(User, pk=id)
    current_user.delete()
    return redirect("/")

def post_delete(req, id):
    current_post=get_object_or_404(Posts, pk=id)
    current_post.delete()
    return redirect(req.META['HTTP_REFERER'])

@login_required(login_url="/login")
def article_detail(req, id):
    current_post=get_object_or_404(Posts, id=id)
    fav=bool
    if req.user not in current_post.reader.all():
        fav=False
    else:
        fav=True
    return render(req, 'main/detail.html', {'post':current_post, 'fav':fav})

# def user_posts(req, id):
#     current_posts=Posts.objects.filter(creater=req.user)

#     return render(req, 'main/posts.html', {'current_posts':current_posts})


PostForm=modelform_factory(Posts, exclude=["creater", "reader", "date"])

def new_post(req, id):
    if req.method=='POST':
        form=PostForm(req.POST, req.FILES)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.creater=req.user
            instance.save()
            print('record saved')
            return redirect("/{}/user-profile".format(id))
        else:
            print('not Saved!')
    else:
        form=PostForm()
    return render(req, 'main/create-posts.html', {"form":form})