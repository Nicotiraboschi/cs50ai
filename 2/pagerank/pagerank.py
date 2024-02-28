import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]: .4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]: .4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
     
    new_dict = {}
    list_values = corpus[page]
    for key, value in corpus.items():
        if key in list_values:
            new_dict[key] = damping_factor / len(list_values)
            
        new_damping = 1-damping_factor if len(list_values) else 1
        new_value = new_damping / len(corpus)
                
        if key in new_dict and new_dict[key]:
            new_dict[key] += new_value
        else:
            new_dict[key] = new_value
            
    for key, value in new_dict.items():
        new_dict[key] = round(value, 3)
                    
    return new_dict   


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    current_page = random.choice(list((corpus.keys())))
    
    next_page_range = transition_model(corpus, current_page, damping_factor)
        
    return_dict = {}
    
    for i in range(n):
        items, weights = zip(*next_page_range.items())
        selected_page = random.choices(items, weights)[0]
        if selected_page in return_dict and return_dict[selected_page]:
            return_dict[selected_page] += 1
        else:
            return_dict[selected_page] = 1
        next_page_range = transition_model(corpus, selected_page, damping_factor)

    for key, value in return_dict.items():
        return_dict[key] = round(value/n, 4)
            
    return return_dict


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    numlinks = {}
    old_probs = {}
    len_corpus = len(corpus)
    
    for key, value in corpus.items():
        if len(corpus[key]) == 0:
            for page in corpus:
                corpus[key].add(page)
    
    for key, value in corpus.items():
        numlinks[key] = len(value)
    
    for key, value in corpus.items():
        old_probs[key] = 1/len_corpus
        
    new_probs = {}
    
    linking_pages = {}
    
    for key, value in corpus.items():
        for page in corpus:
            if key in corpus[page]:
                if key in linking_pages:
                    linking_pages[key].append(page)
                else:
                    linking_pages[key] = [page]
            else:
                if key not in linking_pages:
                    linking_pages[key] = []
        
    def calc():
        nonlocal old_probs
        nonlocal new_probs
        nonlocal linking_pages
        nonlocal len_corpus
        nonlocal numlinks

        for key in corpus:
            first_part = (1-damping_factor)/len_corpus
            summatory = 0
            for page in linking_pages[key]:
                summatory += old_probs[page] / numlinks[page]
            new_probs[key] = first_part + damping_factor * summatory
            
    calc()
    
    def check_if_continue():
        nonlocal old_probs
        nonlocal new_probs
        for key, value in old_probs.items():
            if round(value - new_probs[key], 4) != 0:
                return False
        return True
            
    while not check_if_continue():
        for key, value in new_probs.items():
            old_probs[key] = value
        calc()
        
    return new_probs
        

if __name__ == "__main__":
    main()
