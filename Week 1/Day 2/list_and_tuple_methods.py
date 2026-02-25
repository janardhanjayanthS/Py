
# list

my_arr: list[int] = [1, 5, 10]
print(my_arr)
my_arr.append(15)
print(my_arr)
my_arr.remove(1)
print(my_arr)
my_arr.insert(0, True)
print(my_arr)
my_arr.append(5)
print(my_arr)
print('Count of 5: ', my_arr.count(5))
print(my_arr)
my_arr.extend([500, 213, 532])
print(my_arr)
my_arr.reverse()
print(my_arr)
my_arr.sort()
print(my_arr)

# tuple

tuple_example: tuple = (0, 9, 7, 3, 0, 8, 2, 0)
print(tuple_example)
print(tuple_example.count(0))
print(tuple_example.index(3))
