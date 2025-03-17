from huggingface_hub import snapshot_download
from transformers import MarianTokenizer, MarianMTModel
import torch


class LangTranslator:
    def __init__(self, from_lang: str = 'ru', to_lang: str = 'en', chunk_size: int = 3000):
        self.chunk_size = chunk_size

        # Скачиваем модель
        model_path = snapshot_download(repo_id=f"Helsinki-NLP/opus-mt-{from_lang}-{to_lang}", cache_dir="./models")

        # Загружаем токенизатор и модель
        self.tokenizer = MarianTokenizer.from_pretrained(model_path)
        self.model = MarianMTModel.from_pretrained(model_path)

        # Переносим модель на GPU, если он доступен
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)  # Переносим модель на GPU

    def _translate(self, text: str):
        # Токенизируем текст и переносим на GPU
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True).to(self.device)

        # Генерируем перевод
        translated = self.model.generate(**inputs)

        # Декодируем результат и возвращаем
        translated_text = self.tokenizer.decode(translated[0], skip_special_tokens=True)
        return translated_text

    def __call__(self, text: str):
        # Разбиваем текст на чанки и переводим каждый чанк
        chunks = [text[i:i + self.chunk_size] for i in range(0, len(text), self.chunk_size)]
        translated_chunks = [self._translate(chunk) for chunk in chunks]
        return " ".join(translated_chunks)