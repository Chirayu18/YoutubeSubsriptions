# See official documention of API:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
from os.path import expanduser

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
    
rss_file = expanduser("~/.config/youtube")
def main():
    
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    api_service_name = "youtube"
    api_version = "v3"
    #This is the oath2 file from google api
    client_secrets_file = "secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server(host='localhost',
        port=8080, 
        authorization_prompt_message='Goto browser', 
        success_message='Authentication Complete!',
    open_browser=True)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.subscriptions().list(
        part="snippet",
        maxResults=50,
        mine=True
    )
    response = request.execute()

    count = 0
    with open(rss_file,'w') as file:
        for i in response["items"]:
            count+=1
            file.write( "https://www.youtube.com/feeds/videos.xml?channel_id=" + str(i["snippet"]["resourceId"]["channelId"])+'\n')
        while "nextPageToken" in response :  
            request = youtube.subscriptions().list(
                part="snippet",
                maxResults=50,
                mine=True,
                pageToken=response["nextPageToken"]
            )
            response = request.execute()
            for i in response["items"]:
                count+=1
                file.write( "https://www.youtube.com/feeds/videos.xml?channel_id=" + str(i["snippet"]["resourceId"]["channelId"])+'\n')
    print(count, " entries added")
    
if __name__ == "__main__":
    main()
