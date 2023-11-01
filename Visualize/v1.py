import pandas as pd
import matplotlib.pyplot as plt

# Read the 'matched.csv' file
data = pd.read_csv(r'Dataset\matched.csv')

# Split the 'category' column to identify unique genres
unique_genres = set()
for genres in data['genres']:
    unique_genres.update(genres.split('|'))

# Calculate the number of movies in each category
genre_counts = {genre: sum(data['genres'].str.contains(genre)) for genre in unique_genres}

# Create a bar chart to visualize the number of movies in each category
plt.figure(figsize=(12, 6))
plt.barh(list(genre_counts.keys()), genre_counts.values())
plt.xlabel('Number of Movies')
plt.ylabel('Genre')
plt.title('Number of Movies in Each Genre')
plt.gca().invert_yaxis()  # Invert the y-axis for better visualization

plt.show()
