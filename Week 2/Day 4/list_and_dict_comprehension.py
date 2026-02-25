# list comprehension

even_numbers = [n for n in range(1, 11) if n % 2 == 0]
print(even_numbers)

sample_list = [[1, 2], [3, 4]]
combined_list = [j for inner in sample_list for j in inner]
print(combined_list)


# Dictionary comprehension

names = ["Alice", "Bob"]
scores = [85, 92]
names_to_scores = {name: score for name, score in zip(names, scores)}
print(names_to_scores)


num_to_squares = {n: n**2 for n in range(100)}
print(num_to_squares)
