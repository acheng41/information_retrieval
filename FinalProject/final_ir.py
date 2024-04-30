import datetime
import logging
import re
import sys
from bs4 import BeautifulSoup
from queue import Queue
from urllib import parse, request
import heapq
import pandas as pd

logging.basicConfig(level=logging.DEBUG, filename='output.log', filemode='w')
visitlog = logging.getLogger('visited')
extractlog = logging.getLogger('extracted')


def parse_links(root, html):
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            text = link.string
            if not text:
                text = ''
            text = re.sub('\s+', ' ', text).strip()
            yield (parse.urljoin(root, link.get('href')), text)


def parse_links_sorted(root, html):
    # DONE: implement    
    priority = [] #create a priority queue using heapq
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            text = link.string
            if not text:
                text = ''
            text = re.sub('\s+', ' ', text).strip()
            #add link to queue sorting based on relevance function
            heapq.heappush(priority, ((rel(text)), (parse.urljoin(root, link.get('href')), text)))
    for link in priority:
        yield (heapq.heappop(priority)[1])

#generate priority using the length of the title
#usually, descriptive titles can be helpful for finding information
def rel(text):
    if len(text) == 0: 
        return 2
    else:
        return 1/ len(text)


def get_links(url):
    res = request.urlopen(url)
    return list(parse_links(url, res.read()))

# code to test output of sorted links
def get_links_sorted(url):
    res = request.urlopen(url)
    return list(parse_links_sorted(url, res.read()))


def get_nonlocal_links(url):
    '''Get a list of links on the page specificed by the url,
    but only keep non-local links and non self-references.
    Return a list of (link, title) pairs, just like get_links()'''

    # DONE: implement
    links = get_links(url)
    #get domain and path for the base link
    base_domain = parse.urlparse(url).netloc 
    base_path = parse.urlparse(url).path


    filtered = []
    for link, title in links:
        parsed_link = parse.urlparse(link)
        parsed_path = parsed_link.path
        parsed_domain = parsed_link.netloc
        #non-local links should not have the same domain 
        #self-referencing links have the same path
        if parsed_domain != base_domain or parsed_path != base_path:
            filtered.append((link, title)) #only add non-local and non-self referencing
    return filtered


def crawl(root, wanted_content=[], within_domain=True):
    '''Crawl the url specified by `root`.
    `wanted_content` is a list of content types to crawl
    `within_domain` specifies whether the crawler should limit itself to the domain of `root`
    '''
    # DONE: implement
    queue = Queue()
    queue.put(root)

    visited = []
    extracted = []

    while not queue.empty():
        url = queue.get()
        if url in visited: 
            continue #do not visit duplicates
        try:
            req = request.urlopen(url)
            html = req.read().decode('utf-8', 'ignore')

            visited.append(url)
            visitlog.debug(url)

            for ex in extract_information(url, html):
                print(ex)
                extracted.append(ex)
                extractlog.debug(ex)
            
            for link, title in parse_links(url, html):  #the regular crawler          
            # for link, title in parse_links_sorted(url, html): #custom link relevance sorting
                # print(link)
                req_link = request.urlopen(link)
                content_type = req_link.headers['Content-Type']
     
                if not any(content in content_type for content in wanted_content):
                    continue # the content type does not match any of the content listed in wanted_content
                
                
                if is_self_referencing(link, url):
                    continue
                if within_domain:
                    if parse.urlparse(root).netloc == parse.urlparse(link).netloc:
                        queue.put(link) # link that is being parsed is not in the domain that we're specifying
                else:
                    queue.put(link)

                # print(queue.__sizeof__())

        except Exception as e:
            print(e, url)

    return visited, extracted

def is_self_referencing(root, url):
    
    root_parsed = parse.urlparse(root)
    link_parsed = parse.urlparse(url)

    # Check if both URLs have the same netloc and path
    if root_parsed.netloc == link_parsed.netloc and root_parsed.path == link_parsed.path:
        return True
    
    # not self referencing
    return False


def extract_information(address, html):
    '''Extract contact information from html, returning a list of (url, category, content) pairs,
    where category is one of PHONE, ADDRESS, EMAIL'''
    
    # TODO: implement
    results = []

    #TODO:: Search for Price
    price_pattern =  r'\$\d+(\.\d+)?'
    for match in re.findall(price_pattern, str(html)):
        results.append((address, 'PRICE', match))
   
    # #TODO: Search for Travel Time
    # time_pattern =  r'\d+h \d+m'
    # for match in re.findall(time_pattern, str(html)):
    #     results.append((address, 'DURATION', match))
    
    #TODO: Search for Departure/ Arrival Time
    dept_arriv_pattern = r'^\d{2}:\d{2} (?:AM|PM)$'
    for match in re.findall(dept_arriv_pattern, str(html)):
        results.append((address, 'DEPT|ARR', match))
        print(match)



    return results

#TODO: Helper to match links with their info
#return a dictionary of dictionaries
#key: URL,val = dictionary
#dictionary contents: {mode: , departure: , arrival: , duration: , cost: , }
#mode depends on which site we crawl
def convert_time(time_str):
    # Convert time string to datetime object
    return datetime.strptime(time_str, '%I:%M %p')

def create_linkdf(extracted, link): 
    # Step 1: Extract unique links
    unique_links = set(item[0] for item in extracted)

    # Step 2: Collect data for each unique link
    rows = []
    for link in unique_links:
        link_data = {'Link': link, 'Dept|Arr': []}
        for item in extracted:
            if item[0] == link:
                if item[1] == 'PRICE':
                    link_data['Price'] = item[2]
                elif item[1] == 'DEPT|ARRIV':
                    link_data['Dept|Arr'].append(convert_time(item[2]))
        # sort based on the time that is already in the link's data
        link_data['Dept|Arr'] = sorted(link_data['Dept|Arr'])

        # subtracting and then converting to minutes
        duration = (link_data['Dept|Arr'][1] - link_data['Dept|Arr'][0]).total_seconds() / 60
        link_data['Duration'] = duration

        rows.append(link_data)

    # Step 3: Create DataFrame
    df = pd.DataFrame(rows)

    return df 

#TODO: group info with link

#DONE: function to determine which time is arrival and which is departure (TAYLOR)
#DONE: calcuate duration from arrival and deparure times (TAYLOR)

#TODO: create ranking functions  -- args (mode, dictionaries of info)
# cost
# travel time
#TODO: implement function to add time to get to airport, tsa, etc. 
# recommended -- our weighting



#TODO: create wrapper that crawls all travel websites 
#create dictionary from each website -- based on each website add mode



def writelines(filename, data):
    with open(filename, 'w') as fout:
        for d in data:
            print(d, file=fout)


def main():
    site = sys.argv[1]

    links = get_links(site)
    writelines('links.txt', links)

    # code to test sorted links
    links2 = get_links_sorted(site)
    writelines('links2.txt', links2)

    nonlocal_links = get_nonlocal_links(site)
    writelines('nonlocal.txt', nonlocal_links)

    visited, extracted = crawl(site,['text/html'])

    dictionary_links =  match_info(visited, extracted)
    print(extracted)

    # writelines('visited.txt', visited)
    # writelines('extracted.txt', extracted)


def run_query(date, time, destination):
    if destination.upper() == "BWI":
        location = "Baltimore"
    else:
        location = "New York"
    print("Generating results...\n")
    print("You want a trip to %s on %s arriving by %s\n\n" % (location, date, time))

    return


if __name__ == '__main__':
    main()