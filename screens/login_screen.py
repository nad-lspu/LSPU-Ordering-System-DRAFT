from kivy.uix.screenmanager import Screen
from firebase_config import auth, db
from kivymd.toast import toast

class LoginScreen(Screen):
    def login_user(self):
        email = self.ids.login_email
        password = self.ids.login_password

        email.error = False
        password.error = False

        if not email.text or "@" not in email.text:
            email.error = True
            email.helper_text = "Enter a valid email"
            return
        if len(password.text) < 6:
            password.error = True
            password.helper_text = "Password too short"
            return

        try:
            user = auth.sign_in_with_email_and_password(email.text, password.text)
            uid = user['localId']
            user_data = db.child("users").child(uid).get().val()

            # user_info = auth.get_account_info(user['idToken'])
            # if not user_info['users'][0]['emailVerified']:
            #     toast("Please verify your email first.")
            #     return

            if user_data:
                role = user_data.get("role")
                if role == "Admin":
                    self.manager.current = "admin_dashboard"
                else:
                    self.manager.current = "user_dashboard"
            else:
                toast("User data not found.")
        except:
            email.error = True
            password.error = True
            email.helper_text = "Wrong credentials"
            password.helper_text = "Wrong credentials"

    def forgot_password(self):
        from kivymd.toast import toast

        email = self.ids.login_email.text

        if not email or "@" not in email:
            self.ids.login_email.error = True
            self.ids.login_email.helper_text = "Enter a valid email"
            return

        try:
            auth.send_password_reset_email(email)
            toast("Password reset email sent!")
        except Exception as e:
            print(e)
            self.ids.login_email.error = True
            self.ids.login_email.helper_text = "Failed to send reset email"


