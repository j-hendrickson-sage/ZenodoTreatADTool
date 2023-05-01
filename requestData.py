import requests
import pandas as pd
import os
                                
def getResponse(community):
  ACCESS_TOKEN = os.getenv("ZenodoAPI")

  response = requests.get('https://zenodo.org/api/records',
                        params={'communities': community, 'size': 10000,
                                'access_token': ACCESS_TOKEN})
  
  return response

def requestData(response, communityDisplayName):
  
  data = response.json()
  
  #simplify needed json response
  neededData = data['hits']['hits']
  
  doi = []
  community = []
  title = []
  uniqueViews = []
  uniqueDownloads = []
  views = []
  downloads = []
  publicationDate = []

  for i in range(0,  len(neededData)):
    doi.append(neededData[i]['metadata']['doi'])
    community.append(communityDisplayName)
    title.append(neededData[i]['metadata']['title'])
    uniqueViews.append(neededData[i]['stats']['unique_views'])
    uniqueDownloads.append(neededData[i]['stats']['unique_downloads'])
    views.append(neededData[i]['stats']['version_views'])
    downloads.append(neededData[i]['stats']['version_downloads'])
    publicationDate.append(neededData[i]['metadata']['publication_date'])
    
    df = pd.DataFrame(list(zip(doi, community, title, uniqueViews, uniqueDownloads, views, downloads, publicationDate)), columns =['doi', 'community', 'title', "uniqueViews", "uniqueDownlods", "views", "downloads", "publicationDate"])
    
  return df
