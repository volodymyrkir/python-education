"""This module is used to work with different vehicles"""
from abc import ABC, abstractmethod


class Engine(ABC):
    """Abstract class, that defines some methods for subclasses"""

    def __init__(self, power, fuel_use):
        """Magical method that initiates an Engine part of subclasses based on Engine"""
        self._power = power
        self._fuel_use = fuel_use

    def __lt__(self, other):
        """Magical method that implements comparison for objects that have engines"""
        return self._power < other._power

    def __gt__(self, other):
        """Magical method that implements comparison for objects that have engines"""
        return self._power > other._power

    @abstractmethod
    def test_eng(self):
        """Abstract method that is needed in subclasses of the Engine class"""
        pass


class Transport(ABC):
    """Abstract class for any transport"""
    vehicles = 0

    def __init__(self, speed_kmh: float, seats: int, weight: float):
        """Magical method that initiates the Transport part of subclasses"""
        if speed_kmh < 0:
            self._speed_kmh = 0
        else:
            self._speed_kmh = speed_kmh
        self.seats = seats
        self.weight = weight

    def __lt__(self, other):
        """Magical method that implements comparison for objects that are transport"""
        return self._speed_kmh < other._speed_kmh

    def __gt__(self, other):
        """Magical method that implements comparison for objects that are transport"""
        return self._speed_kmh > other._speed_kmh

    def __bool__(self):
        """Magical method that implements conversion to bool for objects that are transport"""
        return self.weight > 0

    def __neg__(self):
        """Magical method that overloads unary subtraction for setting speed to 0"""
        self._speed_kmh = 0

    def __pos__(self):
        """Magical method that overloads unary + symbol to increment seats in vehicle"""
        self.seats += 1

    @property
    def speed(self):
        """Property that shows the speed of vehicle"""
        print(f"Speed of this vehicle is {self._speed_kmh} kms per hour")

    @speed.setter
    def speed(self, new):
        """property setter which sets new value to protected field and reflects to console"""
        self._speed_kmh = new
        print(f"New speed of this vehicle is {self._speed_kmh} kms per hour")

    @abstractmethod
    def drive(self):
        """Drive method, that needs to be implemented in subclasses"""
        pass

    @staticmethod
    def is_fast(speed_kmh):
        """Static method that shows, whether the vehicle is fast"""
        if speed_kmh > 80:
            print("Vehicle is pretty fast!")
        else:
            print("Vehicle is slow")

    @classmethod
    def get_total(cls):
        """class method, that shows amount of vehicles at all"""
        print(f"We have {cls.vehicles} vehicles ready!")


class Car(Transport, Engine):
    """Class, that represents car as subclass of Transport and Engine"""
    cars = 0

    def __init__(self, speed_kmh: float, seats: int, weight: float, brand: str, power: int, fuel_use: float):
        """Magical method that initiates a Car"""
        Transport.__init__(self, speed_kmh, seats, weight)
        Engine.__init__(self, power, fuel_use)
        self.brand = brand

    def __new__(cls, *args, **kwargs):
        """Magical method that increments amount of cars and vehicles"""
        Transport.vehicles += 1
        cls.cars += 1
        return object.__new__(cls)

    def test_eng(self):
        """Method, that interconnects with engine in vehicle"""
        print(f"Car tests it's {self._power} kW engine which consumes {self._fuel_use} l. fuel per hour")

    def drive(self):
        """Implementation of an abstract method drive for car"""
        print(f"{self.brand} сar is driving with speed {self._speed_kmh}")

    @classmethod
    def get_total(cls):
        """Method, that shows amount of cars in project"""
        print(f"We have {cls.cars} cars ready!")


class Bus(Transport, Engine):
    """Class, that represents bus as subclass of Transport and Engine"""
    buses = 0

    def __init__(self, speed_kmh: float, weight: float, power: int, fuel_use: float, seats: int = 24):
        """Magical method that initiates a Bus"""
        Transport.__init__(self, speed_kmh, seats, weight)
        Engine.__init__(self, power, fuel_use)

    def __new__(cls, *args, **kwargs):
        """Magical method that increments amount of buses and vehicles"""
        Transport.vehicles += 1
        cls.buses += 1
        return object.__new__(cls)

    def drive(self):
        """Implementation of an abstract method drive for bus"""
        print(f"Bus is driving with speed {self._speed_kmh}")

    def test_eng(self):
        """Method, that interconnects with engine in vehicle"""
        print(f"Bus tests it's {self._power} kW engine which consumes {self._fuel_use} l. fuel per hour")

    @classmethod
    def get_total(cls):
        """Method, that shows amount of buses in project"""
        print(f"We have {cls.buses} buses ready!")


class Bicycle(Transport):
    """Class, that represents bicycle as subclass of Transport and Engine"""
    bicycles = 0

    def __init__(self, speed_kmh: float, weight: float, type: str, seats: int = 1):
        """Magical method that initiates a Bus"""
        super().__init__(speed_kmh, seats, weight)
        self.type = type

    def __new__(cls, *args, **kwargs):
        """Magical method that increments amount of bicycles and vehicles"""
        Transport.vehicles += 1
        cls.bicycles += 1
        return object.__new__(cls)

    def drive(self):
        """Implementation of an abstract method drive for bicycle"""
        print(f"{self.type} bicycle is driving with speed {self._speed_kmh}")

    @classmethod
    def get_total(cls):
        """Method, that shows amount of bicycles in project"""
        print(f"We have {cls.bicycles} bicycles ready!")


class Wagon(Transport):
    """Method, that shows amount of wagons in project"""
    wagons = 0

    def __init__(self, weight: float, horses: int, seats: int = 1):
        """Magical method that initiates a wagon"""
        super().__init__(horses * 10, seats, weight)
        self.horses = horses

    def __new__(cls, *args, **kwargs):
        """Magical method that increments amount of wagons and vehicles"""
        Transport.vehicles += 1
        cls.wagons += 1
        return object.__new__(cls)

    def drive(self):
        """Implementation of an abstract method drive for wagon"""
        print(f"Wagon with {self.horses} horses is driving with speed {self._speed_kmh}")

    @classmethod
    def get_total(cls):
        """Method, that shows amount of wagons in project"""
        print(f"We have {cls.wagons} bicycles ready!")


if __name__ == "__main__":
    c = Car(30, 2, 500, "Subaru", 350, 1.5)
    c.drive()
    b = Bus(20, 700, 330, 1.2)
    b.drive()
    print(b < c)
    bi = Bicycle(9, 7, "Mountain")
    w = Wagon(90, 3)
    -w
    w.speed
    print(bi > w)
    c1 = Car(-5, 3, 0, "Kia", 290, 0.6)
    +c1
    print(c1.seats)
    print(bool(c1))
    Transport.is_fast(61)
    Transport.get_total()
    Bus.get_total()
