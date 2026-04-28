from sentence_transformers import util

def compute_similarity_matrix(te_model, input_sentences, wiki_sentences, batch_size=32):
    # Compute cosine similarity matrix between input sentences and wiki sentences

    print(f"\nEncoding {len(input_sentences)} input sentences...")
    input_embs = te_model.encode(
        input_sentences,
        convert_to_tensor=True,
        show_progress_bar=True,
        batch_size=batch_size
    )

    print(f"Encoding {len(wiki_sentences)} wiki sentences...")
    wiki_embs = te_model.encode(
        wiki_sentences,
        convert_to_tensor=True,
        show_progress_bar=True,
        batch_size=batch_size
    )

    return util.cos_sim(input_embs, wiki_embs)


def analyze_similarities(sim_matrix, input_sentences, wiki_sentences, wiki_sources, similarity_threshold=0.70, print_threshold=0.70):
    # Analyze the similarity matrix to find matches and print high-scoring pairs

    match_count = 0
    highest_sims = []

    for i, inp_sent in enumerate(input_sentences):
        sims = sim_matrix[i]
        max_sim, idx = float(sims.max()), int(sims.argmax())

        print(f"\n[{i+1}/{len(input_sentences)}] {inp_sent[:80]}...")

        # Print high-scoring matches
        high_scores = [(j, float(sims[j])) for j in range(len(wiki_sentences)) 
                       if float(sims[j]) >= print_threshold]
        for j, score in sorted(high_scores, key=lambda x: -x[1])[:3]:
            print(f"  [{wiki_sources[j]}] ({score:.3f}): {wiki_sentences[j][:100]}...")

        if max_sim >= similarity_threshold:
            highest_sims.append(max_sim)
            match_count += 1
            print(f"  MATCHED ({max_sim:.3f})")
        else:
            highest_sims.append(0.0)
            print(f"  NO MATCH (best: {max_sim:.3f})")

    return match_count, highest_sims
