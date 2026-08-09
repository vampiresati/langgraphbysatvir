from gtts import gTTS


def speak_text(text, language="pa", filename="output.mp3"):
    tts = gTTS(
        text=text,
        lang=language,
        slow=False
    )

    tts.save(filename)

    print(f"Audio saved as {filename}")
    return filename
if __name__ == "__main__":
    punjabi_text = "aja appa punjabi wich gal kriye"
    fname=speak_text(
        punjabi_text,
        language="hi",
        filename="punjabi.mp3"
    )
    import subprocess

    subprocess.run(["xdg-open", fname])
