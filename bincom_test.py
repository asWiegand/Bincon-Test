import psycopg2
from collections import Counter
import random
import statistics
import requests
from bs4 import BeautifulSoup


db_name = ... # Put the name of database
db_user = ... # Put the user of database
db_pass = ... # Put the password of database
db_host = ... # Put the host url of database

#Here i get the colors of the table
url = ... # Put the link of site here, in my case, i used localhost
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

data = {}
rows = soup.find_all("tr")[1:]

for row in rows:
    cols = row.find_all("td")
    if len(cols) == 2:
        day = cols[0].text.strip()
        colors = cols[1].text.strip().replace(" ", "").split(",")
        data[day] = colors

colors = []
for day in data.values():
    colors.extend(day)

color_counts = Counter(colors)

# 1. Mean color
mean_color = max(color_counts, key=lambda x: color_counts[x])
print("Mean color:", mean_color)

# 2. Most worn color
most_worn = color_counts.most_common(1)[0][0]
print("Most worn color:", most_worn)

# 3. Median color
sorted_colors = sorted(color_counts.items(), key=lambda x: x[1])
median_color = sorted_colors[len(sorted_colors) // 2][0]
print("Median color:", median_color)

# 4. Variance of colors
color_freqs = list(color_counts.values())
variance = statistics.variance(color_freqs)
print("Variance of colors:", variance)

# 5. Probability of picking red
prob_red = color_counts.get("RED", 0) / sum(color_counts.values())
print("Probability of picking red:", prob_red)

# 6. Save to PostgreSQL
def save_to_db():
    try:
        conn = psycopg2.connect(dbname = db_name user= db_user password=db_pass host= db_host)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS color_frequency (color TEXT, frequency INT)")
        for color, freq in color_counts.items():
            cursor.execute("INSERT INTO color_frequency (color, frequency) VALUES (%s, %s)", (color, freq))
        conn.commit()
        cursor.close()
        conn.close()
        print("Data saved to database.")
    except Exception as e:
        print("Database error:", e)

# uncomment the following line to save to the database
# save_to_db()

# 7. Recursive search algorithm
def recursive_search(arr, target, low, high):
    if low > high:
        return -1
    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] > target:
        return recursive_search(arr, target, low, mid - 1)
    else:
        return recursive_search(arr, target, mid + 1, high)

# 8. Generate 4-digit binary and convert to decimal
binary_num = "".join(str(random.randint(0, 1)) for _ in range(4))
decimal_value = int(binary_num, 2)
print(f"Generated binary: {binary_num}, Decimal: {decimal_value}")

# 9. Sum first 50 Fibonacci numbers
def fibonacci(n):
    a, b = 0, 1
    total = 0
    for _ in range(n):
        total += a
        a, b = b, a + b
    return total

sum_fib = fibonacci(50)
print("Sum of first 50 Fibonacci numbers:", sum_fib)
