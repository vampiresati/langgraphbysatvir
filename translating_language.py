from transformers import MarianMTModel, MarianTokenizer


# Hindi -> English
HI_EN_MODEL = "Helsinki-NLP/opus-mt-hi-en"

hi_en_tokenizer = MarianTokenizer.from_pretrained(HI_EN_MODEL)
hi_en_model = MarianMTModel.from_pretrained(HI_EN_MODEL)


# English -> Indic languages
EN_INDIC_MODEL = "Helsinki-NLP/opus-mt-en-inc"

en_indic_tokenizer = MarianTokenizer.from_pretrained(EN_INDIC_MODEL)
en_indic_model = MarianMTModel.from_pretrained(EN_INDIC_MODEL)


def hindi_to_english(text):
    inputs = hi_en_tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True
    )

    output = hi_en_model.generate(**inputs)

    return hi_en_tokenizer.decode(
        output[0],
        skip_special_tokens=True
    )


def english_to_punjabi(text):

    # Important: tell multilingual model the target language
    text = f">>pan_Guru<< {text}"

    inputs = en_indic_tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True
    )

    output = en_indic_model.generate(**inputs)

    return en_indic_tokenizer.decode(
        output[0],
        skip_special_tokens=True
    )


if __name__ == "__main__":

    hindi = "नमस्ते, आज हम कृत्रिम बुद्धिमत्ता के बारे में बात करेंगे।"

    english = hindi_to_english(hindi)

    punjabi = english_to_punjabi(english)

    print("Hindi:")
    print(hindi)

    print("\nEnglish:")
    print(english)

    print("\nPunjabi:")
    print(punjabi)