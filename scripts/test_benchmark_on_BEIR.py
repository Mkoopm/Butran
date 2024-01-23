#### Provide the data_path where scifact has been downloaded and unzipped
# corpus, queries, qrels = GenericDataLoader(data_folder=data_path).load(split="test")


# translator = TranslatorMarianMT("en", "nl")

# #### Load the SBERT model and retrieve using cosine-similarity
# model = DRES(models.SentenceBERT("msmarco-distilbert-base-tas-b"), batch_size=16)
# retriever = EvaluateRetrieval(model, score_function="dot") # or "cos_sim" for cosine similarity
# results = retriever.retrieve(corpus, queries)

# #### Evaluate your model with NDCG@k, MAP@K, Recall@K and Precision@K  where k = [1,3,5,10,100,1000]
# ndcg, _map, recall, precision = retriever.evaluate(qrels, results, retriever.k_values)
