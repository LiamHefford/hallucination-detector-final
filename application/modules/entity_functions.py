def extract_entities(text, ner_model):
    """
    Extracts named entities from the provided text using the spacy library.
    Returns a list of tuples containing the entity text and its corresponding label.
    """

    text = ner_model(text)
    entities = []
    for ent in text.ents:
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
            "DATE", "TIME",
            # Numeric values
            "MONEY", "PERCENT", "QUANTITY", "ORDINAL", "CARDINAL"
        ]:
            entities.append((ent.text, ent.label_))
    return entities

def trim_entity_list(entities):
    """
    Returns a new list of entities with numeric values and time entities removed.
    Excludes: MONEY, PERCENT, QUANTITY, ORDINAL, CARDINAL, TIME
    """

    excluded_labels = {"MONEY", "PERCENT", "QUANTITY", "ORDINAL", "CARDINAL", "TIME"}
    return [(entity, label) for entity, label in entities if label not in excluded_labels]


def extract_unique_entities(text, ner_model):
    """Extract, trim, and deduplicate entities from text."""
    entities = extract_entities(text, ner_model)
    entities_trimmed = trim_entity_list(entities)

    seen = set()
    unique_entities = []
    for ent, label in entities_trimmed:
        key = ent.strip().lower()
        if key not in seen:
            seen.add(key)
            unique_entities.append((ent, label))

    return unique_entities