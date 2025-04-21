from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

class AdminDashboard(MDScreen):
    def on_enter(self):
        app = MDApp.get_running_app()
        print(f"Admin logged in: {app.admin_name}")
