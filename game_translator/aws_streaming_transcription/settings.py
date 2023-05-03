from difflib import SequenceMatcher

AUDIO_PATH = "../audio/test.wav"
AUDIO_MIN_RMS = 30
MAX_LOW_AUDIO_FLAG = 100
BYTES_PER_SAMPLE = 2
CHANNEL_NUMS = 1
CHUNK_SIZE = 1024 * 8
REGION = "us-east-1"  # new york
SAMPLE_RATE = 16000
MIN_SIMILARITY = 0.5

LANGUAGE_MAPPING = {
    "english": "en-US",
    "chinese": "zh-CN",
    "french": "fr-FR",
    "german": "de-DE",
    "japanese": "ja-JP",
    "korean": "ko-KR",
    "russian": "ru-RU",
    "spanish": "es-ES",
}


def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()


def select_result(sentences):
    # filter and concact
    s = ""
    last = ""
    for cur in sentences:
        if similarity(last, cur) < MIN_SIMILARITY:  # not similar: concact
            s += last
            last = cur
        elif len(last) < len(cur):  # similar and longer: update
            last = cur
    s += last
    return "".join(s)
