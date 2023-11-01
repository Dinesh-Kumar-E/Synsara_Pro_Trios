import pandas as pd

# Read the CSV file
df = pd.read_csv(r'Dataset\ratings.csv')

# Calculate the average rating for each movie ID
average_ratings = df.groupby('movieId')['rating'].mean().reset_index()

# Write the results to a new CSV file
average_ratings.to_csv(r'Dataset\ratings-processed.csv', index=False)

print("Average ratings calculated and saved to 'average_ratings.csv'")
