from __future__ import annotations

import hashlib
from . import models
from . import api_types

__all__ = [
    'MyType',
    'CallbackButton',
    # 'InlineKeyboard',
]


class MyType:

    def to_dict(self) -> dict:
        pass


class CallbackButton:

    def __init__(self, text: str, data: str = None):
        self.text = text
        self.data = data or text
        self.args = {}

    def __getitem__(self, item):
        return self.args[item]

    def save(self) -> str:
        string = f'{self.text}|{self.data}|{self.args}'
        button_id = hashlib.md5(string.encode()).hexdigest()
        models.CallbackButton(id=button_id, text=self.text, data=self.data, args=self.args).save()
        return button_id

    @classmethod
    def get(cls, button_id: str) -> CallbackButton | None:
        button_doc: models.CallbackButton = models.CallbackButton.objects(id=button_id).first()
        button = CallbackButton(button_doc.text, button_doc.data)
        button.args = button_doc.args
        return button

    def __call__(self, **args: str | int | list | dict | set) -> api_types.InlineKeyboardButton:
        """Return InlineKeyboardButton(text=text.format(**args), callback_data=button_id)"""
        new_button = CallbackButton(self.text, self.data)
        new_button.args = args
        button_id = new_button.save()

        return api_types.InlineKeyboardButton(
            text=new_button.text.format(**args),
            callback_data=button_id,
        )
