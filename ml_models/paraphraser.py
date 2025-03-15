import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer


MODEL_NAME = 'cointegrated/rut5-base-paraphraser'
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME)
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME, legacy=True)

model.cuda()
model.eval()

def paraphrase(text, beams=10, grams=4, do_sample=True, temperature=0.7):
    x = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512).to(model.device)
    max_size = int(x.input_ids.shape[1] * 1.5 + 10)

    with torch.no_grad():
        out = model.generate(
            **x,
            encoder_no_repeat_ngram_size=grams,
            num_beams=beams,
            max_length=max_size,
            do_sample=do_sample,
            temperature=temperature
        )

    return tokenizer.decode(out[0], skip_special_tokens=True)
