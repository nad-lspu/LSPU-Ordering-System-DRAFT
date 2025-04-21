from kivy.uix.screenmanager import Screen
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from firebase_config import auth, db
from kivymd.toast import toast
from kivy.utils import get_color_from_hex

class RegisterScreen(Screen):
    def on_pre_enter(self):
        self.create_role_menu()

    def create_role_menu(self):
        self.role_menu = MDDropdownMenu(
            caller=self.ids.reg_role,
            items=[
                {"text": "User", "on_release": lambda x="User": self.set_role(x)},
                {"text": "Admin", "on_release": lambda x="Admin": self.set_role(x)},
            ],
            width_mult=3,
            max_height=dp(112)
        )

    def open_role_menu(self):
        if not hasattr(self, 'role_menu'):
            self.create_role_menu()
        self.role_menu.open()

    def set_role(self, role):
        self.ids.reg_role.text = role
        self.role_menu.dismiss()

    def register_user(self):
        name = self.ids.reg_name
        role = self.ids.reg_role
        email = self.ids.reg_email
        password = self.ids.reg_password

        # Reset text colors
        for field in [name, role, email, password]:
            field.error = False
            field.helper_text = ""
            field.helper_text_mode = "on_error"

        if len(password.text) < 6:
            password.error = True
            password.helper_text = "Password must be at least 6 characters"
            return

        if "@" not in email.text or "." not in email.text:
            email.error = True
            email.helper_text = "Invalid email format"
            return

        if not name.text or not role.text:
            toast("All fields are required.")
            return

        try:
            user = auth.create_user_with_email_and_password(email.text, password.text)
            uid = user['localId']
            db.child("users").child(uid).set({
                "name": name.text,
                "role": role.text,
                "email": email.text
            })
            toast("Registered successfully!")
            self.manager.current = "login"

            # auth.send_email_verification(user['idToken'])
            # toast("Verification email sent. Please check your inbox.")
        except Exception as e:
            print(e)
            email.error = True
            email.helper_text = "Email already exists or invalid"

    def toggle_password_visibility(self, field):
        field.password = not field.password
        field.icon_right = "eye" if not field.password else "eye-off"

