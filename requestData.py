import requests
import pandas as pd
import os
                                
def getResponse(community):
  ACCESS_TOKEN = os.getenv("ZenodoAPI")

  response = requests.get('https://zenodo.org/api/records',
                        params={'communities': community, 'size': 1000,
                                'access_token': ACCESS_TOKEN})
  
  return response

def requestData(response, communityDisplayName):
  
  data = response.json()
  
  #simplify needed json response
  neededData = data['hits']
  
  doi = []
  community = []
  title = []
  uniqueViews = []
  uniqueDownloads = []
  views = []
  downloads = []

  for i in range(0,  len(neededData['hits'])):
    doi.append(neededData['hits'][i]['metadata']['doi'])
    community.append(communityDisplayName)
    title.append(neededData['hits'][i]['metadata']['title'])
    uniqueViews.append(neededData['hits'][i]['stats']['unique_views'])
    uniqueDownloads.append(neededData['hits'][i]['stats']['unique_downloads'])
    views.append(neededData['hits'][i]['stats']['version_views'])
    downloads.append(neededData['hits'][i]['stats']['version_downloads'])
    
    df = pd.DataFrame(list(zip(doi, community, title, uniqueViews, uniqueDownloads, views, downloads)), columns =['doi', 'community', 'title', "uniqueViews", "uniqueDownlods", "views", "downloads"])
    
  return df
