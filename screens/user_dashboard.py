from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import ScrollView
from kivymd.uix.card import MDCard
from kivymd.toast import toast
from firebase_config import db

class UserDashboard(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_orders = []
        self.load_user_orders()

    def load_user_orders(self):
        # Load orders from Firebase for the current user
        user_id = "current_user_id"  # Replace with actual user data
        order_data = db.child("orders").order_by_child("user_id").equal_to(user_id).get().val()

        if order_data:
            self.user_orders = [order for order in order_data]
        else:
            self.user_orders = []

    def display_orders(self):
        layout = self.ids.user_orders_layout
        layout.clear_widgets()

        if not self.user_orders:
            layout.add_widget(MDLabel(text="No orders yet", halign="center"))

        for order in self.user_orders:
            card = MDCard(
                orientation="vertical",
                size_hint=(None, None),
                size=("280dp", "150dp"),
                padding="10dp",
                elevation=10,
                radius=[25, 25, 25, 25],
                pos_hint={"center_x": 0.5},
                on_release=lambda order=order: self.view_order_details(order)
            )
            card.add_widget(MDLabel(text=f"Order #{order['order_id']}", halign="center"))
            card.add_widget(MDLabel(text=f"Status: {order['status']}", halign="center"))
            layout.add_widget(card)

    def view_order_details(self, order):
        # Display order details in a new screen or popup
        details_screen = self.manager.get_screen('order_details')
        details_screen.load_order_details(order)
        self.manager.current = "order_details"

    def logout(self):
        # For logging out, you can add a method to handle user session ending
        toast("Logging out...")
        self.manager.current = "login_screen"
