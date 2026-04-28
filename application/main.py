from sentence_transformers import SentenceTransformer
from pyfiglet import Figlet

import modules.app_utils as au
import modules.wiki_functions as wf
import modules.entity_functions as entf
import modules.embedding_functions as embf


# ----- Settings -----

similarity_threshold = 0.70
print_threshold = 0.70
batch_size = 32


# ----- Model Loading -----

def load_models():
    # Load and return the text embedding / NER models

    print("Loading sentence-transformers model 'all-mpnet-base-v2'...")
    te_model = SentenceTransformer('all-mpnet-base-v2')
    print("Model loaded.\n")

    print("Loading spacy English model 'en_core_web_sm'...")
    ner_model = entf.spacy.load("en_core_web_sm")
    print("Model loaded.\n")

    au.clear_console()

    return te_model, ner_model


# ----- Results Calculation -----

def calculate_confidence(match_count, total, highest_sims):
    # Calculate confidence metrics

    percent_matched = (match_count / total * 100) if total > 0 else 0
    average_highest = (sum(highest_sims) / len(highest_sims)) if highest_sims else 0.0
    confidence_score = (percent_matched + average_highest * 100.0) / 2.0

    return {
        'matched': match_count,
        'total': total,
        'percent_matched': percent_matched,
        'average_highest': average_highest,
        'confidence_score': confidence_score
    }


def print_results(results):
    # Print the results

    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Matched sentences: {results['matched']}/{results['total']}")
    print(f"Match percentage: {results['percent_matched']:.2f}%")
    print(f"Average highest similarity: {results['average_highest']:.3f}")
    print(f"Confidence score: {results['confidence_score']:.2f}%")
    print("=" * 60)


# ----- Analysis Pipeline -----

def analyze_text(text, te_model, ner_model):
    # Full analysis pipeline

    au.clear_console()

    # Stage 1: Extract entities
    print("\n[Stage 1] Extracting entities...\n")
    entities = entf.extract_entities(text, ner_model)
    print(f"Found {len(entities)} unique entities: {[e[0] for e in entities]}")

    if not entities:
        print("No entities found in text.")
        return
    
    input("\nPress Enter to continue...")
    au.clear_console()

    # Stage 2: Find Wikipedia pages
    print("\n[Stage 2] Searching Wikipedia...\n")
    pages = wf.find_wikipedia_pages(entities)
    print(f"\nFound {len(pages)} Wikipedia pages")

    if not pages:
        print("\nNo Wikipedia pages found for entities.")
        return

    input_sentences = au.split_sentences(text)
    if not input_sentences:
        print("No sentences found in input text.")
        return
    
    input("\nPress Enter to continue...")
    au.clear_console()

    # Stage 3: Collect wiki sentences
    print("\n[Stage 3] Scraping Wikipedia content...\n")
    wiki_sentences, wiki_sources = wf.collect_wiki_sentences(pages)
    print(f"\nTotal wiki sentences: {len(wiki_sentences)}")

    if not wiki_sentences:
        print("\nNo Wikipedia content to compare against.")
        return

    input("\nPress Enter to continue...")
    au.clear_console()

    # Stage 4: Compute similarities
    print("\n[Stage 4] Encoding text...")
    sim_matrix = embf.compute_similarity_matrix(
        te_model, input_sentences, wiki_sentences, batch_size
    )

    input("\nPress Enter to continue...")
    au.clear_console()

    # Stage 5: Analyze results
    print("\n[Stage 5] Analyzing matches...")
    match_count, highest_sims = embf.analyze_similarities(
        sim_matrix, input_sentences, wiki_sentences, wiki_sources,
        similarity_threshold, print_threshold
    )

    input("\nPress Enter to continue...")
    au.clear_console()

    # Stage 6: Calculate and display results
    results = calculate_confidence(match_count, len(input_sentences), highest_sims)
    print_results(results)


# ----- Menu -----

def display_menu():
    # Display the main menu and return the user's choice

    au.clear_console()

    # Display menu with Figlet header
    print("\n" + "=" * 62)
    f = Figlet(font='slant')
    print(f.renderText('Hallucination'))
    print(f.renderText('    Detector'))
    print("Liam Hefford - 100640433 - University of Derby\n".center(62))
    print("=" * 62)
    print("1. Analyze text")
    print("2. View current settings")
    print("3. Exit")
    print("=" * 62)
    print("")

    # Menu input loop
    while True:
        try:
            choice = int(input("Enter your choice (1-3): "))
            if 1 <= choice <= 3:
                return choice
            print("Please enter a number between 1 and 3.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 3.")


def view_settings():
    # Display current settings

    au.clear_console()
    print("\n" + "-" * 40)
    print("CURRENT SETTINGS")
    print("-" * 40)
    print(f"Similarity threshold: {similarity_threshold}")
    print(f"Print threshold: {print_threshold}")
    print(f"Batch size: {batch_size}")
    print("-" * 40)
    input("\nPress Enter to return to menu...")


# ----- Main -----

def main():
    # Main program loop

    te_model, ner_model = load_models()

    while True:
        choice = display_menu()

        if choice == 1:
            au.clear_console()
            print("\nEnter text to analyze (press Enter twice to submit):") # allows multi-line input
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            text = " ".join(lines)

            if text.strip():
                analyze_text(text, te_model, ner_model)
                input("\nPress Enter to continue...")
            else:
                print("No text entered.")

        elif choice == 2:
            view_settings()

        elif choice == 3:
            au.clear_console()
            print("\nExiting program...")
            break


if __name__ == "__main__":
    main()