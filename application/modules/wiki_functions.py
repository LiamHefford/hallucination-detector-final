import wikipediaapi
import re

import modules.app_utils as au

wiki = wikipediaapi.Wikipedia(user_agent='University Project (liamhefford7@gmail.com)', language='en') # Wikipedia user agent, required for scraping text via API


def find_wikipedia_pages(entities):
    # Find Wikipedia pages for a list of entities.

    pages = []
    seen_pages = set()

    for entity_name, _ in entities:
        print(f"  Searching: {entity_name}...", end=" ")
        page = wiki.page(entity_name)
        canonical_title = page.title if page.exists() else None
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
    # Scrape text from a list of Wikipedia page titles and split into sentences

    all_sentences = []
    sources = []

    for title in page_titles:
        print(f"  Scraping: {title}...", end=" ")
        page = wiki.page(title)
        content = page.text if page.exists() else None
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