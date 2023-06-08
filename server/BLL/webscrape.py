import requests
from bs4 import BeautifulSoup
import requests_html as rh
from langdetect import detect

def web_scrape_all_information(searches_list,stores_list):
    '''
    This Function: web_scrape_all_information get search list and srors list from exeml file and fetch data from zap file
    '''
    urls_semi = list()
    links = list()
    item_stores_prices = list()
    indexs = list()
    indexs_prices = list()
    
    urls_semi = define_links(searches_list)
    #GET THE URL FOR ITEMS
    for i in range(len(searches_list)):
        links.append(get_url_for_item(urls_semi[i],searches_list[i]))
    #GET ITEM AND STORE INFORMATION
    for i in range(len(links)):
        item_stores_prices.append("")
        indexs.append(0)
        indexs_prices.append(0)
        item_stores_prices[i] ,indexs[i] ,indexs_prices[i]= get_item_store_webInfo(links[i],stores_list[i])
    #RETURN LINKS FOR EVERY ITEM , STORES AND PRICES FOR EACH ITEM , OUR STORE POSITION AND INDEX
    return links , item_stores_prices , indexs , indexs_prices

def define_links(searches_list):
    '''
    This Function: define_links  - This function turns urls into links
    get searches_list and return urls_list
    '''
    urls_list = list()
    for i in range(len(searches_list)):
        search_link = "https://www.zap.co.il/search.aspx?keyword="
        item = searches_list[i]
        link = " ".join([search_link, item])
        search_url = f"{link}"
        urls_list.append(search_url)
    return urls_list
    


def get_url_for_item(itemurl,itemname):

    #SETTING UP THE URL TO USE FOR WEBSCRAPE
    headers =   {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    url = itemurl
    response = requests.get(url,headers = headers)
    # Create a BeautifulSoup object by parsing the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
 
    reslut_not_found = "SearchResultsContainer"
    get_all_results = "ModelTitle"
    div_no_result = soup.find("div", class_=reslut_not_found)
    if div_no_result is not None:
        div_all_options = div_no_result.find_all("a",class_ = get_all_results)
        options = []
        for div in div_all_options:
            options.append(div)

        for i in range(len(options)):
            label = options[i].get("aria-label")
            href = options[i].get("href")
            itemname = delete_hebrew_words(itemname)
            if(label.find(itemname)!=-1):
                itemurl  = "https://www.zap.co.il" + href

    else:
        div_yes_result = soup.find('link',rel="canonical")
        if div_yes_result is not None:
            itemurl = div_yes_result.get("href")
    return itemurl

def delete_hebrew_words(link):
    link = link.split()
    for i in range(len(link)):
        try:
            language = detect(link[i])
            if language == 'he':
                link[i] = ""
        except:
            x=1
    link = ' '.join(link)
    return link

def get_item_store_webInfo(url,curStore):
    all_item_stores = []
    indexs = []
    indexs_prices = []
    #GETTING ALL THE INFORMAION ABOUT AN ITEM
    items = getAllStoresInItem(url)
    item = "compare-item-row"
    firstitem = items.find_all("div",class_ = item)
    all_items = []
    for div in firstitem:
        all_items.append(div)
    for i in range(len(all_items)):
        price = all_items[i].get("data-total-price")
        store = all_items[i].get("data-site-name")
        index = all_items[i].get("data-index")
        if curStore == store:
            indexs = index
            indexs_prices = price
        if(price != None and store != None):
            all_item_stores.append([price,store])
        
    return all_item_stores , indexs ,indexs_prices
    

def getAllStoresInItem(url):
    headers =   {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    response = requests.get(url,headers = headers)
    # Create a BeautifulSoup object by parsing the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    div_elements = soup.find_all('div')
    # Filter elements based on class name and data-group-sale-type attribute
    for div in div_elements:
        class_attr = div.get('class')
        sale_type = div.get('data-group-sale-type')
        
        if class_attr == ['compare-items-group'] and sale_type == '1':
            filtered_elements = div

    return filtered_elements

def filter_function(tag):
    return tag.name == 'div' and tag.get('class') == ['compare-items-group'] and tag.get('data-group-sale-type') == 'data-group-sale-type'
