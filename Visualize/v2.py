import pandas as pd
import matplotlib.pyplot as plt

# Read the 'dataset.csv' file
data = pd.read_csv(r'Dataset\netflix_filtered.csv', encoding='latin1')

# Count the occurrences of each rating
rating_counts = data['rating'].value_counts()

# Create a bar chart to visualize the count of ratings
plt.figure(figsize=(10, 6))
rating_counts.plot(kind='bar')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.title('Count of Ratings')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability

plt.show()
