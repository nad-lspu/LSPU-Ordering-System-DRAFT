from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivy.uix.button import Button

from screens.admin_dashboard import AdminDashboard
from screens.user_dashboard import UserDashboard
from screens.menu_screen import Menu
from screens.orders_screen import Orders
from screens.menu_management_screen import MenuManagement

class GrabPiyudApp(MDApp):
    def build(self):
        self.screen_manager = ScreenManager()

        # Add screens for user and admin
        self.screen_manager.add_widget(AdminDashboard(name="admin_dashboard"))
        self.screen_manager.add_widget(UserDashboard(name="user_dashboard"))
        self.screen_manager.add_widget(Menu(name="menu_screen"))
        self.screen_manager.add_widget(Orders(name="orders_screen"))
        self.screen_manager.add_widget(MenuManagement(name="menu_management_screen"))

        # Set flag for testing (change between "user" or "admin" for testing)
        self.testing_role = "admin"  # "user" or "admin"

        if self.testing_role == "admin":
            self.change_screen("admin_dashboard")
        elif self.testing_role == "user":
            self.change_screen("user_dashboard")

        return self.screen_manager

    def change_screen(self, screen_name):
        self.screen_manager.current = screen_name

    def logout(self):
        self.change_screen("login_screen")  # Redirect to login if needed

