import spacy


def extract_entities(text, ner_model):
    # Extract entities from text using spacy, filtering by specific entity types.

    doc = ner_model(text)
    entities = []
    for ent in doc.ents:
        if ent.label_ in [
            # People and groups
            "PERSON", "NORP",
            # Locations
            "GPE", "LOC", "FAC",
            # Organizations and products
            "ORG", "PRODUCT",
            # Art, events, laws, language
            "WORK_OF_ART", "EVENT", "LAW", "LANGUAGE",
            # Dates and times
            "DATE",
        ]:
            entities.append((ent.text, ent.label_))

    # Deduplicate entities
    seen = set()
    deduplicated_entites = []
    for ent_text, label in entities:
        key = ent_text.strip().lower()
        if key not in seen:
            seen.add(key)
            deduplicated_entites.append((ent_text, label))

    return deduplicated_entites
