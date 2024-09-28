import csv
from io import StringIO
import json
import azure.functions as func
import logging

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient

import logging
import requests
import asyncio

import requests
#import csv
from codecs import iterdecode
from typing import  List


def get_key_vault_secret(vault_url: str, secret_name: str, credential: DefaultAzureCredential) -> str:
    secret_client: SecretClient = SecretClient(
        vault_url=vault_url, credential=credential)
    return secret_client.get_secret(secret_name).value


def csv_to_json(csv_content :str):
    csv_data : list[str] = StringIO(csv_content)
    csv_reader = csv.DictReader(csv_data)
    data = [row for row in csv_reader]
    for row in data:
        row['_id'] = int(row['_id'])
        row['Nr_Boczny'] = int(row['Nr_Boczny'])
        row['Ostatnia_Pozycja_Szerokosc'] = float(row['Ostatnia_Pozycja_Szerokosc'])
        row['Ostatnia_Pozycja_Dlugosc'] = float(row['Ostatnia_Pozycja_Dlugosc'])

    # Convert the list of dictionaries to a list of JSON strings
    json_messages = [json.dumps(row) for row in data]

    return json_messages


async def download_and_publish_events_csv(url:str, EVENT_HUB_NAME:str):

    key_vault_url = r'https://wkv3dc.vault.azure.net/'
    event_hub_connection_string_secret_name = r'eventHubConnectionStringMpkBuss'
    credential: DefaultAzureCredential = DefaultAzureCredential()

    EVENT_HUB_CONNECTION_STR = get_key_vault_secret(
        key_vault_url, event_hub_connection_string_secret_name, credential)

    try:
        producer = EventHubProducerClient.from_connection_string(
            conn_str=EVENT_HUB_CONNECTION_STR, eventhub_name=EVENT_HUB_NAME
        )
    except Exception as e:
        logging.info(f"Error getting the producer: {e}")

    response = requests.get(url)
    response.raise_for_status()  # Check for errors in the HTTP request

    # Get the CSV content as a string directly from the response csv_content: list[str]
    csv_content = csv_to_json(response.text)
    

    if producer == None:
        logging.info("producer empty")

    async with producer:
        # Create a batch.
        try:
            event_data_batch = await producer.create_batch()
        except Exception as e:
            logging.info(f"Error creating batch: {e}")

        for row in csv_content:
            event_data_batch.add(EventData(row))
            # logging.info('added a row')
        
        try:
            await producer.send_batch(event_data_batch)
            pass
        except Exception as e:
            logging.info(f"Error sending a batch: {e}")




app = func.FunctionApp()
@app.schedule(schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=True)
def timer_trigger(myTimer: func.TimerRequest) -> None:
    logging.info('timer trigger function processed a request.')
    api_url = r'https://www.wroclaw.pl/open-data/datastore/dump/17308285-3977-42f7-81b7-fdd168c210a2'
    EVENT_HUB_NAME = r'mpk_event_stream'

    asyncio.run(download_and_publish_events_csv(
        api_url, EVENT_HUB_NAME))
    #if myTimer.past_due:
        
        