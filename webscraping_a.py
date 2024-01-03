import requests

from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
import pprint

url = 'https://www.dice.com/jobs/q-Machine+learning-jobs'
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print('Success')  # Print the content of the response
else:
    print(f'Request failed with status code: {response.status_code}')

soup = BeautifulSoup(response.content, 'html.parser')

rows = soup.select('div.jobs-container')

row = rows[0]
data = row.select_one('h2.job-title a')
title = data.find_all(string=True, recursive=False)[1]
print(title)
location = row.select_one('p.location-display').text.split(", ")[1:]
print(location)
emp_type = row.select_one('p.employment-type').text.split(", ")
print(emp_type)

rows = soup.select('div.jobs-container > dhi-job-search-job-card')

import pprint
import re

def get_title(rows):
  titles = list()
  for row in rows:
    data = row.select_one('h2.job-title a')
    title = data.find_all(string=True, recursive=False)[1]
    titles.append(title)
  return titles

print(get_title(rows))

def get_link(rows):
  links = list()

  for row in rows:
    links.append(row.select_one('h2.job-title a')['href'])

  return links

def get_sp_links(links):
  skills = list()
  salary = list()

  for link in links:
    header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}
    resp = requests.get(link, headers=header)
    sp = BeautifulSoup(resp.content, 'html.parser')

    sk_div = sp.select('div.Skills_chipContainer__mlLa7 span')
    sk_span = list()
    for d in sk_div:
      sk_span.append(d.text.upper())
    skills.append(sk_span)

    sl_div = sp.find('div', {'data-cy' : 'payDetails'})
    if(sl_div is None):
      sl_span = 'Salary Missing'
    else:
      sl_span = sl_div.select_one('span').text
    salary.append(sl_span)

  return [skills, salary]

obj = get_sp_links(get_link(rows))

def get_skill(skills):
  skills_dict = {'Python' : 0, 'Java': 0, 'SQL': 0, 'AI': 0, 'ML': 0, 'LLM': 0, 'Coding': 0, 'Cloud Computing': 0, 'Big Data': 0, 'NLP': 0, 'Deep Learning': 0, 'Generative AI': 0, 'Shell Scripting': 0, 'Pytorch': 0, 'Tensorflow': 0, 'Scikit-learn': 0}
  for skill in skills:
    st = str(skill)
    if('PYTHON' in st):
      skills_dict['Python'] += 1
    if('JAVA' in st):
      skills_dict['Java'] += 1
    if('SQL' in st):
      skills_dict['SQL'] += 1
    if('AI' in st or 'ARTIFICIAL INTELLIGENCE' in st or 'ARTIFICIALINTELLIGENCE' in st):
      skills_dict['AI'] += 1
    if('ML' in st or 'MACHINE LEARNING' in st or 'MACHINELEARNING' in st):
      skills_dict['ML'] += 1
    if('LLM' in st or 'LARGE LANGUAGE MODEL' in st or 'LARGELANGUAGEMODEL' in st):
      skills_dict['LLM'] += 1
    if('CODING' in st or 'PROGRAMMING' in st):
      skills_dict['Coding'] += 1
    if('CLOUD' in st or 'CLOUD COMPUTING' in st or 'CLOUDCOMPUTING' in st or 'AZURE' in st or 'AWS' in st or 'GOOGLE CLOUD' in st or 'GOOGLECLOUD' in st or 'GCP' in st):
      skills_dict['Cloud Computing'] += 1
    if('BIG DATA' in st or 'BIGDATA' in st):
      skills_dict['Big Data'] += 1
    if('NLP' in st or 'NATURAL LANGUAGE PROCESSING' in st or 'NATURALLANGUAGEPROCESSING' in st):
      skills_dict['NLP'] += 1
    if('DEEP LEARNING' in st or 'DL' in st or 'DEEPLEARNING' in st):
      skills_dict['Deep Learning'] += 1
    if('GENRATIVE AI' in st or 'GENRATIVEAI' in st or 'GENAI' in st or 'GEN AI' in st):
      skills_dict['Generative AI'] += 1
    if('SHELL' in st or 'SCRIPTING' in st or 'SHELL SCRIPTING' in st or 'SHELLSCRIPTING' in st):
      skills_dict['Shell Scripting'] += 1
    if('PYTORCH' in st):
      skills_dict['Pytorch'] += 1
    if('TENSORFLOW' in st):
      skills_dict['Tensorflow'] += 1
    if('SCIKIT' in st or 'SCRIPTING' in st or 'SHELL SCRIPTING' in st or 'SHELLSCRIPTING' in st):
      skills_dict['Scikit-learn'] += 1

  return skills_dict

