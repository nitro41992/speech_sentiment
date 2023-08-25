import os
from google.cloud import speech
from google.cloud import language_v1
from pydub import AudioSegment

# Set your Google Application Credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path-to-your-service-account-file.json"
NUMBER_OF_CONTEXT_WORDS = 3
PATH_TO_AUDIO_FILE = "audio_file_name.wav"

def convert_to_mono(filename):
    audio = AudioSegment.from_wav(filename)

    # Check if audio is stereo (channels = 2)
    if audio.channels == 2:
        mono_audio = audio.set_channels(1)
        mono_filename = filename.replace('.wav', '_mono.wav')
        mono_audio.export(mono_filename, format='wav')
        return mono_filename

    return filename

def transcribe_audio(local_audio_path):
    client = speech.SpeechClient()

    with open(local_audio_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US"
    )

    response = client.recognize(config=config, audio=audio)

    full_transcript = ""
    for result in response.results:
        full_transcript += result.alternatives[0].transcript + " "

    return full_transcript.strip()

def get_sentiment_and_context(text_content):
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT, language="en")

    # Get sentiment analysis
    sentiment_response = client.analyze_sentiment(document=document)
    sentiment = sentiment_response.document_sentiment

    # Get entity analysis for context
    entity_response = client.analyze_entities(document=document)
    
    # Extract the most salient entities for context
    salient_entities = sorted(entity_response.entities, key=lambda entity: entity.salience, reverse=True)
    context_entities = [entity.name for entity in salient_entities[:NUMBER_OF_CONTEXT_WORDS]]  # Adjust this number as needed

    return sentiment, context_entities

def sentiment_description(score, magnitude):
    if -1.0 <= score < -0.7:
        sentiment_desc = "Very Negative"
    elif -0.7 <= score < -0.3:
        sentiment_desc = "Negative"
    elif -0.3 <= score <= 0.3:
        sentiment_desc = "Neutral"
    elif 0.3 < score <= 0.7:
        sentiment_desc = "Positive"
    else:  # 0.7 < score <= 1.0
        sentiment_desc = "Very Positive"

    if magnitude < 0.5:
        magnitude_desc = "Faint"
    elif 0.5 <= magnitude < 2.5:
        magnitude_desc = "Mild"
    elif 2.5 <= magnitude < 5:
        magnitude_desc = "Strong"
    else:  # magnitude >= 5
        magnitude_desc = "Very Strong"

    return sentiment_desc, magnitude_desc

if __name__ == "__main__":
    file_path = f"audio_clips/{PATH_TO_AUDIO_FILE}"
    print(file_path)

    mono_filename = convert_to_mono(file_path)
    transcript = transcribe_audio(mono_filename)
    
    sentiment, context = get_sentiment_and_context(transcript)
    sentiment_desc, magnitude_desc = sentiment_description(sentiment.score, sentiment.magnitude)

    print("Transcribed Text:", transcript)
    print(f"Sentiment Score (Technical): {sentiment.score} | Description: {sentiment_desc}")
    print(f"Sentiment Magnitude (Technical): {sentiment.magnitude} | Intensity: {magnitude_desc}")
    print("Context (salient entities):", ', '.join(context))