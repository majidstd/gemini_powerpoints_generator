import os
import openai
from dotenv import load_dotenv
import requests
import json

load_dotenv()
#openai.api_key = os.getenv("OPENAI_API_KEY")
API_KEY = os.getenv('API_KEY')

def chat_development(user_message):
    conversation = build_conversation(user_message)
    #try:
    assistant_message = generate_assistant_message(conversation)
    #except openai.error.RateLimitError as e:
    #    assistant_message = "Rate limit exceeded. Sleeping for a bit..."
    print("---->",assistant_message)
    return assistant_message


def build_conversation(user_message):
    return user_message
    """return [
        {"role": "system",
         "content": "You are an assistant that gives the idea for PowerPoint presentations. When answering, give the user the summarized content for each slide based on the number of slide. "
                    "And the format of the answer must be Slide X(the number of the slide): {title of the content} /n Content: /n content with some bullet points."
                    "Keyword: /n Give the most important keyword(within two words) that represents the slide for each one"},
        {"role": "user", "content": user_message}
    ]
    """


def generate_assistant_message_old(conversation):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    return response['choices'][0]['message']['content']



def get_response_from_google_api(prompt):
    headers = {
        'Content-Type': 'application/json',
        'x-goog-api-key': API_KEY,
    }

    #data = {
    #    "contents": [
    #        {   
    #            "role": "user",
    #            "parts": [{"text": prompt}]
    #        }
    #    ]
    #}
    
    data = {
        "contents": [
    
                #{"role":"system","parts": [{"text": "You are an assistant that gives the idea for PowerPoint presentations. When answering, give the user the summarized content for each slide based on the number of slide. And the format of the answer must be Slide X(the number of the slide): {title of the content} /n Content: /n content with some bullet points. Keyword: /n Give the most important keyword(within two words) that represents the slide for each one"}] } ,
                #{"role": "user" ,"parts": [{"text": "You are an assistant that gives the idea for PowerPoint presentations. When answering, give the user the summarized content for each slide based on the number of slide. And the format of the answer must be Slide X(the number of the slide): {title of the content} /n Content: /n content with some bullet points. Keyword: /n Give the most important keyword(within two words) that represents the slide for each one. This is the prompt: "+prompt}]}
                {"role": "user" ,"parts": [{"text": "You are an assistant that gives the idea for PowerPoint presentations. When answering, give the user the summarized content for each slide based on the number of slide. And the format of the answer must be Slide X(the number of the slide): {title of the content} \n Content: \n content with some bullet points. \n\n Keyword: \n Give the most important keyword (within two words) that represents the slide for each one. Content goes before and Keyword goes last. This is the prompt: "+prompt}]}
            
        ]
    }

    response = requests.post(
        "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent",
        headers=headers,
        data=json.dumps(data)
    )

    return response.json()

def generate_assistant_message(conversation):
    print(conversation)
    response = get_response_from_google_api(conversation)
    print("-----------------------")
    print(response)
    print(type(response))
    if response!="": #response.status_code == 200:
        # Get the response data
        response_data = response #.json()
        # Access and print the generated text
        #generated_text = response_data["contents"][0]["generated"]["text"]
        generated_text = response_data['candidates'][0]['content']['parts'][0]["text"]
        print(f"Gemini Response: {generated_text}")
        extracted_text=generated_text
    else:
        print(f"Error: API request failed with status code: {response.status_code}")


    #extracted_text = response['candidates'][0]['content']['parts'][0]['text']
    #answer_edit.setText(extracted_text)
    return extracted_text

    #response = openai.ChatCompletion.create(
    #    model="gpt-3.5-turbo",
    #    messages=conversation
    #return response['choices'][0]['message']['content']

    


