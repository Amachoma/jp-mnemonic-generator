import requests
from bs4 import BeautifulSoup
import numpy as np
from scipy.stats import norm
from sklearn.cluster import KMeans

service_url = "https://text.ru/synonym"


def wilson_score_interval(likes, dislikes, confidence=0.95):
    n = likes + dislikes
    if n == 0:
        return None, None
    p = likes / n
    z = norm.ppf(1 - (1 - confidence) / 2)
    denominator = 1 + z ** 2 / n
    centre_adjusted_probability = p + z ** 2 / (2 * n)
    adjusted_standard_deviation = np.sqrt((p * (1 - p) + z ** 2 / (4 * n)) / n)
    lower_bound = (centre_adjusted_probability - z * adjusted_standard_deviation) / denominator
    upper_bound = (centre_adjusted_probability + z * adjusted_standard_deviation) / denominator
    return lower_bound, upper_bound


def get_synonym(word):
    web_page = requests.get(f"{service_url}/{word}")
    soup = BeautifulSoup(web_page.text, "html.parser")

    all_synonyms = []
    synonym_table = soup.find(attrs={"id": "table_list_synonym"})

    if synonym_table and synonym_table.find("td", attrs={"class": 'ta-l'}):
        for table_row in synonym_table.findAll("tr")[1:]:
            word = table_row.find("td", attrs={"class": 'ta-l'}).find("a").text

            like_count = int(
                table_row.find("a", attrs={'class': 'like'}).find(attrs={'class': 'number'}).text or 0)
            dislike_count = int(
                table_row.find("a", attrs={'class': 'dislike'}).find(attrs={'class': 'number'}).text or 0)

            lower_bound, _ = wilson_score_interval(like_count, dislike_count)
            if lower_bound:
                all_synonyms.append((word, lower_bound))

    sorted_synonyms = sorted(all_synonyms, key=lambda x: x[1], reverse=True)

    try:
        kmeans = KMeans(n_clusters=2, random_state=19).fit(np.array([x[1] for x in sorted_synonyms]).reshape(-1, 1))
        threshold = max(kmeans.cluster_centers_)[0]
        return list(x[0] for x in
                    filter(lambda item: item[1] >= threshold, sorted_synonyms))[:5]
    except:
        return []


if __name__ == "__main__":
    print(get_synonym("Стройка"))
