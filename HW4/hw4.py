import logging
import re
import sys
from bs4 import BeautifulSoup
from queue import Queue
from urllib import parse, request

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
    # TODO: implement
    links = list(parse_links(root, html))
    return relevance(links)

def relevance(links): 
    #define most relevant links by length of title and then length of the link
    #usually, descriptive titles can be helpful for finding information
    #usually, longer links can indicate paths that enter subpages to more specific information
    links.sort(key = lambda x: len(x[0]), reverse  = True) 
    links.sort(key = lambda x: len(x[1]), reverse = True)
    return links

def get_links(url):
    res = request.urlopen(url)
    return list(parse_links(url, res.read()))

# def get_links_sorted(url):
#     res = request.urlopen(url)
#     return parse_links_sorted(url, res.read())


def get_nonlocal_links(url):
    '''Get a list of links on the page specificed by the url,
    but only keep non-local links and non self-references.
    Return a list of (link, title) pairs, just like get_links()'''

    # DONE: implement
    links = get_links(url)
    base_domain = parse.urlparse(url).netloc

    base_path = parse.urlparse(url).path


    filtered = []


    for link, title in links:
        parsed_link = parse.urlparse(link)
        parsed_path = parsed_link.path
        parsed_domain = parsed_link.netloc
        if parsed_domain != base_domain or parsed_path != base_path:
            filtered.append((link, title))


    return filtered


def crawl(root, wanted_content=[], within_domain=True):
    '''Crawl the url specified by `root`.
    `wanted_content` is a list of content types to crawl
    `within_domain` specifies whether the crawler should limit itself to the domain of `root`
    '''
    # TODO: implement

    queue = Queue()
    queue.put(root)

    visited = []
    extracted = []

    while not queue.empty() and len(visited) < 5:
  
        url = queue.get()
        if url in visited:
            continue
        try:
            req = request.urlopen(url)
            html = req.read().decode('utf-8', 'ignore')

            visited.append(url)
            visitlog.debug(url)


            for ex in extract_information(url, html):
                extracted.append(ex)
                extractlog.debug(ex)
            
            for link, title in parse_links(url, html):
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

    for match in re.findall(r'\d\d\d-\d\d\d-\d\d\d\d', str(html)):
        results.append((address, 'PHONE', match))
    for match in re.findall(r'\(\d\d\d\)\s?\d\d\d-\d\d\d\d', str(html)):
        results.append((address, 'PHONE', match))

    for match in re.findall(r'(\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b)', str(html)):
        results.append((address, 'EMAIL', match))
    
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

    # links2 = get_links_sorted(site)
    # writelines('links2.txt', links2)

    nonlocal_links = get_nonlocal_links(site)
    writelines('nonlocal.txt', nonlocal_links)

    visited, extracted = crawl(site,['text/html'])

    writelines('visited.txt', visited)
    writelines('extracted.txt', extracted)



if __name__ == '__main__':
    main()
