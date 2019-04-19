#!/Library/Frameworks/Python.framework/Versions/3.7/bin/python3.7
import http.client
import json
import mysql.connector
import codecs


# petite fonction pour lire les resultats
def getResults(x):
    result = ""
    for i in x.split("|"):
        result = result+"\t"+i
    return result


athlete = input('Nom Athlete : ')
print("Recup des resultats de "+athlete)

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database='archerydb'
)
sql = "select id, fname, gname, noc, age from athlete where fname like '"+athlete+"%' order by gname, fname"
mycursor = mydb.cursor()
mycursor.execute(sql)
myresult = mycursor.fetchall()

for x in myresult:
  print(str(x[0])+" "+x[1]+" "+x[2]+" "+x[3]+" age:"+str(x[4]))

idAthlete = input('Identifiant : ')


conn = http.client.HTTPSConnection("api.worldarchery.org")
conn.request("GET", "/v3/ATHLETEMATCHES/?Id="+str(idAthlete)+"&RBP=1000")

# Lecture des donnees
r1 = conn.getresponse()
data1 = r1.read()
datastore = json.loads(data1)
listComp = []
#print(data1)
datastore = json.loads(data1)

with codecs.open(str(idAthlete)+".xls", 'w', encoding='utf8') as f:
  #f= open(str(idAthlete)+".xls","w+")
  print("CompID\tCompName\tCompPlace\tCompCountry\tCompDtFrom\tCompDtTo\tPhaseName\tFinalRank\tQualRank\tScore1\tSP1\tScore2\tSP2")
  f.write("CompID\tCompName\tCompPlace\tCompCountry\tCompDtFrom\tCompDtTo\tPhaseName\tFinalRank\tQualRank\tScore1\tSP1\tScore2\tSP2\n")
  for a in datastore["items"] :
      if not(listComp.__contains__(a["CompID"])) :
        listComp.append(a["CompID"])
      #print("comp1:"+a["Competitor1"]["Athlete"]["Id"])
      #print("comp2:"+a["Competitor2"]["Athlete"]["Id"])
      if (str(a["Competitor1"]["Athlete"]["Id"])==str(idAthlete)):
        print(str(a["CompID"])+"\t"+a["CompName"]+"\t"+a["CompPlace"]+"\t"+a["CompCountry"]+"\t"+a["CompDtFrom"]+"\t"+a["CompDtTo"]+"\t"+str(a["PhaseName"])+"\t"+str(a["Competitor1"]["FinalRank"])+"\t"+str(a["Competitor1"]["QualRank"])+"\t"+str(a["Competitor1"]["Score"])+"\t"+getResults(a["Competitor1"]["SP"])+"\t"+str(a["Competitor2"]["Score"])+"\t"+getResults(a["Competitor2"]["SP"]))
        f.write(str(a["CompID"])+"\t"+a["CompName"]+"\t"+a["CompPlace"]+"\t"+a["CompCountry"]+"\t"+a["CompDtFrom"]+"\t"+a["CompDtTo"]+"\t"+str(a["PhaseName"])+"\t"+str(a["Competitor1"]["FinalRank"])+"\t"+str(a["Competitor1"]["QualRank"])+"\t"+str(a["Competitor1"]["Score"])+"\t"+getResults(a["Competitor1"]["SP"])+"\t"+str(a["Competitor2"]["Score"])+"\t"+getResults(a["Competitor2"]["SP"])+"\n")
      else :
        print(str(a["CompID"])+"\t"+a["CompName"]+"\t"+a["CompPlace"]+"\t"+a["CompCountry"]+"\t"+a["CompDtFrom"]+"\t"+a["CompDtTo"]+"\t"+str(a["PhaseName"])+"\t"+str(a["Competitor2"]["FinalRank"])+"\t"+str(a["Competitor2"]["QualRank"])+"\t"+str(a["Competitor2"]["Score"])+"\t"+getResults(a["Competitor2"]["SP"])+"\t"+str(a["Competitor1"]["Score"])+"\t"+getResults(a["Competitor1"]["SP"]))
        f.write(str(a["CompID"])+"\t"+a["CompName"]+"\t"+a["CompPlace"]+"\t"+a["CompCountry"]+"\t"+a["CompDtFrom"]+"\t"+a["CompDtTo"]+"\t"+str(a["PhaseName"])+"\t"+str(a["Competitor2"]["FinalRank"])+"\t"+str(a["Competitor2"]["QualRank"])+"\t"+str(a["Competitor2"]["Score"])+"\t"+getResults(a["Competitor2"]["SP"])+"\t"+str(a["Competitor1"]["Score"])+"\t"+getResults(a["Competitor1"]["SP"])+"\n")

  f.close()

with codecs.open(str(idAthlete)+"_score.xls", 'w', encoding='utf8') as f:
  for x in listComp:
    conn.request("GET", "/v3/INDIVIDUALQUALIFICATIONS/?CompId="+str(x)+"&Id="+str(idAthlete)+"&RBP=1000")
    #print("/v3/INDIVIDUALQUALIFICATIONS/?CompId="+str(x)+"&Id="+str(idAthlete)+"&RBP=1000")
    r1 = conn.getresponse()
    data1 = r1.read()
    datastore = json.loads(data1)
    for a in datastore["items"] :
      for b in a["Results"] :
        print(str(x)+"\t"+str(b["Score"]))
        f.write(str(x)+"\t"+str(b["Score"])+"\n")

  
  f.close()
