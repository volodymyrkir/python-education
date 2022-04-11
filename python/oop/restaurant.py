"""This module may be useful to automize restaurant work with possibility to deliver orders"""
import datetime
from abc import ABC


class Customer:
    """Class,that describes customers to ease connection with them"""

    def __init__(self, full_name: str, phone_number: str):
        self.full_name = full_name
        self.phone_number = phone_number


class Dish:
    """Class, that describes dishes in restaurant,
     objects used to calculate general price of order"""

    def __init__(self, name: str, calories: int, price: int):
        self.name = name
        self.calories = calories
        self.price = price


class Order(ABC):
    """Abstract class that defines general aspects of an order"""

    def __init__(self, dishes, customer: Customer):
        self.dishes = dishes
        self._date = datetime.date
        self._customer = customer

    def count_sum(self):
        """Method, wich calculates general price of an order"""
        sum = 0
        for dish in self.dishes:
            sum += dish.price
        return sum


class RestaurantOrder(Order):
    """Class, that implements ABC Order, and is for in-place restaurant orders"""

    def __init__(self, dishes, customer: Customer, table: int):
        super().__init__(dishes, customer)
        self.table = table


class EOrder(Order):
    """Class, that implements ABC Order, and is for delivery orders"""

    def __init__(self, dishes, customer: Customer, address: str):
        super().__init__(dishes, customer)
        self.address = address


class Restaurant:
    """Class, which objects are particular restaurants with their own ID`s and budgets"""
    id = 0

    def __init__(self, address: str, budget: int, seats=200):
        Restaurant.id += 1
        self._id = Restaurant.id
        self.address = address
        self.budget = budget
        self.__seats = seats

    def add_customers(self, amount):
        """Method, that implements a possibility of
         controlling the amount of customers for particular restaurant"""
        if self.__seats - amount > 0:
            self.__seats -= amount
            print(f"Need a table for {amount} person(a)")
        else:
            print(f"Sorry, right now we don't have enough seats for {amount} person(s)")

    def rm_customers(self, amount):
        """Method, that subtracts leaving customers from general amount"""
        self.__seats += amount


class Employee(ABC):
    """Abstract class, that defines basic aspects of an employee of restaurant"""
    id = 0

    def __init__(self, salary: float, full_name: str, work_place: Restaurant, payout_card: str):
        Employee.id += 1
        self._id = Employee.id
        self._salary = salary
        self.full_name = full_name
        self._work_place = work_place
        self.payout_card = payout_card

    def receive_salary(self):
        """method, that subtracts salary of employee from restaurant`s budget"""
        if self._work_place.budget < self._salary:
            print(f"Restaurant {self._work_place.id} is out of money")
        else:
            self._work_place.budget -= self._salary


class Waiter(Employee):
    """Class,that implements base class Employee"""

    def __init__(self, salary: float, full_name: str, work_place: Restaurant, payout_card: int):
        super().__init__(salary, full_name, work_place, payout_card)
        self.current_table = 0

    def serve_table(self, table: int):
        """Method, that switches waiter to particular table"""
        print(f"{self.full_name} serving table {table}")
        self.current_table = table

    def make_order(self, dishes_str: str, dishes_calories, dishes_prices, customer: Customer):
        """Method, that makes waiter able to create an order with dishes"""
        parsed_dishes = dishes_str.split(",")
        dishes_list = []
        for i in range(len(parsed_dishes)):
            dishes_list.append(Dish(parsed_dishes[i], dishes_calories[i], dishes_prices[i]))
        order = RestaurantOrder(dishes_list, customer, self.current_table)
        profit = order.count_sum()
        print(f"Restaurant {self._work_place.id} gets {profit} UAH from in-place order")
        self._work_place.budget += profit
        return order


class Cooker(Employee):
    """Class,that implements base class Employee"""

    def make_dishes(self, order):
        """Method, that allows Cooker to make
        a dish(can be developed with time making for every dish)"""
        for dish in order.dishes:
            print(f"{dish.name} is ready by {self.full_name}")


class Courier(Employee):
    """Class,that implements base class Employee"""

    def deliver_order(self, order: EOrder):
        """Method, that allows courier to deliver
        particular e-order to it`s address and receive money from it"""
        profit = order.count_sum()
        print(f"Order is deliverd to {order.address}, restaurant got {profit} UAH")
        self._work_place.budget += profit


class Operator(Employee):
    """Class,that implements base class Employee"""

    def make_eorder(self, dishes_str: str, dishes_calories,
                    dishes_prices, customer: Customer, address):
        """Method, that allows an operator to make an e-order"""
        parsed_dishes = dishes_str.split(",")
        dishes_list = []
        for i in range(len(parsed_dishes)):
            dishes_list.append(Dish(parsed_dishes[i], dishes_calories[i], dishes_prices[i]))
        print(f"{self.full_name} created new e-order, looking for couriers")
        return EOrder(dishes_list, customer, address)


if __name__ == '__main__':
    print(Dish.__doc__)
    r1 = Restaurant("Gagarina,41", 10000, 3)  # Non-delivery restaurant
    w = Waiter(3000, "John Doe", r1, '4441122989976311')
    c1 = Customer("Maybe Baby", "+38095673123")
    r1.add_customers(1)
    w.serve_table(1)
    order1 = w.make_order("ice cream,chicken", [220, 540], [130, 290], c1)
    cook1 = Cooker(6000, "Cooker_man", r1, '453409921233788')
    cook1.make_dishes(order1)
    print(r1.budget)
    w.receive_salary()
    cook1.receive_salary()
    print(r1.budget)

    r2 = Restaurant("MOskovska,32", 17000)  # Delivery restaurant
    o = Operator(4000, "Anna Bell", r2, '4111567432213456')
    c2 = Customer("Crocky Boy", "+38093173123")
    cook2 = Cooker(5500, "Second_cooker", r2, "4433890078665543")
    courier = Courier(2500, "Courier Boy", r2, "8897655432256673")
    order2 = o.make_eorder("Baked CHicken,Borsch,Cesar salad", [500, 315, 311],
                           [300, 250, 290], c2, "Golovnaya,30a")
    cook2.make_dishes(order2)
    courier.deliver_order(order2)
    print(r2.budget)
    o.receive_salary()
    cook2.receive_salary()
    courier.receive_salary()
    print(r2.budget)
