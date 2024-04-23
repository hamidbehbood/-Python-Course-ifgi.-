
# Here we defined the class
class Calculator:

    def sum(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        # in case you divide a number to zero This will raise a ValueError
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        return a / b
