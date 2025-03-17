from fastapi import FastAPI
import numpy as np

app = FastAPI()

# Загрузка модели и векторизатора при старте приложения
model = tf.keras.models.load_model("category_classifier_model.keras")
with open("tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# Функция для предсказания категории
def predict_category(text):
    processed = preprocess_text(text)
    vector = vectorizer.transform([processed])
    prediction = model.predict(vector.toarray())
    return cluster_names[np.argmax(prediction)]

# Пример маршрута в FastAPI
@app.post("/predict")
async def predict(product_description: str):
    category = predict_category(product_description)
    return {"category": category}


import pickle
import tensorflow as tf

# Сохранение модели
model.save("category_classifier_model.keras")

# Сохранение векторизатора
with open("tfidf_vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

import pickle
import tensorflow as tf

# Загрузка модели
model = tf.keras.models.load_model("category_classifier_model.keras")

# Загрузка векторизатора
with open("tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)