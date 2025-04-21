from kivymd.uix.screen import MDScreen

class UserDashboard(MDScreen):
    def go_to_menu(self):
        self.manager.current = "menu_screen"

    def go_to_my_orders(self):
        self.manager.current = "orders_screen"
