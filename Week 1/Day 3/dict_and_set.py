
mobile_info = {
    'Brand': 'Xaomi',
    'Model': '10T pro',
    'Ram': 6,
    'storage': 128
}

mobile_info['color'] = 'blue'
mobile_info['year'] = 2020
mobile_info['3.5mm port'] = False

print(f'The brand and model of mobile: {mobile_info["Brand"]}: {mobile_info["Model"]}')

print(mobile_info.keys())

print(mobile_info.values())


for key, value in mobile_info.items():
    print(key, ': ', value)


print(f'popping last element from dictionary: {mobile_info.popitem()}')
print(f"popping specific element from dictionary using a key: {mobile_info.pop('color')}")




# set

set1 = set()
set1.add(5)
set1.add(15)
set1.add(50)
set1.add(523)
set1.add(55322)

print(f'Set: {set1}')


set1.remove(5)      # throws keyerror if 5 is not present
set1.discard(5)     # does not throw keyerror if element not present in set
print(f'Set 1: {set1}')

set2 = set([2, 5, 10, 50])
print(f'Set 2: {set2}')

print('Union: ', set1.union(set2))
print('Intersection: ', set1.intersection(set2))
print('Difference: ', set1.difference(set2))
