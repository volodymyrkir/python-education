# Exercise 1
print("Hello, World!")

# Exercise 2
mystring = "hello"
myfloat = 10.0
myint = 20

# Exercise 3
numbers = []
strings = []
names = ["John", "Eric", "Jessica"]
for i in range(1, 4):
    numbers.append(i)
strings.append('hello ')
strings.append('world')
second_name = names[1]

# Exercise 4
x = object()
y = object()
x_list = [x] * 10
y_list = [y] * 10
big_list = x_list + y_list

# Exercise 5
# data = ("John", "Doe", 53.44)
# format_string = "Hello %s %s. Your current balance is $%s."
# print(format_string % data)
data = ("John", "Doe", 53.44)
format_string = "Hello {} {}.Your current balance is {}$".format(data[0], data[1], data[2])
print(format_string)

# Exercise 6
s = "Twenty gacacter ezy!"
print("Length of s = %d" % len(s))
print("The first occurrence of the letter a = %d" % s.index("a"))
print("a occurs %d times" % s.count("a"))
print("The first five characters are '%s'" % s[:5])  # Start to 5
print("The next five characters are '%s'" % s[5:10])  # 5 to 10
print("The thirteenth character is '%s'" % s[12])  # Just number 12
print("The characters with odd index are '%s'" % s[1::2])  # (0-based indexing)
print("The last five characters are '%s'" % s[-5:])  # 5th-from-last to end
print("String in uppercase: %s" % s.upper())
print("String in lowercase: %s" % s.lower())
if s.startswith("Twe"):
    print("String starts with 'Twe'. Good!")
if s.endswith("ezy!"):
    print("String ends with 'ezy!'. Good!")
print("Split the words of the string: %s" % s.split(" "))

# Exercise 7
number = 16
second_number = 0
first_array = [1, 2, 3]
second_array = [1, 2]

if number > 15:
    print("1")

if first_array:
    print("2")

if len(second_array) == 2:
    print("3")

if len(first_array) + len(second_array) == 5:
    print("4")

if first_array and first_array[0] == 1:
    print("5")

if not second_number:
    print("6")

# Exercise 8
numbers = [
    951, 402, 984, 651, 360, 69, 408, 319, 601, 485, 980, 507, 725, 547, 544,
    615, 83, 165, 141, 501, 263, 617, 865, 575, 219, 390, 984, 592, 236, 105, 942, 941,
    386, 462, 47, 418, 907, 344, 236, 375, 823, 566, 597, 978, 328, 615, 953, 345,
    399, 162, 758, 219, 918, 237, 412, 566, 826, 248, 866, 950, 626, 949, 687, 217,
    815, 67, 104, 58, 512, 24, 892, 894, 767, 553, 81, 379, 843, 831, 445, 742, 717,
    958, 609, 842, 451, 688, 753, 854, 685, 93, 857, 440, 380, 126, 721, 328, 753, 470,
    743, 527
]
for number in numbers:
    if number == 237:
        break
    if number % 2 == 0:
        print(number)


# Exercise 9
def list_benefits():
    return ["More organized code", "More readable code", "Easier code reuse",
            "Allowing programmers to share and connect code together"]


# Modify this function to concatenate to each benefit - " is a benefit of functions!"
def build_sentence(benefit):
    return benefit + " is a benefit of functions!"


def name_the_benefits_of_functions():
    list_of_benefits = list_benefits()
    for benefit in list_of_benefits:
        print(build_sentence(benefit))


name_the_benefits_of_functions()


# Exercise 9 part 2
def foo(a, b, c, *args):
    return len(list(args))


def bar(a, b, c, **kwargs):
    return kwargs.get("magicnumber") == 7


# test code
if foo(1, 2, 3, 4) == 1:
    print("Good.")
if foo(1, 2, 3, 4, 5) == 2:
    print("Better.")
if bar(1, 2, 3, magicnumber=6) == False:
    print("Great.")
if bar(1, 2, 3, magicnumber=7) == True:
    print("Awesome!")

# Exercise 11
phonebook = {
    "John": 938477566,
    "Jack": 938377264,
    "Jill": 947662781
}
del phonebook["Jill"]
phonebook["Jake"] = 938273443
# testing code
if "Jake" in phonebook:
    print("Jake is listed in the phonebook.")

if "Jill" not in phonebook:
    print("Jill is not listed in the phonebook.")

# Exercise 12
a = ["Jake", "John", "Eric"]
b = ["John", "Jill"]
print(set(a).symmetric_difference(set(b)))

# Exercise 14
import re
# Your code goes here
find_members = sorted([word for word in dir(re) if "find" in word])