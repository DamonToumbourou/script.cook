from bs4 import BeautifulSoup as bs
import urllib2
import requests 
import re

def get_soup(url):
    html = urllib2.urlopen(url).read()
    html = html.replace("</scr' + 'ipt>","")
    soup = bs(html, 'html.parser')

    return soup

def get_search(page_num, keyword):
    keyword = keyword.replace(' ', '+')
    SEARCH_URL = 'http://www.taste.com.au/search-recipes/?q=' + keyword + '&page=' + str(page_num) 
    
    soup = get_soup(SEARCH_URL)
   
    content = soup.find('div', {'class': 'content-item tab-content current'})
    content = content.find_all('div', {'class': 'story-block '})
    
    output = []
    for i in content:
        path = i.find('a').get('href')
        
        label = i.get_text().strip()
        try:
            thumb = i.find('img')['src']
            thumb =  thumb.replace('_s', '_l')
            thumb = thumb.replace('_m', '_l')

        except AttributeError:
            continue
    
        item = {
            'label': label,
            'path': path,
            'thumbnail': thumb,
        }

        output.append(item)
    print output
    return output
#get_search(1,'mint')

def get_recipe(url):
    ing = ''
    diff = ''
    star = ''
    source = ''

    soup = get_soup(url)

    title = soup.find('div', {'class': 'heading'})
    title = title.get_text().strip() 
    
    sub_title = soup.find('p', {'class': 'quote-left'})
    sub_title = sub_title.get_text()
    
    try: 
        prep_time = soup.find('td', {'class': 'prepTime'})
        prep_time = prep_time.find('em').get_text()
    except AttributeError:
        pass

    try:
        cook_time = soup.find('td', {'class': 'cookTime'})
        cook_time = cook_time.find('em').get_text()
    except AttributeError:
        pass
    
    try:
        ing = soup.find('td', {'class': 'ingredientCount'})
        ing = ing.find('em').get_text()
    except AttributeError:
        pass
    
    try:
        diff = soup.find('td', {'class': 'difficultyTitle'})
        diff = diff.find('em').get_text()
    except AttributeError:
        pass

    try:
        star = soup.find('span', {'class': 'star-level'})
        star = star.get_text()
    except AttributeError:
        pass

    try:
        source = soup.find('div', {'class': 'source-logo'})
        source = source.get_text().strip()
    except AttributeError:
        pass
    
    try:
        serv = soup.find('td', {'class': 'servings'})
        serv = serv.find('em').get_text()
    except AttributeError:
        pass

    if not serv:
        serv = soup.find('td', {'class': 'makes'})
        serv = serv.find('em').get_text()
    
    try:
        img = soup.find('img', {'itemprop': 'photo'})
        img = img.get('src')
    except AttributeError:
        img = ''        

    output = []
    items = {
            'title': title,
            'sub_title': sub_title,
            'prep_time': prep_time,
            'cook_time': cook_time,
            'ing': ing,
            'diff': diff,
            'serv': serv,
            'img': img,
            'star': star,
            'source': source,
    }

    output.append(items)
    
    return output
#get_recipe('http://www.taste.com.au/recipes/29331/hazelnut+milk+chocolates')

def get_recipe_method(url):
    soup = get_soup(url)

    step = soup.find_all('p', {'class': 'description'})

    output = []
    for i in step:
        step = i.get_text()
        items = {
            'step': step,
        }

        output.append(items)

    return output
#get_recipe_method('http://www.taste.com.au/recipes/19197/warm+milk+with+a+twist')

def get_recipe_ingred(url):
    soup = get_soup(url)

    content = soup.find_all('ul', {'class': 'ingredient-table'})
    ing_list = [] 
    for i in content:
        con = i.find_all('li') 
        for k in con:
            ing = k.get_text().strip()
            item = {
                'ing': ing,
            }
            ing_list.append(item)

    return ing_list
#get_recipe_ingred('http://www.taste.com.au/recipes/3213/chocolate+mint+cakes+with+choc+mint+frosting')

def get_high_rated(url):
    soup = get_soup(url)
    content = soup.find_all('div', {'class': 'module recommend-row'})
    
    output = []
    
    for i in content:
        highest = i.find('h4').get_text()
        
        if "Highly rated" in highest:
            labels = i.find_all('li')
           
            for k in labels:
                label = k.get_text()

                path = k.find('a')['href']

                item = {
                        'path': path,
                        'label': label
                }
                output.append(item)
    
    item = {
            'label': 'damon',
            'path': 'frank',
    }
    print output
    return output

get_high_rated('http://www.taste.com.au/')
