# Televiewshka

> Note: as for now, this is neither stable nor working code.
Being Created in ... purposes it is a subject for further updates and improvements

_viewshka_ - Russian noun: informal of eng. "view", obtained by adding a diminutive suffix "shka"

Televiewshka allows you develop UI & logic for telegram bots with class based views.
In views you can define its content and how user actions and replies must be handled on it.
When all stuff related particular step in user flow is held in one class, you can clearly
see relationship between components

Televiewshka supposed to be developed in such a manner to be compatible
with a bunch of libs and frameworks for telegram bot api widely used by community

I guess I should write few adaptors for this purpose someday

## (Supposed) Example

```py
from telebot import TeleBot
from televiewshka import KeyboardView, \
    KeyboardLayout, Button, adaptors, handler, render

# create adaptor for your lib/framework
bot = TeleBot("super-secret")
bot = adaptors.create_adaptor(bot)


# specify views
class FirstView(KeyboardView):
    @bot.action_handler(action="next")
    def go_next(self, query: Query):
        return render("NextView", inplace=True, param=42)

    @staticmethod
    def render():
        return KeyboardLayout(
            keyboard = (
                Button("Go next", on_click="next"),
            ))


class NextView(KeyboardView):
    @bot.action_handler()
    def back(self, query: Query):
        return render(FirstView, inplace=True)

    @staticmethod
    def render(param: int):
        return KeyboardLayout(
            text=f"Passed param: {param}",
            keyboard = (
                Button("Go back", on_click="back"),
            ))

# run the bot
bot.start()
```

## Some details explained

### Views

something that can be rendered to user
and than handle user actions on itselves
actions are dispatched to appropriate view' and method
in accordance with user state (e.g. current_scene flag)
which is set when the view is rendered

### Dispatch

messages are being dispatched according to user' state
state = current view
callback data or message = view method

### User state

pass
