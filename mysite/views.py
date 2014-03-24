# -*- coding: utf-8 -*-
import os
from django.shortcuts import get_object_or_404
import datetime
from mysite.forum.models import *
from mysite.forum.models import Messages
from mysite.form import MyUserForm, MessageForm, ThreadForm
from mysite.settings import MEDIA_ROOT
from django.shortcuts import render, redirect

# Function for showing list of topics it subcategory
def thread_list(request, subcategory_id):
    subcat = get_object_or_404(Subcategories, id=subcategory_id)
    if not auth_check(request, subcat.auth_required):
        return redirect("login_page")

    if not request.POST:
        tops = Topics.objects.filter(subcategory=subcat)
        return render(request, 'thread_list.html',
                {"subcat": subcat, "topics": tops, "path": request.path})

    else:
        form = request.POST
        if form.get('new_top') == u'Create new topic':
            return redirect('create_topic_page', subcategory_id)

# Function for showing main forum page
def categories(request):
    cats, subcats = Categories.objects.filter(auth_required=False), Subcategories.objects.filter(auth_required=False)
    auth_cats, auth_subcats = Categories.objects.filter(auth_required=True), Subcategories.objects.filter(
        auth_required=True)
    time = datetime.datetime.now()
    return render(request, "subcategories.html",
            {"current_time": time, "cats": cats, "subcats": subcats, "auth_cats": auth_cats,
             "auth_subcats": auth_subcats})

# Function for creating new topic
def create_thread(request, subcategory_id):
    subcat = get_object_or_404(Subcategories, id=subcategory_id)

    #If authorization required for topic and user is anonymous,
    # then redirect to login page
    if not auth_check(request, subcat.auth_required):
        return redirect("login_page")

    form = ThreadForm(request.POST, request.FILES)

    # If user has created topic then save it to database
    if request.method == 'POST' and form.is_valid():

        #Get name of message author from Threadform(if user is anonymous) or from user object
        if not request.user.is_anonymous():
            creator_name = request.user.username
        else:
            creator_name = form.cleaned_data.get('creator_name', None)

        thread_title = form.cleaned_data.get('title', None)
        thread_descr = form.cleaned_data.get('description', None)
        if request.FILES:
            top_file = handle_uploaded_file(request.FILES['file'],request.FILES['file'].name)
            top=Topics(title=thread_title,description=thread_descr,creator_name=creator_name,subcategory = Subcategories.objects.get(id=subcategory_id), file_name=top_file)
        else:
           top=Topics(title=thread_title,description=thread_descr,creator_name=creator_name,subcategory = Subcategories.objects.get(id=subcategory_id))

        top.save()
        top_id=top.id
        return redirect('topic_page',subcategory_id,top_id)
    else:
        form = ThreadForm(request.POST or None)
        if not request.user.is_anonymous():
            form.fields['creator_name'].widget.attrs['value'] = request.user.username
            form.fields['creator_name'].widget.attrs['readonly'] = True
        context = { 'form': form, 'subcat' : subcat}
        return render(request, "create_thread.html", context)

# Function for handling topic page
def thread(request, subcategory_id, top_id):
    subcat = get_object_or_404(Subcategories, id=subcategory_id)

    #If authorization required for topic and user is anonymous,
    # then redirect to login page
    if not auth_check(request, subcat.auth_required):
        return redirect("login_page")

    form = MessageForm(request.POST, request.FILES)
    top = get_object_or_404(Topics, id=top_id)

    if request.POST.get('back') == u'Back to threads':
        return redirect('threads', subcategory_id)

    #If Reply button was clicked then open message form
    if request.POST.get('reply') == u'Reply':
        form = MessageForm(request.POST, request.FILES)
        msgs = Messages.objects.filter(topic_id=top_id)

        #If user logged on, then showing his name in message form
        if not request.user.is_anonymous():
           form.fields['creator_name'].widget.attrs['value'] = request.user.username
           form.fields['creator_name'].widget.attrs['readonly'] = True
        return render(request, 'thread.html', {"top": top, "messages": msgs,'form': form, 'subcat': subcat})

   # If user has sent message then save it to database
    if request.method == 'POST' and form.is_valid():

        msgs = Messages.objects.filter(topic_id=top_id)
        message_descr = form.cleaned_data.get('description', None)

        #Get name of message author from Messageform(if user is anonymous) or from user object
        if request.user.is_anonymous():
            creator_name = form.cleaned_data.get('creator_name', None)
        else:
            creator_name = request.user.username

        #If user attached file in message, then handle it
        if request.FILES:
            message_file = handle_uploaded_file(request.FILES['file'], request.FILES['file'].name)
            message = Messages(message=message_descr, creator_name=creator_name, topic=top, file_name=message_file)
        else:
            message = Messages(message=message_descr, creator_name=creator_name, topic=top)

        #Save message to database and update topic's change date
        message.save()
        Topics.objects.filter(id=top.id).update(update_date=datetime.datetime.now())
        return render(request, 'thread.html', {"top": top, "messages": msgs, 'form': form, 'subcat': subcat})
    else:
        msgs = Messages.objects.filter(topic_id=top_id)[:2]
    return render(request, 'thread.html', {"top": top, "messages": msgs, 'subcat': subcat})

# Function for saving upload files
def handle_uploaded_file(file, filename):
    path_tofile=os.path.join(MEDIA_ROOT,filename)
    destination = open(path_tofile, 'wb+')
    for chunk in file.chunks():
        destination.write(chunk)
    destination.close()
    return filename

# Function for handling registration page
def register(request):
    if request.method == 'POST':
        form = MyUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/forum/registered')
    else:
        form = MyUserForm()
    return render(request, "registration/register.html", {'form': form,})

# Function for checking user authority
def auth_check(request, auth_required):
    if auth_required and request.user.is_anonymous():
        return False
    else:
        return True
