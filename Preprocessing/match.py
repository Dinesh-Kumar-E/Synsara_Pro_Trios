import pandas as pd

# Read the 'movie.csv' and 'rating.csv' files
movies = pd.read_csv(r'Dataset\movies.csv')
ratings = pd.read_csv(r'Dataset\ratings-processed.csv')

# Perform a left join on 'movieId' to combine the data, fill NaN ratings with 0
matched = movies.merge(ratings, on='movieId', how='left').fillna({'rating': 0})

# Save the result to a new CSV file 'matched.csv'
matched.to_csv(r'Dataset\matched.csv', index=False)

print("Merged data saved to 'matched.csv'")
