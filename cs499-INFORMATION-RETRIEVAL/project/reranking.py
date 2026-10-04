from googlesearch import search
from RankGPT.rank_gpt import permutation_pipeline, sliding_windows
import random
import numpy as np
import matplotlib.pyplot as plt

def precision_at_k(ground_truth, predicted_rank, k):
    true_positives = sum(1 for rank in predicted_rank[:k] if ground_truth[rank - 1])
    return true_positives / k

def ndcg_at_k(ground_truth, predicted_rank, k):
    max_rank = len(ground_truth)
    ground_truth_dcg = sum((2 ** (max_rank - 1 - k_i) - 1) / np.log2(2+k_i) for k_i in range(k))
    dcg = sum((2 ** (max_rank - rank) - 1) / np.log2(idx + 2) for idx, rank in enumerate(predicted_rank[:k]))
    return dcg/ground_truth_dcg

def mean_average_precision(ground_truth, predicted_rank):
    avg_precision = 0.0
    num_correct = 0
    for idx, rank in enumerate(predicted_rank):
        if ground_truth[rank - 1]:
            num_correct += 1
            avg_precision += num_correct / (idx + 1)
    return avg_precision / len(ground_truth)

def mean_reciprocal_rank(ground_truth, predicted_rank):
    for idx, rank in enumerate(predicted_rank):
        if ground_truth[rank - 1]:
            return 1 / (idx + 1)
    return 0

def misordered_pairs(ground_truth, predicted_rank):
    misordered = 0
    for i in range(len(ground_truth)):
        for j in range(i + 1, len(ground_truth)):
            if ground_truth[i] < ground_truth[j] and predicted_rank[i] > predicted_rank[j]:
                misordered += 1
            elif ground_truth[i] > ground_truth[j] and predicted_rank[i] < predicted_rank[j]:
                misordered += 1
    return misordered

def fetch_websites(query, num_results):
    try:
        # Perform the Google search
        search_results = search(query, num_results=num_results, sleep_interval=5, advanced=True)
        arr = []
        for result in search_results:
            arr.append({'content': f'Url: {result.url} Title: {result.title} Content: {result.description}'})
        return arr
    except Exception as e:
        print("An error occurred:", str(e))
        raise e

def get_api_key():
    file_path = "openAIKey.txt"
    with open(file_path, 'r') as file:
        api_key = file.read().strip()
    return api_key

def get_llama_key():
    return "LL-DTZe1ixVBkE9sUjG9qvimuyMvoS94LaJUeR5qgNcyvmmnwDRftR6RUskhnOxtMlu"
def rerank_with_description(query, num_results=100, rerank_iters=5, shuffle=True, method="permutation_pipeline", window_size=20, step=10, model_name='gpt-3.5-turbo'):
    openai_api_key = get_api_key()
    result_ranks = [np.arange(num_results)+1]

    print("Fetching websites...")
    item = {
        'query': query,
        'hits': fetch_websites(query, num_results)
    }

    # Create a dictionary to map unshuffled content to its index in obj
    content_to_index = {item['content']: idx + 1 for idx, item in enumerate(item['hits'])}

    # Shuffle ground truths
    if shuffle:
        random.shuffle(item['hits'])

    result = [content_to_index[item['content']] for item in item['hits']]
    result_ranks.append(result)
    print(f"Initial shuffle:\n{result}\n")

    # print(f'item: {item}')
    # print("lengths: ", [len(hit['content']) for hit in item['hits']])

    for i in range(rerank_iters):
        print(f"reranking iteration {i}")
        if method == "permutation_pipeline":
            new_item = permutation_pipeline(item, rank_start=0, rank_end=num_results, model_name=model_name, api_key=openai_api_key)
        elif method == "sliding_windows":
            new_item = sliding_windows(item, rank_start=0, rank_end=num_results, window_size=window_size, step=step, model_name=model_name, api_key=openai_api_key)
        else:
            print("INVALID RERANKING METHOD")
            exit()
        # print(f"run {i}: new_item:\n{new_item}\n")

        # Match the contents of new_obj with obj and get their indices
        result = [content_to_index[item['content']] for item in new_item['hits']]
        result_ranks.append(result)
        # print(f"run {i}:\n{result}\n")

    return result_ranks

