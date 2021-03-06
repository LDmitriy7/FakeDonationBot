from __future__ import annotations

from datetime import datetime

import mongoengine as me


class Config(me.Document):
    admins_ids: list[int] = me.ListField(me.IntField())
    log_file: str = me.StringField()
    log_level: int = me.IntField()
    restart_date: datetime = me.DateTimeField()
