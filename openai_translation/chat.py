import os
import openai

def tranlate_sentence(s, language):
    
    prompt = "translate to " + language + " : " + s
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": prompt}
      ]
    )
    print("translation success...")
    return completion.choices[0].message.content.lstrip()[1:]


