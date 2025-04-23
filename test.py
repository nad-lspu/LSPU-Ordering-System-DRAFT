from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivy.metrics import dp
from kivy.properties import BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

KV = '''
<PasswordTextField>:
    size_hint_y: None
    height: password_field.height

    MDTextField:
        id: password_field
        hint_text: "Password"
        password: True
        helper_text: "Enter your password"
        helper_text_mode: "on_focus"
        pos_hint: {"center_y": .5}
        size_hint_x: 1
        password: root.password_hidden

    MDIconButton:
        icon: "eye-off" if root.password_hidden else "eye"
        pos_hint: {"center_y": .5}
        pos: password_field.width - self.width + dp(8), 0
        theme_text_color: "Hint"
        on_release: root.toggle_password_visibility()

PasswordScreen:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)

        MDLabel:
            text: "Login"
            font_style: "H4"
            size_hint_y: None
            height: dp(50)
            halign: "center"

        Widget:
            size_hint_y: 0.3

        MDTextField:
            hint_text: "Username"
            icon_right: "account"
            size_hint_x: None
            width: "300dp"
            pos_hint: {"center_x": .5}

        PasswordTextField:
            id: password_field
            size_hint_x: None
            width: "300dp"
            pos_hint: {"center_x": .5}

        Widget:
            size_hint_y: 0.3

        MDRaisedButton:
            text: "LOGIN"
            pos_hint: {"center_x": .5}
            size_hint_x: None
            width: "200dp"
'''

class PasswordTextField(BoxLayout):
    password_hidden = BooleanProperty(True)

    def toggle_password_visibility(self):
        self.password_hidden = not self.password_hidden


class PasswordScreen(MDScreen):
    pass


class PasswordApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)


if __name__ == "__main__":
    PasswordApp().run()