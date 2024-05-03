# Code Structure of the project

## Introduction
This document outlines the structure and functionality of the various modules and functions utilized within this project.

## Utilizing GPT for Presentation Generation

The core functionality of this application is in `flaskapp.py`, where various functions are called to handle different 
aspects of the application. One crucial part of this script is the endpoint defined for generating presentations based 
on user input:

```python
@app.route('/generator', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        number_of_slide = request.form['number_of_slide']
        user_text = request.form['user_text']
        template_choice = request.form.get('template_choice')
        presentation_title = request.form['presentation_title']
        presenter_name = request.form['presenter_name']
        insert_image = 'insert_image' in request.form
```
In the snippet above, we define an endpoint at `/generator` which accepts both `GET` and `POST` requests. 
When a `POST` request is made to this endpoint, the application collects necessary information from the user through 
a form submission. This information includes the number of slides, text content, template choice, presentation title, 
presenter name, and an option to insert images.

The next snippet demonstrates how we prepare the user's input for processing by the GEMINI model:
```python
user_message = f"I want you to come up with the idea for the PowerPoint. The number of slides is {number_of_slide}. " \
                f"The content is: {user_text}.The title of content for each slide must be unique, " \
                f"and extract the most important keyword within two words for each slide. Summarize the content for each slide. "
```

Rather than passing the raw user_text directly to GEMINI, we construct a formatted message, user_message, that encapsulates
the user's request in a structured manner. This approach enables a clearer communication of the user's intent to GEMINI, 
ensuring that the generated presentation aligns with the specified requirements. 
This formatting is robust to variations in user input, accommodating a range of phrasing and request complexities.

For instance, whether a user submits a content request as `Evolution of AI` or phrases it as `Can you make a 
presentation for Evolution of AI with clear examples?`, , the application is designed to interpret and process the 
request effectively.

Keyword extraction is later utilized for retrieving relevant images using the Pexels API.

In the code snippet below, `flaskapp.py` executes three functions:
  - `chat_development()` from `gpt_generate.py` located in `myapp/utils`, to retrieve GPT's response.
  - `parse_response()` from `text_pp.py` located in `myapp/utils`, to process the assistant's response and obtain the 
  - content for the slides.
  - `create_ppt()` from `text_pp.py` located in `myapp/utils`, to forward the slide content, template choice, 
  - presenter's name, and image insertion option.

```python
assistant_response = chat_development(user_message)
# Check the response (for debug)
print(assistant_response)
slides_content = parse_response(assistant_response)
create_ppt(slides_content, template_choice, presentation_title, presenter_name, insert_image)


>print(assistant_response) is used to check if the GPT is correctly responding or not.

assistant_response = chat_development(user_message)
# Check the response (for debug)
print(assistant_response)
slides_content = parse_response(assistant_response)
create_ppt(slides_content, template_choice, presentation_title, presenter_name, insert_image)
```

### `gpt_generate.py`

**build_conversation**

```python
def build_conversation(user_message):
    return user_message

def get_response_from_google_api(prompt):
    headers = {
        'Content-Type': 'application/json',
        'x-goog-api-key': API_KEY,
    }
  
    data = {
        "contents": [
                {"role": "user" ,"parts": [{"text": "You are an assistant that gives the idea for PowerPoint presentations. When answering, give the user the summarized content for each slide based on the number of slide. And the format of the answer must be Slide X(the number of the slide): {title of the content} \n Content: \n content with some bullet points. \n\n Keyword: \n Give the most important keyword (within two words) that represents the slide for each one. Content goes before and Keyword goes last. This is the prompt: "+prompt}]}
            
        ]
    }

    response = requests.post(
        "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent",
        headers=headers,
        data=json.dumps(data)
    )

    return response.json()
```

This function is defined to accept one argument: user_message, which is made in `flaskapp.py`. 
The content in the "system" role serves as an instruction or a **prompt** for the model, helping to set the context 
or the scenario in which the model should operate. This way, when the model receives the user's request in the "user" 
role, it has a clear understanding of how to handle and respond to that request in a manner that aligns with the given 
instruction. 
In the above code, we include how GPT should answer it in the prompt, so that we can get a response in such a way that,
```
Assistant Response:
Slide 1: Evolution of AI
Content:
- Overview of AI evolution
- Milestones of AI development
- Impact of AI on various industries
- Future prospects of AI
- Ethical considerations in AI development
Keyword: Evolution, AI
```

**generate_assistant_message**

```python
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
        generated_text = response_data['candidates'][0]['content']['parts'][0]["text"]
        print(f"Gemini Response: {generated_text}")
        extracted_text=generated_text
    else:
        print(f"Error: API request failed with status code: {response.status_code}")
    return extracted_text
```
A request is made to Gemini's ChatCompletion endpoint using the `get_response_from_google_api(conversation)` method.
The model parameter specifies the model version to use, in this case, **"GEMINI"**.
The messages parameter passes the conversation array (made in the `chat_development`) to the Gemini API.
Finally, it extracts and returns the content of the message generated by the assistant.

**chat_development**

```python
def build_conversation(user_message):
    return user_message
```
If you encounter the "Rate limit exceeded" message, it's advisable to check your Gemini API usage on
the [GEMINI API Usage](https://gemini.google.com/) page. This could potentially be a result of exhausting
your API rate limits, and verifying your usage might provide insights into the cause and possible solutions.