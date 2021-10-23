from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from datetime import datetime

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1-e_-HTWNDuVG9JZKe53IDHeCLWTdhkta2WOnQy7wu2U'
SAMPLE_RANGE_NAME = 'Form Responses 3'

categories = ["likability bias","similarity bias","halo effect","candidate vs. position req.","question bias","intuition bias","description bias"]
def r_scorecalc(answer_values_list):
   r_list = []
   # likability
   likability_sum = 0
   for i in range(0, 4):
      likability_sum += answer_values_list[i]

   likability_sum /= 4
   likability_sum *= 10
   likability_sum -= 10
   r_list.append(likability_sum)
 

   # similarity
   similarity_sum = 0
   for i in range(4, 6):
      similarity_sum += answer_values_list[i]

   similarity_sum /= 2
   similarity_sum *= 10
   similarity_sum -= 10
   r_list.append(similarity_sum)


   # halo
   halo_sum = 0
   for i in range(6, 8):
      halo_sum += answer_values_list[i]
   
   halo_sum /= 2
   halo_sum *= 10
   halo_sum -= 10
   r_list.append(halo_sum)


   # requirements
   requirements_sum = 0
   for i in range(8, 11):
      requirements_sum += answer_values_list[i]

   requirements_sum /= 3
   requirements_sum *= 10
   requirements_sum -= 10 
   r_list.append(requirements_sum)


   # question
   question_sum = 0
   for i in range(11, 13):
      question_sum += answer_values_list[i]

   question_sum /= 2
   question_sum *= 10
   question_sum -= 10 
   r_list.append(question_sum)


   # intuition
   intuition_sum = 0
   for i in range(13, 14):
      intuition_sum += answer_values_list[i]

   intuition_sum /= 1
   intuition_sum *= 10 
   intuition_sum -= 10
   r_list.append(intuition_sum)


   # description
   description_sum = 0
   for i in range(14, 16):
      description_sum += answer_values_list[i]

   description_sum /= 2
   description_sum *= 10
   description_sum -= 10
   r_list.append(description_sum)
   return r_list

def calculate_values(answer_values_list):
  # r_list = r_scorecalc(answer_values_list)
   r_arrays = []
   for vals in answer_values_list:
      r_arrays.append(r_scorecalc(vals))

   # etc
 
   # then once we're done making the r_list, plot it!
   fig = go.Figure(
       data=go.Scatterpolar(
           r=r_arrays[0],
           theta = categories,
           fill="toself",
       )
   )
   r_arrays.pop(0)
   for rvalue in r_arrays:
      fig.add_trace(go.Scatterpolar(
         r= rvalue,
         theta = categories,
         fill = 'toself',
      ))
      fig.update_layout(
         polar=dict(
            radialaxis=dict(visible=True),
         ),
         showlegend=False,
      )
 
   fig.show()
 

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    x=input("please enter the date of the first form entry you’d like to plot (yyyy-mm-dd): ")     
    y =input("please enter the date of the second form entry you’d like to plot (yyyy-mm-dd): ")
    current = datetime.now()
    first_datetime = datetime.strptime(x,"%Y-%m-%d")
    second_datetime = datetime.strptime(y, "%Y-%m-%d")

   #  range_truth = first_datetime <= current <= second_datetime
   #  print(range_truth)
   
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
         values.pop(0)
         range_responses = []
         for row in values:
            current_datetime = datetime.strptime(row[1], "%Y-%m-%d")
            range_truth = first_datetime <= current_datetime <= second_datetime
            if range_truth:
               print(row)
 #              print(isinstance(row,list))
               clean_row = row
               clean_row.pop(0)
               clean_row.pop(0)
               int_array = list(map(int,clean_row))
               range_responses.append(int_array)
               print(int_array)
         calculate_values(range_responses)
         #for row in values:
        # Print columns A and E, which correspond to indices 0 and 4.
         #   print('%s, %s' % (row[0], row[1]))

if __name__ == '__main__':
    main()



