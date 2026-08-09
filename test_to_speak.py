from gtts import gTTS


def speak_text(text, language="pa", filename="output.mp3"):
    tts = gTTS(
        text=text,
        lang=language,
        slow=False
    )

    tts.save(filename)

    print(f"Audio saved as {filename}")

if __name__ == "__main__":
    punjabi_text = "ਸਤ ਸ੍ਰੀ ਅਕਾਲ, ਅੱਜ ਅਸੀਂ ਆਰਟੀਫੀਸ਼ਲ ਇੰਟੈਲੀਜੈਂਸ ਬਾਰੇ ਗੱਲ ਕਰਾਂਗੇ।"
    speak_text(
        punjabi_text,
        language="pa",
        filename="punjabi.mp3"
    )