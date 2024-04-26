from calculator import Calculator

# Create an instance of the Calculator class
calc = Calculator()

# Perform the calculations
result1 = calc.add(7, 5)
result2 = calc.subtract(34, 21)
result3 = calc.multiply(54, 2)
result4 = calc.divide(144, 2)
result5 = calc.divide(45, 0)  # This will result in an error

# Print the results
print("Result 1:", result1)
print("Result 2:", result2)
print("Result 3:", result3)
print("Result 4:", result4)
print("Result 5:", result5)

from shopping import ShoppingCart

# Create an instance of the ShoppingCart class
cart = ShoppingCart()

# Add 3 different items in different quantities to the cart
cart.add_item("Apple", 3)
cart.add_item("Banana", 2)
cart.add_item("Orange", 1)

# Display the current items in the cart
print("Current items in the cart:")
for item_name, qty in cart.items:
    print(f"- {qty} {item_name}")

# Calculate the total quantity
total_items = cart.calculate_total()
print("Total items in the cart:", total_items)

# Remove an item from the cart
cart.remove_item("Banana")

# Display the updated items in the cart
print("Updated items in the cart after removing Banana:")
for item_name, qty in cart.items:
    print(f"- {qty} {item_name}")

# Recalculate the total quantity
total_items_after_removal = cart.calculate_total()
print("Total items in the cart after removing Banana:", total_items_after_removal)

print("All tests passed successfully!")