import requests
import json
import datetime
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
from os.path import join, dirname, abspath, exists
from os import mkdir, remove
class Request: 
  def __init__(self, station, date):
    if station != None:
      self.station=str(station.upper())
    if date != None:
      try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        self.date=date
      except ValueError:
        raise ValueError("Incorrect date format, should be YYYY-MM-DD")        
  
  def getRawData(self):
    data=[]
    try:
        path = f"{join(dirname(abspath(__file__)),'data')}/{self.station}_{self.date}.json"
        file = open(path,"r")
        data = json.load(file)
        file.close()
        return data
    except Exception:
        url=f"https://public.opendatasoft.com/api/records/1.0/search/?dataset=donnees-synop-essentielles-omm&q=&refine.nom={self.station}&refine.date={self.date}&sort=date"
        data = requests.get(url).json()
        if len(data['records'])>0:
            #save data in a json file
            self.saveData(data)
        return data
  
  def printData(self):
      data=self.getRawData()
      records=data["records"]
      if len(data["records"])>0:
          line=[]
          line.append('| Station : '+str(records[0]['fields']['nom'])+", numéro "+str(records[0]['fields']['numer_sta']))
          line.append("| Date "+str(data['parameters']['refine']['date']))
          line.append("| Heure\t\t| T(°C)\t| Humidité(%)\t| Vitesse vent moy10min(m/s)")
          length=len(max(line,key=len))
          print("-" * (length +14))
          print(line[0].ljust(length-len(line[0])-1)+'\t\t\t\t\t|')
          print(line[1].ljust(length-len(line[1])-1)+'\t\t\t\t|')
          print(line[2].ljust(length-len(line[2])-1)+'\t|')
          print("-" * (length +14))
          for record in records:
            print(
              '| '+ str(record["fields"]["date"].split("T")[1].split("+")[0])+ '\t'
              '| '+str(round(float(record["fields"]['t'])-273.15,2))+ '\t'
              '| '+str(record["fields"]["u"])+ '\t\t'
              '| '+str(record["fields"]['ff'])+ '\t\t\t\t|'
            )
          print("-" * (length +14))
      else:
          print('no data for station '+str(self.station)+" at "+str(self.date))
  
  def saveData(self,data):
      mode = 0o666
      path=join(dirname(abspath(__file__)),'data')

      try:
        mkdir(path, mode)
      except FileExistsError:
        pass
      
      file=open(f"{path}/{self.station}_{self.date}.json","w")
      json.dump(data,file)
      file.close()
  
  @staticmethod
  def stations():
    url="https://public.opendatasoft.com/api/records/1.0/search/?dataset=donnees-synop-essentielles-omm&q=&facet=nom"
    data=requests.get(url).json()
    facets=data["facet_groups"][0]["facets"]
    names=[]
    for facet in facets:
        names.append(facet['name'])
    return names
  
  def savePlot(self):
      #Create folder of images
      dir="plots"
      mode = 0o666
      pathImg=join(dirname(abspath(__file__))+'/static',dir)
      try:
          mkdir(pathImg,mode)
      except FileExistsError:
          pass
      
      #read from json file
      dir="data"
      path=join(dirname(abspath(__file__)),dir)
      try:
          f=open(path+'/'+self.station+"_"+self.date+".json","r")
          data=json.load(f)
          f.close()
          records=data["records"]
          dates=[]
          temperature=[]
          humidity=[]
          windSpeed=[]
          for record in reversed(records):
              dates.append(record["fields"]["date"].split("T")[1].split("+")[0])
              temperature.append(round(float(record["fields"]['t'])-273.15))
              humidity.append(record["fields"]["u"])
              windSpeed.append(record["fields"]['ff'])
          plt.plot(dates,temperature, label = "Temperature")
          plt.plot(dates,humidity, label = "Humidité")
          plt.plot(dates,windSpeed, label = "Vitesse vents")
          plt.xlabel('temps')
          plt.ylabel('Les valeurs')
          plt.title('graph of station '+self.station+' at '+self.date)
          plt.legend()
          plt.savefig(pathImg+'/'+self.station+"_"+self.date+".png") 
          plt.cla()           
      except Exception:
          pass
  
  def checkPlot(self):
      pathImg=join(dirname(abspath(__file__))+'/static','plots')
      if not exists(pathImg+'/'+self.station+"_"+self.date+".png"):
          self.savePlot()
  
  def plot(self):
          try:
              self.checkPlot()
              pathImg=join(dirname(abspath(__file__))+'/static','plots')
              image=Image.open(pathImg+'/'+self.station+"_"+self.date+".png")
              image.show()
          except Exception:
              print("---- no data found for this station ------------")
  
  def saveWordCloud(self):
      #Create folder of wordCloud images
      dir="wordClouds"
      mode = 0o666
      pathImg=join(dirname(abspath(__file__))+'/static',dir)
      try:
          mkdir(pathImg,mode)
      except FileExistsError:
          pass
      exclure_words = ['d', 'du', 'de', 'la', 'des', 'le', 'et', 'est', 'elle', 'une', 'en', 'que', 'aux', 'qui', 'ces', 'les', 'dans', 'sur', 'l', 'un', 'pour', 'par', 'il', 'ou', 'à', 'ce', 'a', 'sont', 'cas', 'plus', 'leur', 'se', 's', 'vous', 'au', 'c', 'aussi', 'toutes', 'autre', 'comme']
      dir="data"
      path=join(dirname(abspath(__file__)),dir)
      text=""
      try:
          f=open(path+'/'+self.station+"_"+self.date+".json","r")
          data=json.load(f)
          records=data["records"]
          for record in records:
              try:
                  text=text+","+record["fields"]['temps_present']
                  text=text+','+record["fields"]['nom']
                  text=text+','+record["fields"]['libgeo']
                  text=text+','+record["fields"]['nom_reg']
                  text=text+','+record["fields"]['nom_epci']
                  text=text+','+record["fields"]['type_de_tendance_barometrique']
                  text=text+','+record["fields"]['temps_passe_1']
              except Exception:
                  pass
          wordcloud = WordCloud(background_color = 'white', stopwords = exclure_words, max_words = 80,width=1600, height=800).generate(text)
          if exists(pathImg+'/'+self.station+"_"+self.date+".png"):
              remove(pathImg+'/'+self.station+"_"+self.date+".png")
          wordcloud.to_file(pathImg+'/'+self.station+"_"+self.date+".png")    
      except Exception:
          pass        
  
  def checkWordCloud(self):
      pathImg=join(dirname(abspath(__file__))+'/static','wordClouds')
      if not exists(pathImg+'/'+self.station+"_"+self.date+".png"):
          self.saveWordCloud()
  
  def wordCloud(self):
      try:
          self.checkWordCloud()
          pathImg=join(dirname(abspath(__file__))+'/static','wordClouds')
          image=Image.open(pathImg+'/'+self.station+"_"+self.date+".png")
          image.show()
      except Exception:
          print("---- no data found for this station ------------")
