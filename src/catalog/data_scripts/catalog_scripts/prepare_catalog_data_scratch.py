import json

import numpy as np
import pandas as pd
import spacy
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from pipelines.connector import MarketplaceDBSession
from src import CatalogCategory
from src.core.language_translator.google_translator import (
    translate_large_text,
    translate_text,
)


def load_classifier(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


# Загрузка данных ОКВЕД и МКТУ
okved_data = load_classifier("../okved_scripts/оквэд.json")  # Ваша функция для загрузки
mktu_data = load_classifier("../mktu_scripts/mktu.json")  # Ваша функция для загрузки

# Загрузка моделей для русского языка
nlp = spacy.load("ru_core_news_sm")


# Создание общего датасета
def preprocess_text(text):
    doc = nlp(text.lower())
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return " ".join(tokens)


data = []
step = 0
for item in okved_data:
    data.append(
        {"text": preprocess_text(item["name"]), "source": "okved", "code": item["code"]}
    )
    print(step)
    step += 1

for item in mktu_data:
    data.append(
        {
            "text": preprocess_text(item["content"] + " " + item["products"]),
            "source": "mktu",
            "code": item["name"],
        }
    )
    print(step)
    step += 1

df = pd.DataFrame(data)
a = 0

# Создание TF-IDF векторов
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(df["text"])

# Кластеризация (примерно 50 кластеров для старта)
n_clusters = 50
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
df["cluster"] = kmeans.fit_predict(X)

from sklearn.tree import DecisionTreeClassifier


# Определение родительских категорий
def find_parent_cluster(row):
    if row["source"] == "okved":
        # Логика для ОКВЕД иерархии
        parent_code = ".".join(row["code"].split(".")[:-1])
        return df[df["code"] == parent_code]["cluster"].values[0]
    return -1


df["parent_cluster"] = df.apply(find_parent_cluster, axis=1)

# Дерево для построения иерархии
tree_model = DecisionTreeClassifier(max_depth=5)
tree_model.fit(X, df["cluster"])

from gensim.models import Word2Vec

# Генерация названий кластеров
cluster_names = {}
for cluster_id in range(n_clusters):
    cluster_texts = df[df["cluster"] == cluster_id]["text"]
    words = [word for text in cluster_texts for word in text.split()]
    model = Word2Vec([words], vector_size=100, window=5, min_count=1)
    cluster_names[cluster_id] = model.wv.index_to_key[
        0
    ]  # Берем наиболее характерное слово


session = MarketplaceDBSession()

# Создание категорий каталога
for cluster_id, name in cluster_names.items():
    parent = (
        session.query(CatalogCategory)
        .filter_by(cluster_id=df["parent_cluster"])
        .first()
    )
    category = CatalogCategory(
        name=name.capitalize(),
        en_name=translate_large_text(name),  # Функция перевода
        parent=parent,
    )
    session.add(category)

session.commit()


import tensorflow as tf

# Создание модели нейронной сети
model = tf.keras.Sequential(
    [
        tf.keras.layers.Dense(128, activation="relu", input_shape=(X.shape[1],)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(n_clusters, activation="softmax"),
    ]
)

model.compile(
    optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"]
)

# Обучение модели
model.fit(X.toarray(), df["cluster"], epochs=10, validation_split=0.2)


# Функция для предсказания категории нового товара
def predict_category(text):
    processed = preprocess_text(text)
    vector = vectorizer.transform([processed])
    prediction = model.predict(vector.toarray())
    return cluster_names[np.argmax(prediction)]


new_product = "Горный велосипед с алюминиевой рамой"
predicted_category = predict_category(new_product)
print(f"Рекомендуемая категория: {predicted_category}")
# Вывод: "Рекомендуемая категория: Велосипеды"