print(get_skill(obj[0]))

def get_location(rows):
  locations = list()
  for row in rows:
    location = row.select_one('p.location-display').text.split(", ")[-2:]
    l = ', '.join(location)
    if(l == ''):
      l = 'To be decided'
    locations.append(l)

  dict_loc = dict()
  for loc in locations:
    if(loc in dict_loc):
      dict_loc[loc] += 1
    else:
      dict_loc[loc] = 1

  return dict_loc

print(get_location(rows))

def get_type(rows):
  types = list()
  for row in rows:
    ty = row.select_one('p.employment-type').text.split(', ')
    types.append(ty)
  return types

print(get_type(rows))

def check(n):
  if(n < 50):
    return 'Below $50K'
  elif(n >= 50 and n < 75):
    return '$50K - $75K'
  elif(n >= 75 and n < 100):
    return '$75K - $100K'
  elif(n >= 100 and n < 125):
    return '$100K - $125K'
  elif(n >= 125 and n < 150):
    return '$125K - $150K'
  elif(n >= 150 and n < 200):
    return '$150K - $200K'

  return 'Above $200K'


def get_salary(salary):
  range = list()
  salary_dict = {'Below $50K': 0, '$50K - $75K': 0, '$75K - $100K': 0, '$100K - $125K': 0, '$125K - $150K': 0, '$150K - $200K': 0, 'Above $200K': 0, 'Salary Info Missing': 0}
  for sal in salary:
    if not any(i.isdigit() for i in sal):
      salary_dict['Salary Info Missing'] += 1
    else:
      range.append(list(map(int, re.findall('\d+', sal))))

  for r in range:
    if len(r) > 0:
      r.sort()
      val = r[-1]
      if(r[-1] > 2000):
        val = int(str(val)[:-3])
        # print(r[-1], val)
        salary_dict[check(val)] += 1
      else:
        salary_dict[check(r[-1])] += 1

  return salary_dict

pprint.pprint(get_salary(obj[1]))

details = {'Title': [], 'Skills': [], 'Type': [], 'Salary': []}

titles = get_title(rows)
skills, salary = get_sp_links(get_link(rows))
emp_type = get_type(rows)
n = len(titles)

for i in range(n):
  details['Title'].append(titles[i])
  sk = ', '.join(skills[i][:4])
  details['Skills'].append(sk)
  t = ', '.join(emp_type[i])
  details['Type'].append(t)
  details['Salary'].append(salary[i])

df = pd.DataFrame.from_dict(details)

fig, ax = plt.subplots()
ax.axis('off')
ax.axis('tight')
t= ax.table(cellText=df.values, colWidths = [0.9]*len(df.columns),  colLabels=df.columns)
t.auto_set_font_size(False)
t.set_fontsize(8)
fig.tight_layout()
plt.show()

