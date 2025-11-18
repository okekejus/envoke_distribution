import requests 
import concurrent.futures 
from requests.auth import HTTPBasicAuth
import os
import json 
from pandas import DataFrame
import pandas as pd 
import datetime as dt 
from dotenv import load_dotenv
import time
import numpy as np 


def create_contact_dicts(contact_list_dataframe): 
    """ Creating a dict for all contacts using information gotten from CRM/Advanced find"""
    holder = []
    for index, row in contact_list_dataframe.iterrows(): 
        p_d = {"remote_id": "", 
            "first_name": "", 
            "last_name": "", 
            "title": "", 
            "email": "", 
            "company": "", 
            "phone": "", 
            "address_1": "", 
            "address_2": "", 
            "city": "Toronto",
            "country": "CA", 
            "province": "ON", 
            "postal_code": "", 
            "website": "", 
            "language": "",
            "feedback": "", 
            "consent_status": "Implied - Transaction", 
            "consent_description": "Implied consent"}
    
        p_d['first_name'] = row["first_name"]
        p_d["last_name"] = row["last_name"]
        p_d["email"] = row["email_contact"]

        holder.append(p_d)
    return holder

def upsert_contact(contact_information, auth): 
    """ After creation of dicts, upsert contacts one by one"""
    url = "https://e1.envoke.com/v1/contacts?upsert=1"
    contact_info = json.dumps(contact_information, indent=2)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.request("POST", url, headers=headers, data=contact_info, auth=auth)
    return response


def send_survey(contact_info_dict, html_content, auth):
  url = "https://e1.envoke.com/api/v4legacy/send/SendEmails.json"

  payload = {
    "SendEmails": [
      {
        "EmailDataArray": [
          {
            "email": [
              {
                "to_email": contact_info_dict["email"],
                "to_name": f"{contact_info_dict["first_name"]} {contact_info_dict["last_name"]}",
                "from_email": "no-reply@org.ca",
                "from_name": "Justin Okeke",
                "reply_email": "no-reply@org.ca",
                "reply_name": "No Reply",
                "message_subject": "We Want Your Feedback!",
                "message_html": html_content
              }
            ]
          }
        ]
      }
    ]
  }

  headers = {'Content-Type': 'application/json'}
  try: 
    response = requests.request("POST",url, headers=headers, json=payload, auth=auth)
  except Exception as e: 
    response = e

  return response
