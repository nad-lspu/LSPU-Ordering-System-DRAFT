from kivy.uix.screenmanager import Screen
from kivymd.uix.list import MDList
from kivymd.toast import toast
from firebase_config import db
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.utils import get_color_from_hex
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp


class Orders(Screen):
    def on_pre_enter(self):
        self.load_orders()
        self.orders_listener = db.child("orders").stream(self.update_orders)

    def on_enter(self):
        self.load_orders()

    def update_orders(self, message):
        self.load_orders()

    def load_orders(self):
        self.ids.orders_list.clear_widgets()

        try:
            orders_data = db.child("orders").get().val()

            if orders_data:
                for order_id, order in orders_data.items():
                    status = order.get("status", "Pending")
                    bg_color = {
                        "Completed": get_color_from_hex("#E8F5E9"),
                        "Cancelled": get_color_from_hex("#FFEBEE"),
                        "Pending": get_color_from_hex("#FFF8E1")
                    }.get(status, get_color_from_hex("#E3F2FD"))

                    text_color = {
                        "Completed": get_color_from_hex("#2E7D32"),
                        "Cancelled": get_color_from_hex("#C62828"),
                        "Pending": get_color_from_hex("#FF8F00")
                    }.get(status, get_color_from_hex("#1565C0"))

                    card = MDCard(
                        orientation="vertical",
                        size_hint_y=None,
                        height=dp(120),
                        elevation=2,
                        md_bg_color=bg_color,
                        radius=[dp(12)],
                        padding=dp(12),
                        spacing=dp(8)
                    )

                    header = MDBoxLayout(
                        orientation="horizontal",
                        adaptive_height=True,
                        spacing=dp(10)
                    )

                    customer_name = order.get('user', 'N/A').split('@')[0]
                    header.add_widget(MDLabel(
                        text=f"{customer_name}'s Order",
                        font_style="H6",
                        bold=True,
                        size_hint_x=0.6
                    ))

                    status_label = MDLabel(
                        text=status,
                        font_style="Subtitle1",
                        theme_text_color="Custom",
                        text_color=text_color,
                        bold=True,
                        size_hint_x=0.4,
                        halign="right"
                    )
                    header.add_widget(status_label)
                    card.add_widget(header)

                    details = MDBoxLayout(
                        orientation="vertical",
                        adaptive_height=True,
                        spacing=dp(4)
                    )

                    details.add_widget(MDLabel(
                        text=f"Items: {order.get('items', 'N/A')}",
                        font_style="Body2",
                        size_hint_y=None,
                        height=dp(20),
                        shorten=True
                    ))

                    if 'timestamp' in order:
                        details.add_widget(MDLabel(
                            text=f"Placed: {order['timestamp']}",
                            font_style="Caption",
                            size_hint_y=None,
                            height=dp(16),
                            theme_text_color="Secondary"
                        ))

                    card.add_widget(details)

                    if status == "Pending":
                        actions = MDBoxLayout(
                            orientation="horizontal",
                            adaptive_height=True,
                            spacing=dp(10),
                            padding=[0, dp(8), 0, 0]
                        )

                        complete_btn = MDRaisedButton(
                            text="COMPLETE",
                            theme_text_color="Custom",
                            text_color=get_color_from_hex("#FFFFFF"),
                            md_bg_color=get_color_from_hex("#2E7D32"),
                            size_hint_x=0.5,
                            on_release=lambda x, oid=order_id: self.update_order_status(oid, "Completed")
                        )

                        cancel_btn = MDRaisedButton(
                            text="CANCEL",
                            theme_text_color="Custom",
                            text_color=get_color_from_hex("#FFFFFF"),
                            md_bg_color=get_color_from_hex("#C62828"),
                            size_hint_x=0.5,
                            on_release=lambda x, oid=order_id: self.confirm_cancel(oid)
                        )

                        actions.add_widget(complete_btn)
                        actions.add_widget(cancel_btn)
                        card.add_widget(actions)

                    self.ids.orders_list.add_widget(card)
            else:
                empty_label = MDLabel(
                    text="No orders found",
                    halign="center",
                    valign="center",
                    font_style="H6",
                    theme_text_color="Secondary",
                    size_hint_y=None,
                    height=dp(200)
                )
                self.ids.orders_list.add_widget(empty_label)

        except Exception as e:
            error_label = MDLabel(
                text="Failed to load orders. Please try again.",
                halign="center",
                valign="center",
                font_style="H6",
                theme_text_color="Error",
                size_hint_y=None,
                height=dp(200)
            )
            self.ids.orders_list.add_widget(error_label)
            print("Order loading error:", e)

    def confirm_cancel(self, order_id):
        self.dialog = MDDialog(
            title="[size=20][b]Confirm Cancellation[/b][/size]",
            text="[size=16]Are you sure you want to cancel this order?[/size]",
            buttons=[
                MDFlatButton(
                    text="NO",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#757575"),
                    on_release=lambda x: self.dialog.dismiss()
                ),
                MDRaisedButton(
                    text="YES",
                    theme_text_color="Custom",
                    text_color=get_color_from_hex("#FFFFFF"),
                    md_bg_color=get_color_from_hex("#C62828"),
                    on_release=lambda x: [self.update_order_status(order_id, "Cancelled"), self.dialog.dismiss()]
                ),
            ],
            radius=[dp(20), dp(7), dp(20), dp(7)],
        )
        self.dialog.open()

    def update_order_status(self, order_id, new_status):
        try:
            db.child("orders").child(order_id).update({"status": new_status})
            toast(f"Order status updated to {new_status}")
            self.load_orders()
        except Exception as e:
            toast("Failed to update status")
            print(f"Error updating status: {e}")

    def on_leave(self):
        if hasattr(self, 'orders_listener'):
            self.orders_listener.close()