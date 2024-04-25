from exercise_3.calculator import Calculator
from exercise_3.shopping import ShoppingCart 
def main():
    # This part Create an instance of the Calculator class
    calc = Calculator()
    
    # Test the input value
    try:
        result1 = calc.sum(7, 5)
        print(f"7 + 5 = {result1}")

        result2 = calc.subtract(34, 21)
        print(f"34 - 21 = {result2}")

        result3 = calc.multiply(54, 2)
        print(f"54 * 2 = {result3}")

        result4 = calc.divide(144, 2)
        print(f"144 / 2 = {result4}")

        # in case you divide a number to zero This will raise a ValueError
        result5 = calc.divide(45, 0)
        print(f"45 / 0 = {result5}")  # This line won't be reached due to exception

    except ValueError as e:
        print(f"Error: {e}")
    # Test the Shopping Card Class
    # Example usage
    # Create an instance of the ShoppingCart class
    cart = ShoppingCart()

    # Add items to the shopping cart
    cart.add_item("Kiwi", 234)
    cart.add_item("Benana", 289)
    cart.add_item("Orange", 100)  
    cart.display_item()
    cart.remove_item("Orange")
if __name__ == "__main__":
    main()
