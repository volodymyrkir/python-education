import os


class CapitalsFileManager:

    def __init__(self, filepath):
        self.filepath = filepath

    def print_file(self):
        if not os.path.isfile(self.filepath):
            print("Current filepath does not exist")
        else:
            with open(self.filepath, 'r') as f:
                for string in f.readlines():
                    if not string:
                        break
                    print(f"The capital of {string.split()[0]} is {string.split()[1]}")

    def write_capital(self, country: str, capital: str):
        """Добавляем страну и столицу (строго в формате \"country capital\")"""
        if not country or not capital:
            print("Use non-empty strings")
        else:
            with open(self.filepath, 'a') as f:
                f.write(f"\n{country} {capital}")
