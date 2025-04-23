from users.models import Contact
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from .models import Message

from django.contrib.auth.models import User
from django.utils import timezone
from django.template.loader import render_to_string
import json
import datetime
# Create your views here.


#Запрос новых сообщений
@login_required(login_url = '/')
def post(request, username):
    companion = User.objects.get(username = username)
    messages = Message.objects.filter(reciever = request.user, sender = companion, is_readed = False)
    for message in messages:
        message.is_readed = True
        message.save()

    for message in messages:
        message.decrypt_message()
    context = {'messages': messages, 'user': request.user}
    if messages:
        return HttpResponse(
            json.dumps({
                "result": True,
                "messages_list": render_to_string('messenger/dialog_messages_block.html', context),
            }),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({
                "result": False,
            }),
            content_type="application/json"
        )


def dialog(request, username):
    companion = User.objects.get(username=username)
    messages = (Message.objects.filter(sender=request.user, reciever=companion,
                                       sender_visibility=True) | Message.objects.filter(reciever=request.user,
                                                                                        sender=companion,
                                                                                        reciever_visibility=True)).order_by(
        "-message_time")[:20]
    messages2 = (Message.objects.filter(sender=request.user, reciever=companion,
                                        sender_visibility=True) | Message.objects.filter(reciever=request.user,
                                                                                         sender=companion,
                                                                                         reciever_visibility=True)).order_by(
        "-message_time")[20:]
    not_readed_messages = Message.objects.filter(reciever=request.user, sender=companion)
    for message in not_readed_messages:

        message.save()

    for message in messages:
        message.decrypt_message()

    contact = User.objects.get(username=username)
    context = {'sort_messages': messages[::-1], 'contact': contact, 'messages2': messages2}
    return render(request, 'messenger/dialog.html', context)


#Проверка на новые сообщения
@login_required(login_url = '/')
def new_messages(request):
    messages = Message.objects.filter(reciever = request.user)
    new_friends = Contact.objects.filter(users_friend = request.user)
    status_for_update = {'online':timezone.now()}
    if messages or new_friends:
        return HttpResponse(
            json.dumps({
                "result": True,
                "messages_count": len(messages),
                "new_friends": len(new_friends),
            }), content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({
                "result": False,
            }), content_type="application/json")


#Отправка сообщения
@login_required(login_url = '/')
def leave_message(request, reciever_name):
    reciever_user = User.objects.get(username = reciever_name)
    if request.method == 'POST':
        message_text = request.POST['message_text']
        print(message_text)

        a = Message(sender = request.user, reciever = reciever_user, message_text = message_text, message_time = timezone.now())
        a.encrypt_message(message_text)
        a.save()
    messages = Message.objects.filter(id = a.id)
    for el in messages:
        el.decrypt_message()

    context = {'messages': messages, 'user': request.user}
    if messages:
        return HttpResponse(
            json.dumps({
                "result": True,
                "messages_list": render_to_string('messenger/dialog_messages_block.html', context),
            }),
            content_type="application/json")
    else:
        return HttpResponse(
            json.dumps({
                "result": False,
            }),
            content_type="application/json")

# Удаление сообщения
@login_required(login_url='/')
def delete_message(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
    except:
        raise Http404("Сообщение не найдено!")
    if message.sender == request.user:
        message.sender_visibility = False
        if not message.reciever_visibility:
            message.delete()
        else:
            message.save()
    else:
        message.reciever_visibility = False
        if not message.sender_visibility:
            message.delete()
        else:
            message.save()
    return JsonResponse({'status': 'ok'})


def delete_dialog(request, companion_id):
    try:
        companion = User.objects.get(id=companion_id)
    except:
        raise Http404("Собеседник не найден!")

    send_messages = Message.objects.filter(sender=request.user, reciever=companion)
    for message in send_messages:
        message.sender_visibility = False
        if not message.reciever_visibility:
            message.delete()
        else:
            message.save()
    reciever_messages = Message.objects.filter(reciever=request.user, sender=companion)
    for message in reciever_messages:
        message.reciever_visibility = False
        if not message.sender_visibility:
            message.delete()
        else:
            message.save()
    return JsonResponse({'status': 'ok'})


# Вывод всех диалогов пользователя
@login_required(login_url='/')
def messages(request):
    messages = (Message.objects.filter(sender=request.user, sender_visibility=True) | Message.objects.filter(
        reciever=request.user, reciever_visibility=True)).order_by("-message_time")
    users = []
    last_messages = []
    for message in messages:
        if message.sender != request.user:
            if not message.sender in users:
                users.append(message.sender)
                last_message = (Message.objects.filter(sender=message.sender,
                                                       reciever=request.user) | Message.objects.filter(
                    reciever=message.sender, sender=request.user)).order_by("-message_time")[:1]
                last_messages.append(last_message)
        if message.reciever != request.user:
            if not message.reciever in users:
                users.append(message.reciever)
                last_message = (Message.objects.filter(sender=message.reciever,
                                                       reciever=request.user) | Message.objects.filter(
                    reciever=message.reciever, sender=request.user)).order_by("-message_time")[:1]
                last_messages.append(last_message)
    last_messages_list = []
    #for message_query in last_messages:
    #    for message in message_query:
    #        if message.reciever == request.user:
    #            last_messages_list.insert(0, message)
    #        else:
    #            last_messages_list.append(message)

    users_friends1 = Contact.objects.filter(user=request.user)
    users_friends2 = Contact.objects.filter(users_friend=request.user)

    print(list(users_friends1))
    print(list(users_friends2))

    contacts = merge_lists(list(users_friends2), list(users_friends1))

    print(contacts)

    context = {'messages': last_messages_list, 'friends1': users_friends1, 'friends2': users_friends2, 'companion': users}
    return render(request, 'messenger/messages.html', context)


def merge_lists(lst1, lst2):
    for i in lst2:
        if i not in lst1:
            lst1.append(i)
    return lst1
