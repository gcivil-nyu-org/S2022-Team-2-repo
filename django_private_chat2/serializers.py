from django.core.files.storage import get_storage_class

from .models import MessageModel, DialogsModel, UserModel, UploadedFile
from typing import Optional, Dict
from users.models import Profile
import os

media_storage = get_storage_class()()


def serialize_file_model(m: UploadedFile) -> Dict[str, str]:
    return {
        "id": str(m.id),
        "url": m.file.url,
        "size": m.file.size,
        "name": os.path.basename(m.file.name),
    }


def serialize_message_model(m: MessageModel, user_id):
    sender_pk = m.sender.pk
    profile = Profile.objects.get(user=sender_pk)
    is_out = sender_pk == user_id
    # TODO: add forwards
    # TODO: add replies
    obj = {
        "id": m.id,
        "text": m.text,
        "sent": int(m.created.timestamp()),
        "edited": int(m.modified.timestamp()),
        "read": m.read,
        "file": serialize_file_model(m.file) if m.file else None,
        "sender": str(sender_pk),
        "recipient": str(m.recipient.pk),
        "out": is_out,
        "sender_username": "{} {}".format(m.sender.first_name, m.sender.last_name),
        "sender_image": str(media_storage.url(name=profile.image.name)),
    }
    return obj


def serialize_dialog_model(m: DialogsModel, user_id):
    username_field = UserModel.USERNAME_FIELD
    other_user = (
        UserModel.objects.filter(pk=m.user1.pk).first()
        if m.user2.pk == user_id
        else UserModel.objects.filter(pk=m.user2.pk).first()
    )
    unread_count = MessageModel.get_unread_count_for_dialog_with_user(
        sender=other_user.id, recipient=user_id
    )
    last_message: Optional[MessageModel] = MessageModel.get_last_message_for_dialog(
        sender=other_user.id, recipient=user_id
    )
    last_message_ser = (
        serialize_message_model(last_message, user_id) if last_message else None
    )
    profile = Profile.objects.get(user=other_user.id)
    other_user_photo = media_storage.url(profile.image.name)
    obj = {
        "id": m.id,
        "created": int(m.created.timestamp()),
        "modified": int(m.modified.timestamp()),
        "other_user_id": str(other_user.id),
        "unread_count": unread_count,
        "username": "{} {}".format(other_user.first_name, other_user.last_name),
        "last_message": last_message_ser,
        "other_user_image": str(other_user_photo),
    }
    return obj
