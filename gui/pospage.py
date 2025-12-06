import tkinter as tk

BG_COLOR = "#2B0505"        # Main Background
SECTION_BG = "#550a0a"      # Lighter sections
BTN_RED = "#AA3333"         # Buttons
TEXT_WHITE = "#FFFFFF"

# 1. Mock Menu Data for demonstration
MOCK_MENU = {
    "APPETIZERS": [
        {"name": "Mozzarella Sticks", "price": "7.99"},
        {"name": "Loaded Fries", "price": "9.50"},
        {"name": "Garlic Knots", "price": "5.00"},
        {"name": "Spinach Dip", "price": "10.00"},
        {"name": "Onion Rings", "price": "6.50"},
        {"name": "Buffalo Wings", "price": "12.00"},
        {"name": "Shrimp Cocktail", "price": "15.00"},
        {"name": "Bruschetta", "price": "8.00"},
    ],
    "MAIN COURSES": [
        {"name": "Grilled Salmon", "price": "18.99"},
        {"name": "Steak Frites", "price": "25.99"},
        {"name": "Chicken Alfredo", "price": "16.50"},
        {"name": "Veggie Stir Fry", "price": "14.00"},
        {"name": "Spicy Burger", "price": "12.00"},
        {"name": "Ribeye Steak", "price": "30.00"},
        {"name": "Pork Chops", "price": "19.50"},
        {"name": "Vegan Curry", "price": "14.50"},
        {"name": "Taco Plate", "price": "13.00"},
    ],
    "DESSERTS": [
        {"name": "Chocolate Cake", "price": "6.00"},
        {"name": "Ice Cream Sundae", "price": "5.50"},
        {"name": "Apple Pie", "price": "6.50"},
        {"name": "Tiramisu", "price": "7.00"},
    ],
    # Add empty lists for other categories to avoid errors
    "DRINKS": [], "SIDES": [], "SPECIALS": [], "SALADS": [], "PASTA": [], "BURGERS": [], "PIZZA": []
}

