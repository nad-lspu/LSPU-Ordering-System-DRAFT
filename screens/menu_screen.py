from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.toast import toast
from firebase_config import db
from kivy.metrics import dp


class MenuScreen(MDScreen):
    cart = []

    def on_enter(self):
        self.load_menu()

    def load_menu(self):
        try:
            menu_items = db.child("menu").get().val()
            if menu_items:
                self.ids.menu_list.clear_widgets()
                for item_name, item_data in menu_items.items():
                    card = MDCard(
                        orientation='vertical',
                        padding=dp(10),
                        size_hint_y=None,
                        height=dp(140),
                        ripple_behavior=True,
                        radius=[12],
                        elevation=6
                    )
                    card.add_widget(MDLabel(
                        text=item_data.get('name'),
                        font_style="H6",
                        theme_text_color="Primary"
                    ))
                    card.add_widget(MDLabel(
                        text=f"Price: ${item_data.get('price')}",
                        font_style="Subtitle1",
                        theme_text_color="Secondary"
                    ))

                    add_button = MDRaisedButton(
                        text="Add to Cart",
                        size_hint_y=None,
                        height=dp(40),
                        pos_hint={"center_x": 0.5},
                        on_release=lambda x=item_name: self.add_to_cart(x)
                    )
                    card.add_widget(add_button)

                    self.ids.menu_list.add_widget(card)
            else:
                self.ids.menu_list.add_widget(MDLabel(
                    text="No menu items available.",
                    halign="center",
                    theme_text_color="Hint"
                ))
        except Exception as e:
            toast(f"Error loading menu: {e}")

    def add_to_cart(self, item_name):
        self.cart.append(item_name)
        toast(f"Added {item_name} to the cart.")

    def navigate_to_cart(self):
        self.manager.current = "cart_screen"

    def checkout(self):
        if not self.cart:
            toast("Your cart is empty!")
        else:
            toast("Proceeding to checkout...")
