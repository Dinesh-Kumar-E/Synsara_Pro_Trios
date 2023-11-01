import tkinter as tk
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# Read the CSV file
df = pd.read_csv('Dataset\matched.csv')

# Create a TF-IDF vectorizer
tfidf = TfidfVectorizer(stop_words='english')
df['genres'] = df['genres'].fillna('')
tfidf_matrix = tfidf.fit_transform(df['genres'])

# Compute the cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Function to get movie recommendations
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = df[df['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Top 10 recommendations (excluding itself)
    movie_indices = [i[0] for i in sim_scores]
    return df['title'].iloc[movie_indices]

# Create the GUI
def recommend_movies():
    input_title = entry.get()
    recommendations = get_recommendations(input_title)
    result_label.config(text="Recommended Movies:\n" + "\n".join(recommendations))

app = tk.Tk()
app.title("Movie Recommendation System")

label = tk.Label(app, text="Enter a movie title:")
label.pack()

entry = tk.Entry(app)
entry.pack()

button = tk.Button(app, text="Get Recommendations", command=recommend_movies)
button.pack()

result_label = tk.Label(app, text="")
result_label.pack()

app.mainloop()
