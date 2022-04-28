import mongoengine as me


class AdPost(me.Document):
    chat_id: int = me.IntField()
    message_id: int = me.IntField()


class ChatAllowedLinks(me.Document):
    chat_id: int = me.IntField()
    allowed_links: list[str] = me.ListField(me.StringField())
