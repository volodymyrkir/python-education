"""This module can be used to check on some attributes of vehicles module"""


class Descriptor:

    def __set_name__(self, owner, name):
        self.name=name

    def __get__(self, instance, owner):
        print(f"Retrieving {instance}`s attribute {self.name}")
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if value<0:
            raise ValueError('This attribute should be positive!')
        print(f"Setting to {instance}`s {self.name} attribute to value {value}")
        instance.__dict__[self.name]=value

    def __delete__(self, instance):
        print(f"Deleting {self.name} attribute of {instance}")
        del(instance.__dict__[self.name])