class POSDashboard(tk.Toplevel):
    def __init__(self, parent=None):
        # Fix the custom constructor name
        super().__init__(parent) 
        self.title("SmartChef - POS")
        self.geometry("1200x700")
        self.configure(bg=BG_COLOR)
        
        # Main Layout: 3 Columns
        # 1. MENU SECTION (Left) - Use a content frame for dynamic swapping
        self.frame_menu = tk.Frame(self, bg=SECTION_BG, width=300, padx=10, pady=10)
        self.frame_menu.pack(side="left", fill="y", padx=(10, 5), pady=10)
        self.frame_menu.pack_propagate(False)
        
        # Frame to hold the dynamic content (Categories or Items)
        self.menu_content_frame = tk.Frame(self.frame_menu, bg=SECTION_BG)
        self.menu_content_frame.pack(fill="both", expand=True)

        self.build_menu_section()

        # 2. CURRENT ORDER (Center)
        self.frame_order = tk.Frame(self, bg=SECTION_BG, width=400, padx=10, pady=10)
        self.frame_order.pack(side="left", fill="both", expand=True, padx=5, pady=10)
        self.build_order_section()

        # 3. CHECKOUT (Right)
        self.frame_checkout = tk.Frame(self, bg=SECTION_BG, width=300, padx=20, pady=20)
        self.frame_checkout.pack(side="right", fill="y", padx=(5, 10), pady=10)
        self.frame_checkout.pack_propagate(False)
        self.build_checkout_section()

    def clear_menu_content(self):
        """Removes all widgets from the dynamic menu content frame."""
        for widget in self.menu_content_frame.winfo_children():
            widget.destroy()

    def build_menu_section(self):
        """Displays the Menu Categories grid."""
        self.clear_menu_content()
        
        tk.Label(self.menu_content_frame, text="MENU CATEGORIES", font=("Segoe UI", 14, "bold"), bg=SECTION_BG, fg="white").pack(pady=(0, 10))
        
        # Grid of buttons
        categories = [
            "APPETIZERS", "MAIN COURSES", 
            "DESSERTS", "DRINKS", 
            "SIDES", "SPECIALS",
            "SALADS", "PASTA",
            "BURGERS", "PIZZA"
        ]
        
        btn_frame = tk.Frame(self.menu_content_frame, bg=SECTION_BG)
        btn_frame.pack(fill="both", expand=True)

        for i, cat in enumerate(categories):
            # Command now calls show_menu_items with the category name
            command = lambda c=cat.replace('\n', ' '): self.show_menu_items(c.strip())
            btn = tk.Button(btn_frame, text=cat, bg=BTN_RED, fg="white", 
                             font=("Segoe UI", 10, "bold"), relief="flat", height=3, command=command)
            btn.grid(row=i//2, column=i%2, sticky="nsew", padx=5, pady=5)
        
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

    def show_menu_items(self, category_name):
        """Displays a scrollable grid of menu items for the selected category."""
        self.clear_menu_content()
        
        # Header with back button
        header_frame = tk.Frame(self.menu_content_frame, bg=SECTION_BG)
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Back Button
        tk.Button(header_frame, text="< BACK", bg=BTN_RED, fg="white", 
                  font=("Segoe UI", 10, "bold"), relief="flat", height=1, 
                  command=self.build_menu_section).pack(side="left", padx=(0, 10))
        
        # Category Title
        tk.Label(header_frame, text=category_name, font=("Segoe UI", 14, "bold"), bg=SECTION_BG, fg="white").pack(side="left", fill="x", expand=True)
        
        # Scrollable Area for Items using Canvas and Scrollbar
        item_canvas = tk.Canvas(self.menu_content_frame, bg=SECTION_BG, highlightthickness=0)
        item_scrollbar = tk.Scrollbar(self.menu_content_frame, orient="vertical", command=item_canvas.yview)
        
        scrollable_frame = tk.Frame(item_canvas, bg=SECTION_BG)
        
        # Attach the scrollable frame to the canvas
        item_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", 
                                   width=self.frame_menu.winfo_width() - 30) # Adjust width for scrollbar/padding

        # Configure the canvas to know when to scroll
        scrollable_frame.bind(
            "<Configure>",
            lambda e: item_canvas.configure(
                scrollregion=item_canvas.bbox("all")
            )
        )
        item_canvas.configure(yscrollcommand=item_scrollbar.set)
        
        item_scrollbar.pack(side="right", fill="y")
        item_canvas.pack(side="left", fill="both", expand=True)
        
        # Get items for the selected category
        items = MOCK_MENU.get(category_name, [])

        if not items:
            tk.Label(scrollable_frame, text=f"No items found for {category_name}.", 
                     bg=SECTION_BG, fg="white", font=("Segoe UI", 12)).pack(pady=50, padx=20)
            return

        # Loop through items and create buttons
        for i, item in enumerate(items):
            # Item button/card showing name and price
            item_btn = tk.Button(scrollable_frame, 
                                 text=f"{item['name']}\n${item['price']}", 
                                 bg=BTN_RED, fg="white", 
                                 font=("Segoe UI", 10, "bold"), relief="flat", height=3, 
                                 # Placeholder: This is where you would call a function to add the item to the order
                                 command=lambda n=item['name'], p=item['price']: print(f"Added {n} (${p}) to order"))
            
            # Place the buttons in a two-column grid
            item_btn.grid(row=i//2, column=i%2, sticky="nsew", padx=5, pady=5)
        
        # Ensure the columns expand equally within the scrollable frame
        scrollable_frame.columnconfigure(0, weight=1)
        scrollable_frame.columnconfigure(1, weight=1)


    def build_order_section(self):
        tk.Label(self.frame_order, text="CURRENT ORDER", font=("Segoe UI", 14, "bold"), bg=SECTION_BG, fg="white").pack(pady=(0, 10))

        # Header for list
        hdr = tk.Frame(self.frame_order, bg=SECTION_BG)
        hdr.pack(fill="x")
        tk.Label(hdr, text="Quantity | Name", bg=SECTION_BG, fg="white", font=("Segoe UI", 10, "bold")).pack(side="left")
        tk.Label(hdr, text="Price", bg=SECTION_BG, fg="white", font=("Segoe UI", 10, "bold")).pack(side="right")

        # Scrollable List Placeholder (Using Frame for styling)
        list_area = tk.Frame(self.frame_order, bg=SECTION_BG)
        list_area.pack(fill="both", expand=True, pady=10)
        
        items = [
            ("2x", "Spicy Burger", "$24.00"),
            ("1x", "Cobb Salad", "$12.50"),
            ("3x", "Iced Tea", "$9.00"),
            ("1x", "Choco Lava Cake", "$8.00"),
        ]

        for qty, name, price in items:
            row = tk.Frame(list_area, bg=SECTION_BG)
            row.pack(fill="x", pady=5)
            tk.Label(row, text=f"{qty}   {name}", bg=SECTION_BG, fg="white", font=("Segoe UI", 12)).pack(side="left")
            tk.Label(row, text=price, bg=SECTION_BG, fg="white", font=("Segoe UI", 12)).pack(side="right")

    def build_checkout_section(self):
        tk.Label(self.frame_checkout, text="CHECKOUT", font=("Segoe UI", 14, "bold"), bg=SECTION_BG, fg="white").pack(pady=(0, 20))

        # Totals
        self.add_total_row("Subtotal:", "$53.50", 16)
        self.add_total_row("Tax:", "$4.82", 14)
        
        tk.Frame(self.frame_checkout, bg="white", height=2).pack(fill="x", pady=20)
        
        self.add_total_row("Total:", "$58.32", 22, bold=True)

        # Big Button
        btn = tk.Button(self.frame_checkout, text="SEND TO\nKITCHEN", bg="#CC3333", fg="white",
                         font=("Segoe UI", 16, "bold"), relief="flat", height=3, cursor="hand2")
        btn.pack(side="bottom", fill="x", pady=20)

    def add_total_row(self, label, value, size, bold=False):
        font_style = ("Segoe UI", size, "bold" if bold else "normal")
        row = tk.Frame(self.frame_checkout, bg=SECTION_BG)
        row.pack(fill="x", pady=5)
        tk.Label(row, text=label, bg=SECTION_BG, fg="white", font=font_style).pack(side="left")
        tk.Label(row, text=value, bg=SECTION_BG, fg="white", font=font_style).pack(side="right")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    # Correct the custom constructor name here as well
    app = POSDashboard() 
    root.mainloop()