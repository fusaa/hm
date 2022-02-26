import requests
from bs4 import BeautifulSoup
import math
import pandas as pd
import re
import time

# Selenium imports.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# Configs for Selenium:
PATH = ".\chromedriver.exe"  # windows driver Selenium
#PATH='./chromedriver' # Mac driver Selenium
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(PATH, chrome_options = options)
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')

# Detection avoidance because of 'headless mode' :
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
options.add_argument('user-agent={0}'.format(user_agent))

# globals
# requests header:
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

#
# main > showcase_clicker(product_id_from_showcase) > color_clicker_id > colorr_clicker_get > get_moreselenium
#   \|-> get_working_soup \|> main+page_id_extract                              \|>get_colors_id


def main():
    soup = get_working_soup()  # showcase page
    # main_page_extract(soup)
    # prod_page_extract_color_color_id(main_page_ID_extract(soup))

    # TODO -> Create success tracker for showcase by ID

    data = pd.DataFrame()
    data['showcaseID_aux'] = main_page_ID_extract(soup)  # (1)
    # go into 1st item...
    product_id_from_showcase = list(data['showcaseID_aux'])
    return_aux = pd.DataFrame()
    return_aux = pd.concat([return_aux, showcase_clicker(product_id_from_showcase)], ignore_index=True)  # (2)
    return_aux.to_csv('hm_data.csv')


    # aux_colors = prod_page_extract_color_color_id(list(data['showcaseID_aux']))
    #data = aux_colors
    #[0985197001, color_list_id, color_list]
    # print(list(data['showcaseID']))



def get_working_soup():
    # obtain webpage / EXPLORATORY - to get proper page size.
    url = 'https://www2.hm.com/en_us/men/products/jeans.html'
    page = requests.get(url, headers=headers)

    # create soup object 1st time EXPLORATORY
    soup = BeautifulSoup(page.text, 'html.parser')

    # get data for calculation for URL page size
    soup_total_product_items = soup.find(class_="load-more-heading")
    displayed_items = soup_total_product_items['data-items-shown']
    total_items = soup_total_product_items['data-total']

    # Calculation for 'page size' url parameter:
    page_size = int(total_items) / int(displayed_items)
    page_size = math.ceil(page_size) * int(displayed_items)
    # print(page_size)

    # re-get of url with all items 'at once' - no append method by parts.
    url = 'https://www2.hm.com/en_us/men/products/jeans.html?sort=stock&image-size=small&image=model&offset=0&page-size=' + str(page_size)
    page = requests.get(url, headers=headers)

    # Create WORKING soup object:
    soup = BeautifulSoup(page.text, 'html.parser')

    return(soup)

def main_page_ID_extract(soup):
    # product_id, product_category, product_name, product_price
    #'scrapy_datetime'  style id + color id
    soup_product_list = soup.find_all(class_="item-heading")
    product_list = [a.get_text(strip = True) for a in soup_product_list]
    # print(product_list)

    soup_product_id_cat = soup.find_all(class_='hm-product-item')
    product_id_list = [a['data-articlecode'] for a in soup_product_id_cat]
    product_category_list = [a['data-category'] for a in soup_product_id_cat]

    # print(id)

    return(product_id_list)

# def prod_page_extract_color_color_id(product_id_list):
#     # print(product_id_list)
#     # url template: 'https://www2.hm.com/en_us/productpage.0985197001.html'
#     # .<product_id>.html
#     url = 'https://www2.hm.com/en_us/productpage.' + str(product_id_list[0]) + '.html'
#     print(url)
#     page = requests.get(url, headers=headers)
#     soup = BeautifulSoup(page.text, 'html.parser')
#     #
#     # get stars
#
#
#     # get number of reviews -> ver pagina selenium
#     # review_numbers = soup.find_all('div', class_='rating-stars js-stars')
#     #print(review_numbers)
#     # get colors
#     color_soup = soup.find_all('a', class_='filter-option miniature')
#     color_soup.append( soup.find_all('a', class_='filter-option miniature active')[0])
#
#     #color_soup2 = color_soup1.find_all('a')
#     print("colors:")
#     color_list = [a['data-color'] for a in color_soup]
#     print(color_list)  # OK it works Colors.
#     color_list_id = [a['data-articlecode'] for a in color_soup]
#
#     #print(color_soup[3]['data-articlecode'])
#     print(color_list_id)
#
#     aux_return = pd.DataFrame()
#     aux_return['color_id'] = color_list_id
#     aux_return['color'] = color_list
#     aux_return['showcaseID'] = product_id_list[0]
#     get_more_selenium(product_id_list[0])
#     return [aux_return]

