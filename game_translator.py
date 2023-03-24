from xunfei_speed_transcription.ost_fast import xf_transcriptor
from openai_translation.chat import tranlate_sentence
from record import Detector
import openai

appid = 
apikey = 
apisecret = 

openai.api_key = 

filepath = r"./audio/test.wav"

# detect audio
recorder = Detector(recording_file=filepath)
recorder.detect_audio()

# xunfei transcription
gClass = xf_transcriptor(appid, apikey, apisecret, filepath)
gClass.get_fileurl()
s = gClass.get_result()

# openai translation
target_language = "english"
res = tranlate_sentence(s, target_language)

print(res)
