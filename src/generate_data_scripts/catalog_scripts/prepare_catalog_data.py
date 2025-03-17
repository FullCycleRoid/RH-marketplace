import os
import json
import pickle
import tensorflow as tf
import pandas as pd
from gensim.models import Word2Vec
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from src.generate_data_scripts.catalog_scripts.prepare_catalog_data_scratch import preprocess_text


def load_classifier(path: str) -> dict:
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Загрузка данных ОКВЕД и МКТУ
okved_data = load_classifier("../okved_scripts/оквэд.json")  # Ваша функция для загрузки
mktu_data = load_classifier("../mktu_scripts/mktu.json")    # Ваша функция для загрузки


# Проверка, существуют ли уже сохраненные данные
if os.path.exists("intermediate_data.csv"):
    # Загрузка данных из файлов
    df = pd.read_csv("intermediate_data.csv")
    X = pd.read_csv("tfidf_vectors.csv").values
    df = pd.read_csv("clustered_data.csv")
    with open("cluster_names.json", "r", encoding="utf-8") as f:
        cluster_names = json.load(f)
else:
    # Обработка данных и сохранение
    data = []
    step = 0
    for item in okved_data:
        data.append({"text": preprocess_text(item["name"]), "source": "okved", "code": item["code"]})
        print(step)
        step += 1

    for item in mktu_data:
        data.append({"text": preprocess_text(item["content"] + " " + item["products"]), "source": "mktu", "code": item["name"]})
        print(step)
        step += 1

    df = pd.DataFrame(data)
    df.to_csv("intermediate_data.csv", index=False)

    # Создание TF-IDF векторов
    vectorizer = TfidfVectorizer(max_features=1000)
    X = vectorizer.fit_transform(df["text"])
    pd.DataFrame(X.toarray()).to_csv("tfidf_vectors.csv", index=False)

    # Кластеризация
    n_clusters = 50
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df["cluster"] = kmeans.fit_predict(X)
    df.to_csv("clustered_data.csv", index=False)

    # Генерация названий кластеров
    cluster_names = {}
    for cluster_id in range(n_clusters):
        cluster_texts = df[df["cluster"] == cluster_id]["text"]
        words = [word for text in cluster_texts for word in text.split()]
        model = Word2Vec([words], vector_size=100, window=5, min_count=1)
        cluster_names[cluster_id] = model.wv.index_to_key[0]
    with open("cluster_names.json", "w", encoding="utf-8") as f:
        json.dump(cluster_names, f, ensure_ascii=False)


# Сохранение модели
model.save("category_classifier_model.keras")

# Сохранение векторизатора
with open("tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)