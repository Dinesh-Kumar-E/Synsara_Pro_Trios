from imdb_lib.session import httpIMDB

imdb = httpIMDB()

print(httpIMDB.searchTitle(imdb,title='interstellar'))