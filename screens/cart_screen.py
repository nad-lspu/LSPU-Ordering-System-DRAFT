from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.toast import toast
from kivy.metrics import dp


class CartScreen(MDScreen):
    def on_enter(self):
        self.load_cart()

    def load_cart(self):
        # Clear the current cart list view
        self.ids.cart_list.clear_widgets()

        total_price = 0
        if MenuScreen.cart:
            for item_name in MenuScreen.cart:
                # Get the menu item data from Firebase
                menu_item = db.child("menu").child(item_name).get().val()
                if menu_item:
                    # Add each item to the cart list
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
                        text=menu_item['name'],
                        font_style="H6",
                        theme_text_color="Primary"
                    ))
                    card.add_widget(MDLabel(
                        text=f"Price: ₱{menu_item['price']}",
                        font_style="Subtitle1",
                        theme_text_color="Secondary"
                    ))
                    self.ids.cart_list.add_widget(card)
                    total_price += menu_item['price']
        else:
            self.ids.cart_list.add_widget(MDLabel(
                text="Your cart is empty.",
                halign="center",
                theme_text_color="Hint"
            ))

        # Display the total price
        self.ids.total_price.text = f"Total: ₱{total_price:.2f}"

    def clear_cart(self):
        # Clear the cart list
        MenuScreen.cart = []
        self.load_cart()  # Reload the cart

    def checkout(self):
        if not MenuScreen.cart:
            toast("Your cart is empty!")
        else:
            # Proceed with checkout logic (e.g., create order in Firebase)
            toast("Proceeding to checkout...")
