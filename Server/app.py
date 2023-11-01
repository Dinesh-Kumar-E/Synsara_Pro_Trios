import streamlit as st
from PIL import Image
import json
from Classifier import KNearestNeighbours
from bs4 import BeautifulSoup
import requests, io
import PIL.Image
from urllib.request import urlopen
import movieposters as mp
from PyMovieDb import IMDB
import json
imdb = IMDB()

with open(r'Server\Data\movie_data.json', 'r+', encoding='utf-8') as f:
    data = json.load(f)
with open(r'Server\Data\movie_titles.json', 'r+', encoding='utf-8') as f:
    movie_titles = json.load(f)
hdr = {'User-Agent': 'Mozilla/5.0'}

def write_to_file(data):
    with open(r'Server\logs\movie_data.txt','a') as f:
        f.write(data+'\n')

def parse_link(imdb_link):
    id_start = imdb_link.find('title/')+6
    id_end = imdb_link.find('/?')
    return imdb_link[id_start:id_end]

def movie_poster_fetcher(imdb_link):
    write_to_file(imdb_link)
    ## Display Movie Poster
    #http://www.imdb.com/title/tt0437745/?ref_=fn_tt_tt_1
    
    link = mp.get_poster(id=parse_link(imdb_link))
    u = urlopen(link)
    raw_data = u.read()
    image = PIL.Image.open(io.BytesIO(raw_data))
    image = image.resize((158, 301), )
    st.image(image, use_column_width=False)

def parse(list):
    names = []
    for i in list:
        names.append(i['name'])
    return str(names).replace('[', '').replace(']', '').replace("'", '')

def get_movie_info(imdb_link):
    movie_id = parse_link(imdb_link)
    res = imdb.get_by_id(movie_id)
    #write_to_file(str(res))
    movie_director = ""
    movie_cast = ""
    movie_story = ""
    movie_rating = ""
    
    movie_data = json.loads(res)
    try:
        movie_director = movie_data['director'][0]['name']
        movie_cast = str([actor['name'] for actor in movie_data['actor']]).replace('[', '').replace(']', '').replace("'", '')
        movie_story = movie_data['review']['reviewBody']
        movie_rating = movie_data['rating']['ratingValue']
    except:
        pass
    # write_to_file(str(movie_director) + movie_cast + str(movie_story) + str(movie_rating))
    return movie_director, movie_cast, movie_story, ""


def KNN_Movie_Recommender(test_point, k):
    # Create dummy target variable for the KNN Classifier
    target = [0 for item in movie_titles]
    # Instantiate object for the Classifier
    model = KNearestNeighbours(data, target, test_point, k=k)
    # Run the algorithm
    model.fit()
    # Print list of 10 recommendations < Change value of k for a different number >
    table = []
    for i in model.indices:
        # Returns back movie title and imdb link
        table.append([movie_titles[i][0], movie_titles[i][2], data[i][-1]])
    print(table)
    return table


st.set_page_config(
    page_title="Movie Recommender System",
)


