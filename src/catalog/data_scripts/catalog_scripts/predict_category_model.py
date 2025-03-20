import pickle

import numpy as np
import tensorflow as tf

from src.catalog.data_scripts.catalog_scripts.prepare_catalog_data_scratch import (
    preprocess_text, vectorizer)

# Загрузка DataFrame
with open("intermediate_data.pkl", "rb") as f:
    df = pickle.load(f)

# Загрузка TF-IDF векторов
with open("tfidf_vectors.pkl", "rb") as f:
    X = pickle.load(f)

# Загрузка кластеризованных данных
with open("clustered_data.pkl", "rb") as f:
    df = pickle.load(f)

# Загрузка названий кластеров
with open("cluster_names.pkl", "rb") as f:
    cluster_names = pickle.load(f)

# Создание модели нейронной сети
n_clusters = 50
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
