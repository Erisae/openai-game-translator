import sys

from difflib import SequenceMatcher

AUDIO_PATH = "../audio/test.wav"
AUDIO_MIN_RMS = 1000
MAX_LOW_AUDIO_FLAG = 70
BYTES_PER_SAMPLE = 2
CHANNEL_NUMS = 1
CHUNK_SIZE = 1024
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


def show_realtime_rms(rms, audio_min_rms=AUDIO_MIN_RMS):
    step = 40 / 2000  # 50#s for rms=2000
    sep = int(audio_min_rms * step)
    show = int(rms * step)
    print("\r", end="")
    progress = "current rms: "
    if show < sep:
        progress += "#" * show + " " * (sep - show)
    else:
        progress += "#" * sep
    progress += "|"

    if show > sep:
        progress += "#" * (show - sep)

    print(progress, end="")
    print("\033[K", end="")
    sys.stdout.flush()