def get_more_selenium(product_id, current_showcase_id):
    # Gets browser driver open on designated page
    url = 'https://www2.hm.com/en_us/productpage.' + str(product_id) + '.html'
    driver.get(url)

    # HTML Loading

    body = driver.find_element_by_css_selector('body')

    for a in range(12):
        body.send_keys(Keys.PAGE_DOWN)
    page_source = driver.page_source

    size_click = driver.find_element_by_id('picker-1')  # opens size window to get in code
    size_click.click()
    page_size_click = driver.page_source

    try:
        review = driver.find_element_by_class_name('reviews-number')  # opens review windows
        driver.execute_script("arguments[0].click();", review)
        page_reviews = driver.page_source
        button_close = driver.find_element_by_class_name("icon-close-black")  # closes review window
        driver.execute_script("arguments[0].click();", button_close)
    except:
        print('*** Found review error')



    # time.sleep(2)

    #cookie_ok_button = driver.find_element_by_id('onetrust-accept-btn-handler')  # closes cookies alert window
    #driver.execute_script("arguments[0].click();", cookie_ok_button)

    # time.sleep(2000)
    details_button = driver.find_element_by_class_name('js-open-more-details')  # opens product details window
    driver.execute_script("arguments[0].click();", details_button)
    page_details = driver.page_source

    # Creating BeautifulSoup OBJECTS from pages...
    soup = BeautifulSoup(page_source)
    try:
        soup_review = BeautifulSoup(page_reviews)
    except:
        soup_review = 'NoReview'
    soup_details = BeautifulSoup(page_details)
    soup_sizes_list = BeautifulSoup(page_size_click)

    # Finding and PRE PROCESSING DATA...

    # Review Number
    try:
        review_numbers = soup_review.find('h2', id='js-review-heading')
        print('Review:')
        print(review_numbers.string[9:-1])  # slice to remove text.
        reviews = review_numbers.string[9:-1]
    except:
        reviews = 'NoReviewData'

    # Stars number
    try:
        stars_from_review_page = soup_review.find('div', class_='star-average-number js-stars-number')
        # print('stars_review:')
        # print(stars_from_review_page.text)  # getting correct string.
        stars = stars_from_review_page.text
    except:
        stars = 'NoStarsData'

    # ############################################################## Sizes list
    # sizes_list_raw = soup_sizes_list.find_all('span', class_='value')
    # aux_sizes_list = [a.text for a in sizes_list_raw]
    # # print("Sizes:")
    # # print(aux_sizes_list)
    # sizes_list = []  # RETURNING LIST
    # for a in aux_sizes_list:
    #     if len(re.findall('\d\d/\d\d', a)) > 0:  # does not work because there are sizes as M,L,XL, also single numbers
    #         sizes_list.append(a)

    # print(sizes_list)

    # Color List Codes  // TODO to be removed - already have that...
        # color_list_soup = soup.find_all('a', class_='filter-option miniature')
        # color_list_soup.append(soup.find_all('a', class_='filter-option miniature active')[0])
    # print(color_list_soup)
        # color_list_codes = [a['data-articlecode'] for a in color_list_soup]  # RETURNING ID COLORS FOR MATCHING
    # print(color_list_codes)  # OK it works Colors. list

    # composition / Length / waist rise / Material
    details = soup_details.find('dl', class_='js-pdp-details-information')
    # print(details)
    # print((details.text.split('\n')))
    # print((details.get_text().split('\n')))
    details_data = [list(a.stripped_strings) for a in details]
    # print(details_data)

    # Console check to see if getting data from Details correctly

    composition = []
    length = []
    waist_rise = []
    material = []
    details_color = []
    fit = []

    for a in details_data:
        if a[0] == 'Composition':
            print("Found Composition")
            for b in a:
                # print(b)
                composition.append(b)
        if a[0] == 'Length':
            for b in a:
                # print(b)
                length.append(b)
        if a[0] == 'Waist Rise':
            for b in a:
                # print(b)
                waist_rise.append(b)
        if a[0] == 'Material':
            for b in a:
                # print(b)
                material.append(b)
        if a[0] == 'Description':
            for b in a:
                print(b)
                details_color.append(b)
        if a[0] == 'Fit':
            for b in a:
                print(b)
                fit.append(b)

    # *** Price Item...
    soup_price_regular = soup.find('div', class_='price')
    price_item_list = (list(soup_price_regular.stripped_strings))
    price_item = ''
    price_item_desc = ''

    if len(price_item_list) == 1:
        price_item_desc = str(price_item_list[0])
        price_item = str(price_item_list[0])
        print("price_item: " + price_item)
    if len(price_item_list) == 2:
        price_item_desc = str(price_item_list[0])
        price_item = str(price_item_list[1])
        print("price_desc: " + price_item_desc)
        print("price_item: " + price_item)

    # Description text:
    # pdp-description-text
    description = soup.find('p', class_='pdp-description-text')
    print(description.text)

    # color-description
    color_description = soup.find('div', class_='product-colors').find('h3').text
    # print(color_description.text)

    # product-title
    product_title = soup.find('div', class_='inner').find('h1')
    product_title = list(product_title.stripped_strings)[0]

    #   -- sizes WITH AVAILABILITY --
    sizes_w_availability = soup_sizes_list.find_all('ul', class_='picker-list')
    print('sizes w a')
    # print(sizes_w_availability[0].text)
    # print(sizes_w_availability[0].text.split('\n'))
    print('this is line R3: ' + str(list(sizes_w_availability[0].stripped_strings)))

    aux_w = [list(a.stripped_strings) for a in sizes_w_availability]
    print('this is aux_w' + str(aux_w))
    aux_size_number = []
    aux_size_avail = []
    len_ = []
    for a in range(len(aux_w[0])):
        condition_slash = re.search('\d\d/\d\d', aux_w[0][a])
        condition_simple = re.search('^[a-zA-Z]{1,4}$', aux_w[0][a])
        condition_2_digits = re.search('\d\d', aux_w[0][a])
        # print('a:' + str(a))
        if condition_slash or condition_simple or condition_2_digits:
            aux_size_number.append(aux_w[0][a])
            aux_size_avail.append('In Stock')
        if a <= len(aux_w[0]):
            if aux_w[0][a] == 'Notify me':
                aux_size_avail[len(aux_size_avail) - 1] = 'Out of Stock'
            if aux_w[0][a] == 'Few pieces left':
                aux_size_avail[len(aux_size_avail) - 1] = 'Few pieces'
        len_.append(a)
    print(len_)

    print(aux_size_number)
    print(aux_size_avail)
    print('s size' + str(len(aux_size_number)))
    print('s avai' + str(len(aux_size_avail)))
    ## SIZES WITH AVAILABILITY END ##


    ## TODO Generate unique list value for sizes without any filtes - separate Dataframe - .unique purposes.
    ## create df with global - so it can be accessed across functions without being passed.



    # Prepare returning dataframe
    aux_return = pd.DataFrame()
    aux_return['sizes'] = aux_size_number
    aux_return['availability'] = aux_size_avail
    aux_return['product_title'] = product_title
    aux_return['color_id'] = product_id
    aux_return['color'] = str(color_description)
    aux_return['details_color'] = str(details_color[1:])
    aux_return['stars'] = stars
    aux_return['reviews'] = reviews
    aux_return['fit'] = str(fit[1:])
    aux_return['composition'] = str(composition[1:])
    aux_return['length'] = str(length[1:])
    aux_return['waist_rise'] = str(waist_rise[1:])
    aux_return['material'] = str(material[1:])
    aux_return['showcase_id'] = current_showcase_id
    aux_return['price_item'] = price_item
    aux_return['price_item_desc'] = price_item_desc
    aux_return['description'] = description.text



    # aux_return.to_csv('temp.csv')
    # print(aux_return)
    # time.sleep(22020)
    return(aux_return)


