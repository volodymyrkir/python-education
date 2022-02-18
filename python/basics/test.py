import time
from file import CapitalsFileManager

c=CapitalsFileManager("capitals.txt")
c.print_file()
c.write_capital("", "kyiv")
print(c.write_capital.__doc__)
c.write_capital("belarus","minsk")
for i in range(10):         #Мониторим файл:)
    time.sleep(5)
    c.print_file()