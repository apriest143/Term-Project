# Function that takes an image and returns the information about a date

#funtion that stores the information about the date

#function to call the information about certin date

import pytesseract
from PIL import Image
import os
from dotenv import load_dotenv
from datetime import datetime
from openai import OpenAI
from dateutil import parser

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
events = []

def image_upload(upload):
    image = Image.open(upload)
    text = pytesseract.image_to_string(image)
    return text


def analyze_text_with_ai(text):
    prompt = f"""
    Analyze the following text extracted from a flyer image and determine:
    1. The name of the event
    2. The date of the event
    3. The time of the event
    4. The location of the event

    If any information is missing or unclear, please indicate so.

    Extracted text:
    {text}

    Please format your response as follows:
    Event Name: [Event Name]
    Event Date: [Event Date]
    Event Time: [Event Time]
    Event Location: [Event Location]
    Additional Notes: [Any additional relevant information or uncertainties]
    """
    completion = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]
    )

    response_text = (completion.choices[0].message.content)
    event_data = {
        'name': '[Not provided]',
        'date': None,
        'time': None,
        'location': '[Not provided]',
        'description': 'No additional information.'
    }

    lines = response_text.strip().split('\n')
    for line in lines:
        if line.startswith('Event Name:'):
            event_data['name'] = line.replace('Event Name:', '').strip() or '[Not provided]'
        elif line.startswith('Event Date:'):
            date_str = line.replace('Event Date:', '').strip()
            try:
                event_data['date'] = parser.parse(date_str).date()
            except (ValueError, parser.ParserError):
                event_data['date'] = None
        elif line.startswith('Event Time:'):
            time_str = line.replace('Event Time:', '').strip()
            try:
                event_data['time'] = parser.parse(time_str).time()
            except (ValueError, parser.ParserError):
                event_data['time'] = None
        elif line.startswith('Event Location:'):
            event_data['location'] = line.replace('Event Location:', '').strip() or '[Not provided]'
        elif line.startswith('Additional Notes:'):
            event_data['description'] = line.replace('Additional Notes:', '').strip() or 'No additional information.'

    return event_data

    #print(completion.choices[0].message.content)
    #print response.json()['choices'][0]['message']['content']
    #logic for fining event info 



# text = image_upload("/Users/coledavenport/Documents/Term-Project/flyerflask/static/uploads/IMG_3746.png")
# print (text)
# event = (analyze_text_with_ai(text))
# print (event)