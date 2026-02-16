from pypdf import PdfReader
import sys
import random

reader = PdfReader("July-2025-DSMA-Restaurant-Guide-links5.pdf")
#reader = PdfReader("Cropped-Finalized-July-2025-DSMA-Restaurant-Guide-links5 - Copy.pdf")  # Some of the restaurant cuisines are clipped out
#print(len(reader.pages))

restaurants = {}  # dictionary of restaurants mapped by restaurant cuisine

# parse and extract pdf text
page = reader.pages[1]
raw_data = list(page.extract_text())
parsed_data = []

cur_string = ""
for c in raw_data:
    if c == '\n':
        parsed_data.append(cur_string.rstrip().lstrip())
        cur_string = ""
    else:
        cur_string = cur_string + c

#for item in parsed_data:
#    if item == "":
#        parsed_data.remove(item)

parsed_data.append(cur_string)
parsed_data = [s for s in parsed_data if '.' not in s[:6]]
#print(parsed_data)

uppercase = [item for item in parsed_data if item.isupper() 
        and len(item.split()) <= 3
        and not any(word in item for word in ["TEA", "PIZZERIA", "SUSHI", "BBQ"])]
#print(uppercase)

restaurant_list = []
i, j = 0, 0
while i < len(parsed_data):
    cur_category = uppercase[j]
    if parsed_data[i] != cur_category:
        restaurant_list.append(parsed_data[i])
    else:
        restaurants[cur_category] = restaurant_list
        restaurant_list = []
        j += 1

    i += 1

#print(restaurants.keys())
#for key in restaurants.keys():
#    print(key, restaurants[key])

n = len(restaurants.keys())
num = random.randint(0, n)
categories = list(restaurants.keys())
print(categories[num])

num2 = random.randint(0, len(restaurants[categories[num]])-1)
print(restaurants[categories[num]][num2])