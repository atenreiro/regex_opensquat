import re
import time
import concurrent.futures
from tqdm import tqdm
import os


# Change Domain names and keywords file (if required)
domains_file = "domain-names-month.txt"
keywords_file = "keywords.txt"



##############################################################
start_time = time.time()

def search_keyword(data):
    keyword, domain_names = data
    matches = []
    pattern = re.compile(keyword)

    for dn_line in domain_names:
        match = pattern.search(dn_line)
        if match:
            matches.append(dn_line)
            #print(dn_line)

    return {
        'keyword': keyword,
        'matches': matches
    }

def is_valid_regex(pattern):
    try:
        return re.compile(pattern)
    except re.error:
        return None

def keyword_check():
    keywords = []

    with open(domains_file, 'r', encoding='utf-8') as dn:
        domain_names = dn.readlines()

    with open(keywords_file, 'r', encoding='utf-8') as kw:
        for kw_line in kw:
            kw_line = kw_line.strip()
            if kw_line.startswith(("#", " ")) or not kw_line:
                continue

            compiled_pattern = is_valid_regex(kw_line)
            if compiled_pattern:
                print(kw_line, "is a valid pattern")
                keywords.append(kw_line)
            else:
                print(kw_line, "is an invalid pattern! Exiting...")
                os.exit(1)

    # Utilizing parallel processing for searching keywords
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(tqdm(executor.map(search_keyword, [(k, domain_names) for k in keywords]),
                            total=len(keywords), desc="Processing Keywords"))

    for result in results:
        print(f"\nPattern search: {result['keyword']}")
        for match in result['matches']:
            print(match)
        print("Total matches:", len(result['matches']))

if __name__ == "__main__":
    keyword_check()
    elapsed_time = time.time() - start_time
    print(f"\nScript executed in {elapsed_time:.2f} seconds.")
