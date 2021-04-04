import requests
from bs4 import BeautifulSoup
import csv
import time
from phantomjs import Phantom
# start of the timer
start_time = time.time()
# get the url of the main pages that is going to be parsed
URL = 'https://www.ubisoft.com/en-gb/game/rainbow-six/siege/game-info/operators?isSso=true&refreshStatus=noLoginData' \
      '&fbclid=IwAR0hE7Rjar0iT52mQtp9FaYL5ezVY3I_Th_KnCpH2ExvLlOE0eHKP6s-kTo '
# add host name as to use it for creating urlLinks for operators
HOST = 'https://www.ubisoft.com'
# headers that is used to look like real people for the server
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6)AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/71.0.3578.98 Safari/537.36'}
# path of the file were to save the csv file
FILE = 'pers.csv'


# create a main function
def parce():

    # list that will store the operators
    pers = []
    html = get_html(URL)
    # check the status of the url
    if html.status_code == 200:
        # add the return of the function get_content to the list called pers
        pers.extend(get_content(html.text))
        # write all the data into a csv file(call the function that does it for us
        # create_file(pers, FILE)

        sort_list(pers)
    else:
        print('error')
    print(len(pers))
    # display the time of execution of all code
    print("--- %s seconds ---" % round(time.time() - start_time, 2))


# function that returns a html file
def get_html(url):

    r = requests.get(url, allow_redirects=True, headers=headers)
    return r


# function that returns result of the parsed html
def get_soup(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup


# function that get the needed content of all the operators from given html
def get_content(html):
    soup = get_soup(html)
    items = soup.find_all('a', class_='oplist__card')
    pers = []
    for item in items:
        # ПОПЫТКА ПОЛУЧИТЬ ИНФОРМАЦИЮ ПРО ОПЕРАТИВНИКОВ С ИХ ЛИЧНОЙ СТРАНИЦЫ ( НЕ РАБОТАЕТ)

        # linkPers = HOST + item.get('href')
        # links = get_html(linkPers)
        # soup = get_soup(links.text)
        # data = soups.find_all('div', class_="operator__biography__info")
        # number = 0
        # for i in data:
        # if number == 0:
        #     realNames = item.find('div', class_="operator__biography__info__value").get_text()
        # elif number ==1:
        #     dateOfBirths = item.find('div', class_="operator__biography__info__value").get_text()
        # else:
        #     placeOfbirths = item.find('div', class_="operator__biography__info__value").get_text()
        # number+=1
        # print(links.text)
        # print(soup)
        # print(links)

        # add all the info about operators from their card info
        pers.append({
            'name': item.find('img', class_='oplist__card__icon').find_next('span').get_text(),
            'logoUri': item.find('img', class_="oplist__card__icon").get('src'),
            'cardLogoUri': item.find('img', class_='oplist__card__img').get('src'),
            'personalPageUri': HOST + item.get('href'),
            # 'realName': realNames,
            # 'dateOfBirth': dateOfBirths,
            # 'placeOfBirth': placeOfbirths,
        })
    return pers


def sort_list(list):
    # set the order for sorting, by default it is set as asc(change to 'desc' for desc order)
    order = 'asc'
    sort_by_name(list, order)


def sort_by_name(list, order):
    if order == 'asc':
        print(sorted(list, key=lambda i: i['name']))
    elif order == 'desc':
        print(sorted(list, key=lambda i: i['name'], reverse=True))


# create csv file using the list of operators
def create_file(items, path):
    with open(path, "w", newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['name', 'logoUri', 'cardLogoUri', 'personalPageUri'])
        for item in items:
            writer.writerow([item['name'], item['logoUri'], item['cardLogoUri'], item['personalPageUri']])






phantom = Phantom()

conf = {
    'url': 'http://example.com/',   # Mandatory field
}
output = phantom.download_page(conf, js_path='/Users/mac/.pyenv/versions/3.9.2/lib/python3.9/phantomjs')
parce()