def evaluate(result_ranks):
    ground_truth, *predictions = result_ranks
    results = {
        "ndcg_1_results": [],
        "ndcg_3_results": [],
        "ndcg_5_results": [],
        "ndcg_10_results": []
    }
    for i, predicted_rank in enumerate(predictions):
        print(f'iteration {i}:')
        print("prediction ranks: ", predicted_rank[:10])
        if -1 in ground_truth:
            print("Precision@3:", precision_at_k(ground_truth, predicted_rank, 5))
            print("MAP:", mean_average_precision(ground_truth, predicted_rank))
            print("MRR:", mean_reciprocal_rank(ground_truth, predicted_rank))
            print("Misordered pairs:", misordered_pairs(ground_truth, predicted_rank), '\n')
        results['ndcg_1_results'].append(ndcg_at_k(ground_truth, predicted_rank, 1))
        results['ndcg_3_results'].append(ndcg_at_k(ground_truth, predicted_rank, 3))
        results['ndcg_5_results'].append(ndcg_at_k(ground_truth, predicted_rank, 5))
        results['ndcg_10_results'].append(ndcg_at_k(ground_truth, predicted_rank, 10))
        print("NDCG@1:", results['ndcg_1_results'][-1])
        print("NDCG@3:", results['ndcg_3_results'][-1])
        print("NDCG@5:", results['ndcg_5_results'][-1])
        print("NDCG@10:", results['ndcg_10_results'][-1])

    return results

def plot(results={}):
    plt.figure(figsize=(10, 8))
    for i, key in enumerate(results):
        val = results[key]
        plt.subplot(2, 2, i+1)
        plt.plot(np.arange(len(val)), val)
        plt.title(key)
        plt.xlabel("iterations")
        plt.ylabel(key)
    plt.show()


if __name__ == "__main__":
    query = "Best restaurants in Seattle"
    query = "Information Retrieval"
    num_results = 200
    rerank_iters = 25

    # # permutation_pipeline_no_irrelevant
    # method = "permutation_pipeline"
    # print(f"\n\nReranking method: {method}")
    # result_ranks = rerank_with_description(query, num_results=num_results, method=method, rerank_iters=rerank_iters)
    # results = evaluate(result_ranks)
    # plot(results)

    # # permutation_pipeline_no_irrelevant_no_shuffle
    # method = "permutation_pipeline"
    # print(f"\n\nReranking method: {method}")
    # result_ranks = rerank_with_description(query, num_results=num_results, method=method, rerank_iters=rerank_iters, shuffle=False)
    # results = evaluate(result_ranks)
    # plot(results)


    # # sliding_windows_no_irrelevant.txt
    # method = "sliding_windows"
    # print(f"\n\nReranking method: {method}")
    # result_ranks = rerank_with_description(query, num_results=num_results, method=method, rerank_iters=rerank_iters)
    # results = evaluate(result_ranks)
    # plot(results)

    # # sliding_windows_no_irrelevant_no_shuffle.txt
    # method = "sliding_windows"
    # print(f"\n\nReranking method: {method}")
    # result_ranks = rerank_with_description(query, num_results=num_results, method=method, rerank_iters=rerank_iters, shuffle=False)
    # results = evaluate(result_ranks)
    # plot(results)

    # Llama
    num_results = 10
    rerank_iters = 2
    method = "sliding_windows"
    print(f"\n\nReranking method: {method}")
    result_ranks = rerank_with_description(query, num_results=num_results, method=method, rerank_iters=rerank_iters, window_size=4, step=2, model_name='llama')
    results = evaluate(result_ranks)
    plot(results)

