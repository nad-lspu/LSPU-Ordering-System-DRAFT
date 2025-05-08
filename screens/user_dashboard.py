from kivymd.uix.screen import MDScreen
from kivymd.toast import toast
from firebase_config import auth, db
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.metrics import dp

class UserDashboard(MDScreen):
    def on_pre_enter(self):
        self.load_user_data()
        self.load_order_history()

    def load_user_data(self):
        try:
            user = auth.current_user
            if user:
                user_id = user['localId']
                user_data = db.child("users").child(user_id).get().val()
                if user_data:
                    self.ids.user_name.text = user_data.get("name", "No Name")
                    self.ids.user_email.text = user_data.get("email", "No Email")
        except Exception as e:
            toast(f"Error loading data: {e}")

    def load_order_history(self):
        try:
            user = auth.current_user
            if user:
                user_id = user['localId']
                orders = db.child("orders").order_by_child("user").equal_to(user_id).get().val()
                self.ids.order_history.clear_widgets()
                if orders:
                    for order_id, order_data in orders.items():
                        card = MDCard(
                            orientation='vertical',
                            padding=dp(10),
                            size_hint_y=None,
                            height=dp(100),
                            ripple_behavior=True,
                            radius=[12],
                            elevation=6
                        )
                        card.add_widget(MDLabel(
                            text=f"Order #{order_id}",
                            font_style="Subtitle1",
                            theme_text_color="Primary"
                        ))
                        card.add_widget(MDLabel(
                            text=f"Status: {order_data.get('status', 'unknown')}",
                            font_style="Caption",
                            theme_text_color="Secondary"
                        ))
                        card.bind(on_release=lambda instance, oid=order_id: self.view_order_details(oid))
                        self.ids.order_history.add_widget(card)
                else:
                    self.ids.order_history.add_widget(MDLabel(
                        text="No orders found.",
                        halign="center",
                        theme_text_color="Hint"
                    ))
        except Exception as e:
            toast(f"Error loading orders: {e}")

    def view_order_details(self, order_id):
        """Minimal implementation (expand later)"""
        toast(f"Order details: {order_id}")

    def navigate_to_menu(self):
        self.manager.current = "menu_screen"

    def logout(self):
        auth.current_user = None
        self.manager.current = "login_screen"