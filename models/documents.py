import mongoengine as me


class AdPost(me.Document):
    chat_id: int = me.IntField()
    message_id: int = me.IntField()
