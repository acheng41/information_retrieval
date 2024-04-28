import logging
import re
import sys
from bs4 import BeautifulSoup
from queue import Queue
from urllib import parse, request
import heapq

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
                extracted.append(ex)
                extractlog.debug(ex)
            
            # for link, title in parse_links(url, html):  #the regular crawler          
            for link, title in parse_links_sorted(url, html): #custom link relevance sorting
                print(link)
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

                print(queue.__sizeof__())

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
    
    # DONE: implement
    results = []

    #Search for Phone Numbers
    for match in re.findall(r'\d\d\d-\d\d\d-\d\d\d\d', str(html)):
        results.append((address, 'PHONE', match))
    for match in re.findall(r'\(\d\d\d\)\s?\d\d\d-\d\d\d\d', str(html)):
        results.append((address, 'PHONE', match))

    #search for emails
    for match in re.findall(r'(\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b)', str(html)):
        results.append((address, 'EMAIL', match))
    
    #search for addresses
    for match in re.findall(r'([A-Z][a-zA-Z\s]+),\s*([A-Z][a-zA-Z\s.]+)\s+(\d{5})', str(html)):
        results.append((address, 'ADDRESS', match))
        print(match)

    return results


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
    print(extracted)

    writelines('visited.txt', visited)
    writelines('extracted.txt', extracted)


def run_query(date, time, destination):
    if destination.upper() == "BWI":
        location = "Baltimore"
    else:
        location = "New York"
    print("Generating results...\n")
    print("You want a trip to %s on %s arriving by %s\n\n" % (location, date, time))

    return


