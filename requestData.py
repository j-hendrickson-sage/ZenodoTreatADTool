import requests
import pandas as pd
                                
def getResponse():
  ACCESS_TOKEN = 'FUbPO66mRefZbFdQKNBbO7ZwTMMU37dQpaji4x4fZ08dpJnKYlHNyb6IFrv7'

  response = requests.get('https://zenodo.org/api/records',
                        params={'communities': 'treatad', 'size': 1000,
                                'access_token': ACCESS_TOKEN})
  
  return response

def requestData(response):
  
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
    community.append("TREAT-AD")
    title.append(neededData['hits'][i]['metadata']['title'])
    uniqueViews.append(neededData['hits'][i]['stats']['unique_views'])
    uniqueDownloads.append(neededData['hits'][i]['stats']['unique_downloads'])
    views.append(neededData['hits'][i]['stats']['version_views'])
    downloads.append(neededData['hits'][i]['stats']['version_downloads'])
    
    df = pd.DataFrame(list(zip(doi, community, title, uniqueViews, uniqueDownloads, views, downloads)), columns =['doi', 'community', 'title', "uniqueViews", "uniqueDownlods", "views", "downloads"])
    
  return df
