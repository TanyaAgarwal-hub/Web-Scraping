import requests 
from bs4 import BeautifulSoup

url = 'https://www.themoviedb.org/movie'

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}
response = requests.get(url, headers=headers)
if response.status_code == 200:
    print('Success!')  # Print the content of the response
else:
    print(f'Request failed with status code: {response.status_code}')
print(response) 
print(response.content[:200]) 

soup = BeautifulSoup(response.content, 'html.parser') 
title = soup('title')[0]
print(title.text) 

def get_content_from_url(url): 
  headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}
  response = requests.get(url, headers=headers)

  if response.status_code == 200:
      soup = BeautifulSoup(response.content, 'html.parser')
      return soup
  else:
      print(f'Request failed with status code: {response.status_code}')

soup = get_content_from_url('https://www.themoviedb.org/movie') 

rows = soup.select('div#page_1 .card')

row = rows[0]

print(row) 

name = row.select_one('h2 a').text.strip()
div = row.select_one('div.user_score_chart')
rating = div['data-percent']

print(name) 
print(rating) 

movie_url_div = row.select_one('div.wrapper a')
movie_url = movie_url_div['href']

print(movie_url)

soup = get_content_from_url('https://www.themoviedb.org/movie')

def get_title(soup):
  rows = soup.select('.page_wrapper > div.card')

  titles = list()

  for row in rows:
    row_data = row.select_one('div.wrapper a')
    if(row_data is None):
      break
    title = row_data['title']

    titles.append(title)

  return titles

print(get_title(soup)) 

def get_ratings(soup):
  rows = soup.select('.page_wrapper > div.card')

  ratings = list()

  for row in rows:
    row_data = row.select_one('div.user_score_chart')
    if(row_data is None):
      break

    rating = row_data['data-percent']
    if(rating == '0.0'):
      rating = 'Not rated'

    ratings.append(rating)


  return ratings

print(get_ratings(soup)) 

def get_html(soup):
  rows = soup.select('.page_wrapper > div.card')

  htmls = list()

  for row in rows:
    row_data = row.select_one('div.wrapper a')
    if(row_data is None):
      break

    html = row_data['href']

    htmls.append(html)

  return htmls

print(get_html(soup)) 

htmls = get_html(soup)

def get_genre(htmls):
  genres = list()
  for h in htmls:
    base_url = 'https://www.themoviedb.org'+ h
    sp = get_content_from_url(base_url)
    rows = sp.select('span.genres')[0]

    gen = list()
    data = rows.find_all('a')
    for d in data:
      gen.append(d.text)

    genres.append(', '.join(gen))

  return genres


print(get_genre(htmls)) 


def get_cast(htmls):
  casts = list()
  for h in htmls:
    base_url = 'https://www.themoviedb.org'+ h
    sp = get_content_from_url(base_url)
    rows = sp.select('div#cast_scroller > ol')[0]

    cast = list()
    data = rows.find_all('li')
    for d in data:
      c = d.select_one('p a')
      if(c.text != 'View More '):
        cast.append(c.text)

    casts.append(', '.join(cast))


  return casts


print(get_cast(htmls)) 

import pandas as pd

soup = get_content_from_url('https://www.themoviedb.org/movie')

def get_pd(soup):
  details = dict()
  details['Title'] = get_title(soup)
  details['Rating'] = get_ratings(soup)
  htmls = get_html(soup)
  details['Genre'] = get_genre(htmls)
  details['Cast'] = get_cast(htmls)
  return pd.DataFrame(details)

print(get_pd(soup)) 

import csv

def get_page_pd(page_till):

  for p in range(1, page_till+1):
    url = 'https://www.themoviedb.org/movie' + '?page=' + str(p)
    soup = get_content_from_url(url)
    pd_obj = get_pd(soup)
    pd_obj.to_csv('movies'+str(p)+'.csv', index=False)

get_page_pd(5) 

details = pd.DataFrame()

csv_files = ['movies1.csv', 'movies2.csv', 'movies3.csv', 'movies4.csv', 'movies5.csv']
for file in csv_files:
            df_temp = pd.read_csv(file)
            details = pd.concat([details, df_temp], ignore_index=True)

print(details)
details.to_csv('movies.csv', index=False) 
