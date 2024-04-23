# Define a class called ShoppingCart to represent a shopping cart
class ShoppingCart:
    # Initialize the shopping cart with an empty list of items
    def __init__(self):
        self.items = []
        

    # Add an item with a name and quantity to the shopping cart
    def add_item(self, item_name, qty):
        item = (item_name, qty)
        self.items.append(item)
        
    # Remove an item with a specific name from the shopping cart
    def remove_item(self, item_name):
        for item in self.items:
            if item[0] == item_name:
                self.items.remove(item)
                self.calculate_total()
                self.display_item()
                break

    # Calculate and return the total quantity of items in the shopping cart
    def calculate_total(self):
        total = 0
        for item in self.items:
            total += item[1]
        return total

    # Display the current items in the cart and Show the total quantity
    def display_item(self):
         print("Current Items in Cart:")
         for item in self.items:
           print(item[0], "-", item[1])
         print(f"{ 'Total Item counts is :' + str(self.calculate_total()) }")
          
