from kivymd.uix.screen import MDScreen

class AdminDashboard(MDScreen):
    def go_to_menu_management(self):
        self.manager.current = "menu_management_screen"

    def go_to_orders(self):
        self.manager.current = "orders_screen"
