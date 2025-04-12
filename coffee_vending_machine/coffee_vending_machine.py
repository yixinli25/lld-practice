# 1. The coffee vending machine should support different types of coffee, such as espresso, cappuccino, and latte.
# 2. Each type of coffee should have a specific price and recipe (ingredients and their quantities).
# 3. The machine should have a menu to display the available coffee options and their prices.
# 4. Users should be able to select a coffee type and make a payment.
# 5. The machine should dispense the selected coffee and provide change if necessary.
# 6. The machine should track the inventory of ingredients and notify when they are running low.
# 7. The machine should handle multiple user requests concurrently and ensure thread safety.

class Coffee:
    def __init__(self, name: str, price: float, recipe: object):
        self.name = name
        self.price = price
        self.recipe = recipe

    def get_name(self):
        return self.name
    
    def get_price(self):
        return self.price
    
    def get_recipe(self):
        return self.recipe
    

class Ingredient:
    def __init__(self, name: str, quantity: int):
        self.name = name
        self.quantity = quantity

    def get_name(self):
        return self.name
    
    def get_quantity(self):
        return self.quantity
    
    def update_quantity(self, amount):
        self.quantity += amount


class Payment:
    def __init__(self, amount: int):
        self.amount = amount

    def get_amount(self):
        return self.amount
    

class CoffeeMachine:
    _instance = None

    def __init__(self):
        if CoffeeMachine._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            CoffeeMachine._instance = self
            self.coffee_menu = []
            self.ingredients = {}
            self._initialize_ingredients()
            self._initialize_coffee_menu()

    @staticmethod
    def get_instance():
        if CoffeeMachine._instance is None:
            CoffeeMachine()
        return CoffeeMachine._instance
    
    def _initialize_ingredients(self):
        self.ingredients["Coffee"] = Ingredient("Coffee", 10)
        self.ingredients["Water"] = Ingredient("Water", 10)
        self.ingredients["Milk"] = Ingredient("Milk", 10)

    def _initialize_coffee_menu(self):
        espresso_recipe = {
            self.ingredients["Coffee"]: 1,
            self.ingredients["Water"]: 1
        }

        cappuccino_recipe = {
            self.ingredients["Coffee"]: 1,
            self.ingredients["Water"]: 1,
            self.ingredients["Milk"]: 1
        }

        latte_recipe = {
            self.ingredients["Coffee"]: 1,
            self.ingredients["Water"]: 1,
            self.ingredients["Milk"]: 2
        }

        self.coffee_menu.append(Coffee("Espresso", 2.5, espresso_recipe))
        self.coffee_menu.append(Coffee("Cappuccino", 3.5, cappuccino_recipe))
        self.coffee_menu.append(Coffee("Latte", 4.0, latte_recipe))

    def display_menu(self):
        print("Coffee Menu:")
        for coffee in self.coffee_menu:
            print(f"{coffee.get_name()} = ${coffee.get_price()}")

    def select_coffee(self, coffee_name: str):
        for coffee in self.coffee_menu:
            if coffee.get_name().lower() == coffee_name.lower():
                print(f"Selected {coffee.get_name()}")
                return coffee
            
        return None
    
    def dispense_coffee(self, coffee: Coffee, payment: Payment):
        if payment.get_amount() >= coffee.get_price():
            if self._has_enough_ingredients(coffee):
                self._update_ingredients(coffee)
                print(f"Dispensing {coffee.get_name()}...")
                
                change = payment.get_amount() - coffee.get_price()
                if change > 0:
                    print(f"Please collect your change: ${change}")
                
                print(f"Please collect your {coffee.get_name()}")
            else:
                print(f"Insufficient ingredients to make {coffee.get_name()}")
        else:
            print(f"Insufficient payment for {coffee.get_name()}")
            

    def _has_enough_ingredients(self, coffee: Coffee):
        for ingredient, required_quantity in coffee.get_recipe().items():
            if ingredient.get_quantity() < required_quantity:
                return False
        
        return True
    
    def _update_ingredients(self, coffee: Coffee):
        for ingredient, required_quantity in coffee.get_recipe().items():
            ingredient.update_quantity(-required_quantity)
            if ingredient.get_quantity() < 3:
                print(f"Low inventory alert: {ingredient.get_name()}")


class CoffeeVendingMachineDemo:
    @staticmethod
    def run():
        coffee_machine = CoffeeMachine.get_instance()

        coffee_machine.display_menu()

        print("----------------------------------------")

        espresso = coffee_machine.select_coffee("Espresso")
        coffee_machine.dispense_coffee(espresso, Payment(3.0))

        print("----------------------------------------")

        cappuccino = coffee_machine.select_coffee("Cappuccino")
        coffee_machine.dispense_coffee(cappuccino, Payment(3.5))

        print("----------------------------------------")

        latte = coffee_machine.select_coffee("Latte")
        coffee_machine.dispense_coffee(latte, Payment(2.0))

if __name__ == "__main__":
    CoffeeVendingMachineDemo.run()