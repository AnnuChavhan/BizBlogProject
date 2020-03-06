from django.shortcuts import render,get_object_or_404
from django.core.mail import send_mail
from blogapp.models import Post
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from taggit.models import Tag
from .forms import CommentForm,EmailSendForm

def post_list_view(request,tag_slug=None):
    post_list=Post.objects.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=post_list.filter(tag__in=[tag])
    paginator=Paginator(post_list,3)
    page_number=request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page((1))
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)  #####
    return render(request,'blog/post_list.html',{'tag':tag,'post_list':post_list})

def post_detail_view(request,year,month,day,post):
    post=get_object_or_404(Post,slug=post,status='published',publish_year=year,publish_month=month,publish_day=day)
    comments=post.comments.filter(active=True)
    csubmit=False
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            csubmit=True
        else:
            form=CommentForm()
        return render(request,'blog/post_deatil.html',{'post':post,'form':form,'csubmit':csubmit})

    def mail_send_view(request,id):
        post=get_object_or_404(Post,id=id,status='published')
        sent=False
        if request.method=='POST':
            form=EmailSendForm(request.POST)
            if form.is_valid():
                cd=form.cleaned_data
                subject="{} ({}) recommends you to read '{}'".format(cd['name'],cd['email'],post.title)
                post_url=request.built_absolute_uri(post.get_absolute_url())
                message='Read Post At: \n{}\n\n{}\'s comments:\n{}'.format('url',cd['name'],cd['comments'])
                send_mail(subject,message,'maddyev3@gmail.com',[cd['to']])
                sent=True
            else:
                form=EmailSendForm()
            return render(request,'blog/sharebymail.html',{'form':form,'post':post,'sent':sent})

