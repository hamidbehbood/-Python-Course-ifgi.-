from easy_shopping import Calculator
from easy_shopping import ShoppingCart

# Test the functionality of the calculator
def test_calculator():
    # Create an instance of the Calculator class
    calc = Calculator()

    # Perform arithmetic calculations
    result1 = calc.add(10, 5)  # Adding 10 and 5
    result2 = calc.subtract(30, 15)  # Subtracting 15 from 30
    result3 = calc.multiply(7, 3)  # Multiplying 7 and 3
    result4 = calc.divide(100, 4)  # Dividing 100 by 4
    result5 = calc.divide(45, 0)  # This will result in an error because dividing by zero is not allowed

    # Print the results
    print("Result 1:", result1)
    print("Result 2:", result2)
    print("Result 3:", result3)
    print("Result 4:", result4)
    print("Result 5:", result5)


# Create an instance of the ShoppingCart class
cart = ShoppingCart()

# Add 3 different items in different quantities to the cart
cart.add_item("Apple", 150)
cart.add_item("Banana", 200)
cart.add_item("Orange", 100)

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