def color_clicker_id(color_ids_from_prod_page,current_showcase_id):
    #clicar cor por cor
    # pegar tamanho + disponibilidade
    # pegar composition
    print("hello id clicker")
    aux_return = pd.DataFrame()
    for product_id in color_ids_from_prod_page:
        # Gets browser driver open on designated page
        url = 'https://www2.hm.com/en_us/productpage.' + str(product_id) + '.html'
        driver.get(url)
        # CHAMAR A FUNCAO DE PEGAR A PAGINA....
        aux_return = pd.concat([aux_return, get_more_selenium(product_id, current_showcase_id)], ignore_index=True)
        # time.sleep(1)
    print(aux_return.shape)
    return(aux_return)

def showcase_clicker(product_id_from_showcase):
    # product_id_from_showcase = [product_id_from_showcase[a + 15] for a in range(16)]  # // TODO delete!
    # print("shorted product id showcase 6 1st items")
    # print(product_id_from_showcase)  # for testing, purposes - to be deleted
    # time.sleep(2)
    aux_return = pd.DataFrame()
    for product_id in product_id_from_showcase:
        url = 'https://www2.hm.com/en_us/productpage.' + str(product_id) + '.html'
        driver.get(url)
        page_source = driver.page_source
        print('got:')
        print(url)
        # CALL FUNCTION GET IDs BY color....
        current_showcase_id = product_id  # TODO coment out.

        aux_return = pd.concat([aux_return, color_clicker_id(get_colors_ids_from_prod_page(page_source), current_showcase_id)], ignore_index=True)
    return(aux_return)

def get_colors_ids_from_prod_page(page_source):
    # print(page_source)
    soup = BeautifulSoup(page_source)
    color_list_soup = soup.find_all('a', class_='filter-option miniature')
    color_list_soup.append(soup.find_all('a', class_='filter-option miniature active')[0])
    # print(color_list_soup)
    color_list_codes = [a['data-articlecode'] for a in color_list_soup]  # RETURNING ID COLORS FOR MATCHING
    # print("this page color list:")
    # print(color_list_codes)  # OK it works Colors. list
    # time.sleep(1)
    return(color_list_codes)


main()





