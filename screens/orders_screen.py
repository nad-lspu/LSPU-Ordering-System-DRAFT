from kivy.uix.screenmanager import Screen
from kivymd.uix.list import TwoLineAvatarIconListItem, IconRightWidget
from kivymd.toast import toast
from firebase_config import db
from kivymd.uix.list import OneLineListItem

class Orders(Screen):
    def on_pre_enter(self):
        self.load_orders()
        self.orders_listener = db.child("orders").stream(self.update_orders)

    def update_orders(self, message):
        self.load_orders()

    def load_orders(self):
        self.ids.orders_list.clear_widgets()

        try:
            orders_data = db.child("orders").get().val()

            if orders_data:
                for order_id, order in orders_data.items():
                    item = TwoLineAvatarIconListItem(
                        text=f"{order['user']} - {order['status']}",
                        secondary_text=order["items"]
                    )

                    complete_icon = IconRightWidget(
                        icon="check-circle",
                        on_release=lambda x, oid=order_id: self.update_order_status(oid, "Completed")
                    )

                    cancel_icon = IconRightWidget(
                        icon="close-circle",
                        on_release=lambda x, oid=order_id: self.update_order_status(oid, "Cancelled")
                    )

                    item.add_widget(complete_icon)
                    item.add_widget(cancel_icon)

                    self.ids.orders_list.add_widget(item)
            else:
                self.ids.orders_list.add_widget(
                    OneLineListItem(
                        text="No orders found.",
                        theme_text_color="Hint",
                        font_style="Subtitle1"
                    )
                )

        except Exception as e:
            self.ids.orders_list.add_widget(
                OneLineListItem(
                    text="Failed to load orders. Please try again.",
                    theme_text_color="Error",
                    font_style="Subtitle1"
                )
            )
            print("Order loading error:", e)

    def update_order_status(self, order_id, new_status):
        try:
            db.child("orders").child(order_id).update({"status": new_status})
            toast(f"Order status updated to {new_status}.")
        except Exception as e:
            toast("Failed to update status.")
            print(f"Error updating status: {e}")

    def on_stop(self):
        if hasattr(self, 'orders_listener'):
            self.orders_listener.close()

