# coding=utf-8
# imports
import random


# functions
def get_random_string(symbols_count):
    data = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz' + '1234567890'
    return ''.join(random.sample(data, k=symbols_count))

# вынес в отдельній файл для примера