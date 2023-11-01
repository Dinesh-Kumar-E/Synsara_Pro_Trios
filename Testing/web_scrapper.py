'''
import movieposters as mp
link = mp.get_poster(title='don tamil movie')

print(link)
'''

'''
from google_images_download import google_images_download
#instantiate the class
response = google_images_download.googleimagesdownload()
arguments = {"keywords":"don movie tamil","limit":10,"print_urls":True}
paths = response.download(arguments)
#print complete paths to the downloaded images
print(paths)
'''

from bing_image_downloader import downloader
query_string = 'don movie tamil'
downloader.download(query_string, limit=1,  output_dir='downloads', adult_filter_off=True, force_replace=False, timeout=60, verbose=True)
