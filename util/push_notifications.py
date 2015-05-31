from gcm import GCM
from hitmeup import settings

gcm = GCM(settings.SENDER_ID)


def push_notification(reg_id, title, message):
    data = {
        'title': title,
        'msg': message,
    }

    if len(reg_id) > 0:
        gcm.plaintext_request(registration_id=reg_id, data=data)