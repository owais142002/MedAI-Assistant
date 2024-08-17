from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, PromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from tenacity import retry
from tenacity import stop_after_delay
from tenacity import RetryError
from tenacity import stop_after_attempt
from tenacity import wait_exponential
from datetime import datetime, timedelta
import tiktoken
import GlobalConstants
import requests
import json
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
from lxml import html

def get_data_from_medicinedb(keyword):
    response = requests.get(f'https://go.drugbank.com/unearth/q?searcher=drugs&query={keyword}')
    tree = html.fromstring(response.content)
    urls = ["https://go.drugbank.com/"+item for item in tree.xpath('//div[contains(@class,"unearth-search-hit ")]//a/@href')]
    if urls:
        response = requests.get(urls[0])
        tree = html.fromstring(response.content)
        medicine_summary = tree.xpath("(//*[@id='summary']/following-sibling::dd)[1]")[0].text_content()
        medicine_background = tree.xpath("(//*[@id='background']/following-sibling::dd)[1]")[0].text_content()
        medicine_indication = tree.xpath("(//*[@id='indication']/following-sibling::dd)[1]")[0].text_content()
        medicine_pharmacodynamics = tree.xpath("(//*[@id='pharmacodynamics']/following-sibling::dd)[1]")[0].text_content()
        medicine_generic_name = tree.xpath("(//*[@id='generic-name']/following-sibling::dd)[1]")[0].text_content()
        return f"Generic name of the medicine {keyword.capitalize()} is {medicine_generic_name}.\nSummary of medicine is: {medicine_summary}.\nIndication of the medicine is: {medicine_indication}.\nBackground of the medicine is: {medicine_background}\nEffects of medicine is:{medicine_pharmacodynamics}"  
    else:
        return "Not able to find details of the medicine."  

def get_data_from_image(system_message, image_url):
    client = OpenAI(api_key=GlobalConstants.LLM_API_KEY)
    response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": system_message},
            {
            "type": "image_url",
            "image_url": image_url
            },
        ],
        }
    ],
    max_tokens=300,
    )
    return response.choices[0].message.content

def get_data_from_fibbit(start_date, end_date, access_token, get_random_sample=False):
    if get_random_sample:
        with open('./app/sample_heart_rate.json', 'r') as file:
            data = json.load(file)        
        return data
    headers = {
        'Authorization': f'Bearer {access_token}'
    }   
    url = f'https://api.fitbit.com/1/user/-/activities/heart/date/{start_date}/{end_date}.json'
    response = requests.get(url, headers=headers)    
    if response.status_code == 200:
        heart_rate_data = response.json()
        return heart_rate_data
    else:
       return "Unable to get the data"
    
def simplify_heart_rate_data(raw_data):
    simplified_data = []
    for day_data in raw_data["activities-heart"]:
        date = day_data["dateTime"]
        resting_heart_rate = day_data["value"]["restingHeartRate"]
        
        total_heart_rate = 0
        total_minutes = 0
        max_heart_rate = 0
        
        for zone in day_data["value"]["heartRateZones"]:
            total_heart_rate += (zone["max"] + zone["min"]) / 2 * zone["minutes"]
            total_minutes += zone["minutes"]
            max_heart_rate = max(max_heart_rate, zone["max"])
        
        average_heart_rate = total_heart_rate / total_minutes if total_minutes > 0 else 0
        
        simplified_data.append({
            "date": date,
            "resting_heart_rate": resting_heart_rate,
            "average_heart_rate": average_heart_rate,
            "max_heart_rate": max_heart_rate
        })
    
    return simplified_data

def safe_access_event(event, keys):
    """
    Safely access nested keys in a data structure which can be a mix of lists and dicts.
    :param event: The data structure to access (can be a dict or list).
    :param keys: List of keys/indexes to access in order.
    :return: The value if it exists, otherwise None.
    """
    current_data = event
    for key in keys:
        try:
            current_data = current_data[key]
        except (TypeError, KeyError, IndexError):
            return None

    return current_data


def getPromptTemplate(system_message):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    return prompt


def tiktoken_len(text):
  tokenizer = tiktoken.get_encoding('cl100k_base')
  tokens = tokenizer.encode(text, disallowed_special=())
  return len(tokens)

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(10))
def create_embedding(client,text):
    try:
        response = client.embeddings.create(
            model=GlobalConstants.LLM_MODEL,
            input=text
        )
        return (response, 'success')     
    except Exception as e:
        if 'The server is currently overloaded with other requests' in e:
            raise Exception
        else:
            return (e, 'failed')
        
def validate_and_convert_date(date_string):
  date = datetime.strptime(date_string, '%Y-%m-%d')
  date = date.date()
  epoch_start = datetime(1970, 1, 1).date()
  delta = date - epoch_start
  epoch_timestamp = int(delta.total_seconds())
  return epoch_timestamp

def removeDuplicatesRef(data):
  forDuplication = []
  returnList = []
  for instance in data:
    if instance['metadata']['content'] in forDuplication:
      continue
    returnList.append(instance)
    forDuplication.append(instance['metadata']['content'])
  return returnList

tokenizer = tiktoken.get_encoding('cl100k_base')

def limit_tokens_from_string(string):
    """Returns the string with token of 3000 and then length of the token of string."""
    encoding = tiktoken.get_encoding("cl100k_base")
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    while len(encoding.encode(string)) >= 3000:
        string = string[:len(string) - 5]
    return string