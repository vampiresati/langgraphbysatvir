from transformers import MarianMTModel, MarianTokenizer

model_name = "Helsinki-NLP/opus-mt-hi-en"

tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

def translate_hindi_to_english(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True
    )

    translated = model.generate(**inputs)

    return tokenizer.decode(
        translated[0],
        skip_special_tokens=True
    )
if __name__ == "__main__":
    english = translate_hindi_to_english(
        "नमस्ते, आज हम कृत्रिम बुद्धिमत्ता के बारे में बात करेंगे।"
    )

    print(english)