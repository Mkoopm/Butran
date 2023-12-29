from transformers import MarianMTModel, MarianTokenizer

src_text = [
    "this is a sentence in english that we want to translate to french",
    "This should go to portuguese",
    "And this to Spanish",
]

model_name = "Helsinki-NLP/opus-mt-en-nl"
tokenizer = MarianTokenizer.from_pretrained(model_name)

model = MarianMTModel.from_pretrained(model_name)
translated = model.generate(**tokenizer(src_text, return_tensors="pt", padding=True))
tgt_text = [tokenizer.decode(t, skip_special_tokens=True) for t in translated]

print(f"{src_text}, translated:\n{tgt_text}")