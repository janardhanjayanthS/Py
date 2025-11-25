# import threading
# import time

# def worker():
#     print("Worker thread starting...")
#     time.sleep(5)
#     print("Worker thread done.")

# # Create a thread
# t = threading.Thread(target=worker)

# t.start()  # Start the worker thread

# print("Main thread waiting for worker to finish...")
# t.join()   # Wait for worker thread to complete
# print("Worker finished, main thread continues.")

# import string


# print(string.ascii_letters)



# for x, y in ((x, y) for x in range(3) for y in range(2)):
    # print(x, y)


# g = (n for n in range(3))
# print(g)
# print(next(g))
# print(next(g))
# print(next(g))
# print(next(g))

from collections import OrderedDict


dictionary: OrderedDict[int, str] = OrderedDict({
    1: 'a',
    2: 'b',
    3: 'c'
})


dictionary.pop(2)
print(dictionary)
dictionary.move_to_end(1)
print(dictionary)
dictionary.popitem()
print(dictionary)
