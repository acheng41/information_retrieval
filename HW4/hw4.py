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
    
    return


def get_links(url):
    res = request.urlopen(url)
    return list(parse_links(url, res.read()))


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
        if parsed_link.netloc != base_domain and parsed_link.path != base_path:
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

    while not queue.empty():
        url = queue.get()
        if url in visited:
            continue
        try:
            req = request.urlopen(url)
            html = req.read()

            content_type = req.headers.get('Content-Type')
            if content_type is None:
                continue # content type is not specified
            if not any(content_type == content for content in wanted_content):
                continue # the content type does not match any of the content listed in wanted_content

            visited.append(url)
            visitlog.debug(url)

            for ex in extract_information(url, html):
                extracted.append(ex)
                extractlog.debug(ex)

            for link, title in parse_links(url, html):
                if within_domain:
                    if parse.urlparse(root).netloc == parse.urlparse(link).netloc:
                        continue # link that is being parsed is not in the domain that we're specifying
                if is_self_referencing(root, link, url):
                    continue # self-referencing link
                queue.put(link)

        except Exception as e:
            print(e, url)

    return visited, extracted

def is_self_referencing(root, link, url):
    if link == root or link == url:
        return True
    
    root_parsed = parse.urlparse(root)
    link_parsed = parse.urlparse(link)

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

    # don't need dashes maybe? optional?
    for match in re.findall('\d\d\d-\d\d\d-\d\d\d\d', str(html)):
        results.append((address, 'PHONE', match))

    for match in re.findall('\S+@\S+', str(html)):
        results.append((address, 'EMAIL', match))

    # what if city is multiple words? period?
    for match in re.findall('[a-zA-Z]+,\s[a-zA-Z]+\.?\s\d\d\d\d\d', str(html)):
        results.append((address, 'ADDRESS', match))

    return results


def writelines(filename, data):
    with open(filename, 'w') as fout:
        for d in data:
            print(d, file=fout)


def main():
    site = sys.argv[1]

    links = get_links(site)
    writelines('links.txt', links)

    nonlocal_links = get_nonlocal_links(site)
    writelines('nonlocal.txt', nonlocal_links)

    visited, extracted = crawl(site)
    writelines('visited.txt', visited)
    writelines('extracted.txt', extracted)



if __name__ == '__main__':
    main()


    # links = get_links("https://www.cs.jhu.edu")
    # print("ALL\n")
    # for link in links:
    #     print(str(link))
    
    # print("\nNONLOCAL\n")
    # links = get_nonlocal_links("https://www.cs.jhu.edu")
    # for link in links:
    #     print(str(link))