def run():
    img1 = Image.open('Server\meta\logo.jpg')
    img1 = img1.resize((700, 250), )
    st.image(img1, use_column_width=False)
    st.title("Movie Recommender System")
    st.markdown('''<h4 style='text-align: left; color: #d73b5c;'> Data is based IMDB Movie Dataset</h4>''',
                unsafe_allow_html=True)
    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News',
              'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']
    movies = [title[0] for title in movie_titles]
    category = ['--Select--', 'Movie based', 'Genre based']
    cat_op = st.selectbox('Select Recommendation Type', category)
    if cat_op == category[0]:
        st.warning('Please select Recommendation Type!!')
    elif cat_op == category[1]:
        select_movie = st.selectbox('Select movie: (Recommendation will be based on this selection)',
                                    ['--Select--'] + movies)
        dec = st.radio("Want to Fetch Movie Poster?", ('Yes', 'No'))
        st.markdown(
            '''<h4 style='text-align: left; color: #cc7533;'>Fetching a Movie Posters will take a time</h4>''',
            unsafe_allow_html=True)
        if dec == 'No':
            if select_movie == '--Select--':
                st.warning('Please select Movie!!')
            else:
                no_of_reco = st.slider('Number of movies you want Recommended:', min_value=5, max_value=20, step=1)
                genres = data[movies.index(select_movie)]
                test_points = genres
                table = KNN_Movie_Recommender(test_points, no_of_reco + 1)
                table.pop(0)
                c = 0
                st.success('Some of the movies from our Recommendation, have a look below')
                for movie, link, ratings in table:
                    c += 1
                    director, cast, story, total_rat = get_movie_info(link)
                    st.markdown(f"({c})[ {movie}]({link})")
                    st.markdown(director)
                    st.markdown(cast)
                    st.markdown(story)
                    st.markdown(total_rat)
                    st.markdown('IMDB Rating: ' + str(ratings) + '⭐')
        else:
            if select_movie == '--Select--':
                st.warning('Please select Movie!!')
            else:
                no_of_reco = st.slider('Number of movies you want Recommended:', min_value=5, max_value=20, step=1)
                genres = data[movies.index(select_movie)]
                test_points = genres
                table = KNN_Movie_Recommender(test_points, no_of_reco + 1)
                table.pop(0)
                c = 0
                st.success('Some of the movies from our Recommendation, have a look below')
                for movie, link, ratings in table:
                    c += 1
                    st.markdown(f"({c})[ {movie}]({link})")
                    movie_poster_fetcher(link)
                    director, cast, story, total_rat = get_movie_info(link)
                    st.markdown(director)
                    st.markdown(cast)
                    st.markdown(story)
                    st.markdown(total_rat)
                    st.markdown('IMDB Rating: ' + str(ratings) + '⭐')
    elif cat_op == category[2]:
        sel_gen = st.multiselect('Select Genres:', genres)
        dec = st.radio("Want to Fetch Movie Poster?", ('Yes', 'No'))
        st.markdown(
            '''<h4 style='text-align: left; color: #d73b5c;'>* Fetching a Movie Posters will take a time."</h4>''',
            unsafe_allow_html=True)
        if dec == 'No':
            if sel_gen:
                imdb_score = st.slider('Choose IMDb score:', 1, 10, 8)
                no_of_reco = st.number_input('Number of movies:', min_value=5, max_value=20, step=1)
                test_point = [1 if genre in sel_gen else 0 for genre in genres]
                test_point.append(imdb_score)
                table = KNN_Movie_Recommender(test_point, no_of_reco)
                c = 0
                st.success('Some of the movies from our Recommendation, have a look below')
                for movie, link, ratings in table:
                    c += 1
                    st.markdown(f"({c})[ {movie}]({link})")
                    director, cast, story, total_rat = get_movie_info(link)
                    st.markdown(director)
                    st.markdown(cast)
                    st.markdown(story)
                    st.markdown(total_rat)
                    st.markdown('IMDB Rating: ' + str(ratings) + '⭐')
        else:
            if sel_gen:
                imdb_score = st.slider('Choose IMDb score:', 1, 10, 8)
                no_of_reco = st.number_input('Number of movies:', min_value=5, max_value=20, step=1)
                test_point = [1 if genre in sel_gen else 0 for genre in genres]
                test_point.append(imdb_score)
                table = KNN_Movie_Recommender(test_point, no_of_reco)
                c = 0
                st.success('Some of the movies from our Recommendation, have a look below')
                for movie, link, ratings in table:
                    c += 1
                    st.markdown(f"({c})[ {movie}]({link})")
                    movie_poster_fetcher(link)
                    director, cast, story, total_rat = get_movie_info(link)
                    st.markdown(director)
                    st.markdown(cast)
                    st.markdown(story)
                    st.markdown(total_rat)
                    st.markdown('IMDB Rating: ' + str(ratings) + '⭐')


run()