def get_pd(page_till):
  base = 'https://www.dice.com/jobs/q-Machine+learning-jobs'
  headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}

  jobs = pd.DataFrame()
  dict_skills = {'Python' : 0, 'Java': 0, 'SQL': 0, 'AI': 0, 'ML': 0, 'LLM': 0, 'Coding': 0, 'Cloud Computing': 0, 'Big Data': 0, 'NLP': 0, 'Deep Learning': 0, 'Generative AI': 0, 'Shell Scripting': 0, 'Pytorch': 0, 'Tensorflow': 0, 'Scikit-learn': 0}
  dict_location = dict()
  dict_salary = {'Below $50K': 0, '$50K - $75K': 0, '$75K - $100K': 0, '$100K - $125K': 0, '$125K - $150K': 0, '$150K - $200K': 0, 'Above $200K': 0, 'Salary Info Missing': 0}
  for i in range(1, page_till+1):
    url = base + '?page=' + str(i)
    # print(url)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    rows = soup.select('div.jobs-container > dhi-job-search-job-card')

    obj = get_sp_links(get_link(rows))
    sk = get_skill(obj[0])
    new_dict = {i: dict_skills.get(i, 0)+sk.get(i, 0)
                    for i in set(dict_skills).union(sk)} # add key values
    dict_skills.update(new_dict) # copy to existing dict

    sl = get_salary(obj[1])
    new_dict = {i: dict_salary.get(i, 0)+sl.get(i, 0)
                    for i in set(dict_salary).union(sl)} # add key values
    dict_salary.update(new_dict) # copy to existing dict


    lc = get_location(rows)
    new_dict = {i: dict_location.get(i, 0)+lc.get(i, 0)
                    for i in set(dict_location).union(lc)} # add key values
    dict_location.update(new_dict) # copy to existing dict

  return [dict_skills, dict_location, dict_salary]

out = get_pd(5)
pprint.pprint(out[0])
pprint.pprint(out[1])
pprint.pprint(out[2])

# bar plot
def plot_bar(dictionary, xl, yl, t):
  keys = dictionary.keys()
  values = dictionary.values()

  plt.bar(keys, values)
  plt.xticks(rotation=90)
  plt.xlabel(xl)
  plt.ylabel(yl)
  plt.title(t)

  plt.show()

out = get_pd(5)
plot_bar(out[0], 'Skills', 'No.of ML roles', 'Key Skills required by ML roles')
plot_bar(out[1], 'Location', 'No.of ML roles', 'Major locations for ML roles')
plot_bar(out[2], 'Salary', 'No.of ML roles', 'Salary range for ML roles')

# pie plot
def plot_pie(dictionary, t):
  labels = dictionary.keys()
  sizes = dictionary.values()

  plt.title(t)
  plt.pie(sizes, labels=labels)

  plt.axis('equal')
  plt.show()

out = get_pd(5)
plot_pie(out[0],'Key Skills required by ML roles')
plot_pie(out[1], 'Major locations for ML roles')
plot_pie(out[2], 'Salary range for ML roles')

def get_sal_skill(links):
  skills = list()
  salary = list()
  skills_list = ['Python', 'Java', 'SQL', 'AI', 'ML', 'LLM', 'Coding', 'Cloud Computing', 'Big Data', 'NLP', 'Deep Learning', 'Generative AI', 'Shell Scripting', 'Pytorch', 'Tensorflow', 'Scikit-learn']


  for link in links:
    header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}
    resp = requests.get(link, headers=header)
    sp = BeautifulSoup(resp.content, 'html.parser')

    sk_div = sp.select('div.Skills_chipContainer__mlLa7 span')
    sk_span = list()
    for d in sk_div:
      sk_span.append(d.text.upper())
    skills.append(sk_span)

    sl_div = sp.find('div', {'data-cy' : 'payDetails'})
    if(sl_div is None):
      sl_span = 'Salary Missing'
    else:
      sl_span = sl_div.select_one('span').text
    salary.append(sl_span)

  return [skills, salary]

# multivariate plot

import seaborn as sns

out = get_pd(5)

len_loc, len_sal, len_sk = len(out[1]), len(out[2]), len(out[0])
loc, sal, sk = list(out[1].values()), list(out[2].values()), list(out[0].keys())
mx = max(len_loc, len_sal, len_sk)
for _ in range(mx - len_loc):
  loc.append(0)

for _ in range(mx - len_sal):
  sal.append(0)

for _ in range(mx - len_sk):
  sk.append(0)

dataset = {'Salary': sal, 'Location': loc, 'Skills': sk}

df = pd.DataFrame.from_dict(dataset)

sns.relplot(x='Salary', y='Location', hue='Skills', data = dataset)
