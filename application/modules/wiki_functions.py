import wikipediaapi
import re
import modules.app_utils as au

wiki = wikipediaapi.Wikipedia(user_agent='University Project (liamhefford7@gmail.com)', language='en')

def does_page_exist(title):
    page = wiki.page(title)
    return page.exists()

def get_canonical_title(title):
    """
    Return the canonical page.title for a page if it exists, otherwise None.
    This helps deduplicate pages (e.g. different aliases resolving to same page).
    """
    page = wiki.page(title)
    if page.exists():
        return page.title
    return None

def scrape_page(title):
    page = wiki.page(title)
    if page.exists():
        return page.text
    else:
        return None


def find_wikipedia_pages(entities):
    """Search Wikipedia for entities and return list of canonical page titles."""
    pages = []
    seen_pages = set()

    for entity_name, _ in entities:
        print(f"  Searching: {entity_name}...", end=" ")
        canonical_title = get_canonical_title(entity_name)
        if canonical_title and canonical_title not in seen_pages:
            pages.append(canonical_title)
            seen_pages.add(canonical_title)
            print(f"Found: {canonical_title}")
        elif canonical_title:
            print(f"Duplicate: {canonical_title}")
        else:
            print("Not found")

    return pages


def collect_wiki_sentences(page_titles):
    """Scrape Wikipedia pages and return flattened sentences with sources."""
    all_sentences = []
    sources = []

    for title in page_titles:
        print(f"  Scraping: {title}...", end=" ")
        content = scrape_page(title)
        if content:
            sentences = au.split_sentences(content)
            for s in sentences:
                cleaned = re.sub(r'\s+', ' ', s.replace('\n', ': ')).strip()
                all_sentences.append(cleaned)
                sources.append(title)
            print(f"{len(sentences)} sentences")
        else:
            print("No content")

    return all_sentences, sources