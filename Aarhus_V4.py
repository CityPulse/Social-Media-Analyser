'''
Created on 7 Dec 2015

@author: Nazli Davar
'''

from bokeh._legacy_charts.builder.step_builder import Step
import pandas as pd 
import sys 
sys.path.append('/lib/messagebus')
sys.path.append('/lib/pika-0.10.0')
sys.path.append('/lib/geopy-1.10.0')
sys.path.append('/lib/goslate')
import subprocess 
import os
from collections import Counter
import numpy as np
from datetime import datetime
import codecs, json
import mysql as MySQLdb
from colorama import init
import site
init(wrap=True)
from colorama import Fore, Back, Style
import pylab as pl
import string
import random
from collections import Counter
import re
import shutil
import warnings
import platform
import time
import datetime
import unicodedata
from matplotlib import pyplot as plt
import pika
from geopy.geocoders import Nominatim
import goslate
from geopy.distance import vincenty
from rabbitmq import RabbitMQ
import uuid

workingDir= os.getcwd()
data_folder = workingDir+'/CRF_NER/CityEventExtraction/data/'
result_folder = workingDir+'/CRF_NER/CityEventExtraction/results/'
main_data_folder=result_folder
dictionary_folder=workingDir+'/CRF_NER/CityEventExtraction/dictionary/'

JAVA_DIR = workingDir+'/CRF_NER/CityEventExtraction'
SENNA_DIR=workingDir+'/CNN_senna'
tags_folder=workingDir+'/TagCollection/'
city='Aarhus'
if city=='Aarhus':
    geo_centre=(10.2074, 56.1526)
    city_BB=[(10.1800, 56.1420), (10.2340, 56.1721)]
elif city=='London':
    geo_centre=(-0.127, 51.507) 
    city_BB=[(-0.489,51.28),(0.236,51.686)]
NOW = datetime.datetime.now() 
step = datetime.timedelta(seconds=60) 
# cmd="php /Phirehose-master/example/filter-geo-"+city+".php"
#shell_cmd = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, shell=True)
# os.system("php /user/eestf/nf0010/Desktop/SmartCity/Tools/Phirehose-master/example/filter-track-geo-3.php &")#,
# #                      shell=True,
# #                      close_fds=True,
# #                      stdin=subprocess.PIPE,
# #                      stdout=subprocess.PIPE)

def Load_Tag(filename):
    with open(tags_folder+filename) as file:
        tagSet=file.readlines()
    tags=[item.strip('\n') for item in tagSet]
    return tags
def my_range(start, end, step):
    while start <= end:
        yield start
        start += step
def serializeEvent (eventID, eventType,eventSource,eventLevel, eventLoc, eventCategory,timestamp):
    
    response = "@prefix geo:   <http://www.w3.org/2003/01/geo/wgs84_pos#> .\n"
    response += "@prefix sao:   <http://purl.oclc.org/NET/UNIS/sao/sao#> .\n"
    response += "@prefix tl:    <http://purl.org/NET/c4dm/timeline.owl#> .\n"
    response += "@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .\n"
    response += "@prefix prov:  <http://www.w3.org/ns/prov#> .\n"
    response += "@prefix ec:    <http://purl.oclc.org/NET/UNIS/sao/ec#> .\n"
    response += "\n"
    response += "sao:" + eventID + "\n"#uuid.uuid1().int>>64
    response += "        a                ec:" + eventType[0] + " ;\n"
    response += "        ec:hasSource     \"" + eventSource + "\" ;\n"
    response += "        sao:hasLevel     \"" + str(eventLevel) + "\"^^xsd:long ;\n"
    response += "        sao:hasLocation  [ a        geo:Instant ;\n"
    if eventLoc[0]!='NAN':
        response += "                           geo:lat  \"" + str(eventLoc[0]) + "\"^^xsd:double ;\n"
        response += "                           geo:lon  \"" + str(eventLoc[1]) + "\"^^xsd:double \n"
        response += "                         ] ; \n"
    response += "        sao:hasType      ec:" + eventCategory + " ;\n"
    response += "        tl:time          \"" + datetime.datetime.strptime(timestamp,'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%dT%H:%M:%S.0004Z') + "\"^^xsd:dateTime ."
    return response
def time_conversion(NOW,input_time):
    # Converting the Twitter Streaming local time to Aarhus time
    output_time=[datetime.datetime.strptime(i,'%Y-%m-%d %H:%M:%S') for i in input_time]
    time_dif=[x-NOW for x in output_time]
    time_dif[:]=[x.total_seconds() for x in time_dif]
    output_time[:]=[x-datetime.timedelta(seconds=3600) for x in output_time]
    formatted_output_time=[x.strftime('%Y-%m-%d %H:%M:%S') for x in output_time]
    return time_dif,formatted_output_time
def fix_SENNA_result(filename,Sleep):
    with open(filename,'r') as CNN_result, open(result_folder+city+'-trans-temporal-Tweets-CNN.txt','w') as Results:
        text1 = CNN_result.readlines()
        newline1 = ''
        for lines in text1:
            if lines.strip():
                tokens=lines.split("\t")
                if tokens[0].strip()!='"':
                    newline1 = newline1+tokens[0].strip() + ' <' + tokens[2].strip()+ '/'+ tokens[3].strip() + '> '
            else:
                if newline1:
                    newline1=newline1+'\n'
                    Results.write(newline1)
                    newline1= ''
    return 
def compute_level(temp_data,threshold):
    time_feature=np.array([ts/300.0 for ts in temp_data.TimeDif])
    loc_feature=np.array([vincenty(temp_data.Loc[i], geo_centre).miles/vincenty(city_BB[0],city_BB[1]).miles for i in range(temp_data.shape[0])])
    raduse=np.sqrt(np.power(time_feature,2)+np.power(loc_feature,2))
    temp_data.Radius= np.array(raduse <= threshold)

    grouped = temp_data.groupby(['Type', 'Radius']).groups
    tmp_df=pd.DataFrame({'Id':[],'Type':[],'Name':[] ,'Time':[],'TimeDif':[],'Loc':[], 'W':[],'Radius':[]})        
    
    level=[]
    ids_list=[]
    Gran_Level=[item.split('/') for item in list(gran_event_df.columns.values)]
    for i in range(len(grouped.values())):
        ids=grouped.values()[i]
        if temp_data.Type[ids[0]]=="TransportationEvent":
            gran_Names_ids=gran_event_df.isin(list(tmp_df.Name[ids].values)).values
            (gran_Names_rows,gran_Names_cols)=np.where(gran_Names_ids)
            # temp_data.Name[ids[0]]=Gran_Level[gran_Names_cols[0]][0]
            if gran_Names_cols:
                temp_data.set_value(ids[0],'Name',Gran_Level[gran_Names_cols[0]][0])
                level.append(int(Gran_Level[gran_Names_cols[0]][1]))
            else:
                level.append(len(ids))
        else:
            level.append(len(ids))        
        ids_list.append(ids[0])
    ids_list.sort()
    grouped_df=tmp_df.append([temp_data.loc[j] for j in ids_list], ignore_index=True)
    for gdf_index,row in grouped_df.iterrows():
        if row['W']==-1:
            # grouped_df.xs(gdf_index, copy = False)['Loc']=('','')
            grouped_df.set_value(gdf_index,'Loc',(np.inf,np.inf))
    return grouped_df,level
def get_result(NOW,trans_df,raw_df,filename1,filename2,filename3):
    with open(filename1, 'r') as CNN_result, open(filename2, 'r') as CRFD_result,open(filename3, 'r') as CRFD_Loc_result: 
        text1,text2,text3 = CNN_result.readlines(),CRFD_result.readlines(),CRFD_Loc_result.readlines()
        count1, count2, count3= len(text1),len(text2),len(text3)
    trans_text_data,raw_text_data,lat_data,long_data,time_stamp,twitterid_data= trans_df.text,raw_df.text,trans_df.lat,trans_df.long,trans_df.time,trans_df.twitterId

    with open(data_folder+city+'temporal_tweet_MV_results1.txt','w') as MV_results, open(data_folder+city+'temporal_tweet_MV_results2.txt','w') as MV_results2, open(data_folder+city+'temporal_tweet_MV_results3.txt','w') as MV_results3:

        fv,R,Type,Name,ID,TS,GL=[],[],[],[],[],[],[]
        if count1==count2:
            for line_id in range(count2):
            # print(line_id)
                token1=text1[line_id].split(' ')#CNN output
                token2=text2[line_id].split(' ')#CRF Event output
                # token1.pop(1)
                # token1.pop(2)
                CRF_Event_label=[x for i,x in enumerate(label_list) if x in text2[line_id]]
                CRF_Loc_label=[x for i,x in enumerate(Loc_label) if x in text2[line_id]]
                CNN_Loc_label=[x for i,x in enumerate(CNN_Loc_tag) if x in text1[line_id]]
                MV_labels=CRF_Event_label+CRF_Loc_label+CNN_Loc_label
                if not MV_labels:
                    MV_labels='<O>'
                MV_results_line=','.join([x for x in MV_labels])
                MV_results.write(MV_results_line)
                MV_results.write('\n')
                R.append(MV_labels)
        else:
            print('The two view files have different length. Hence, the result only relays on CRF evaluations.')
        Locations=[] 
        Weight=[]
        geolocator = Nominatim() 
        for line_id in range(count2):
            catline=text2[line_id]
            token2=catline.split(' ')#CRF Event output
            lines3=text3[line_id]
            token3=np.array(lines3.split(' '))
            if any(x in catline for x in label_list):
                label=[x for x in label_list if x in catline]
                types=[Type_list[i] for i,x in enumerate(label_list) if x in catline]
                label_id=[i for i,item in enumerate(token2) if item in label_list2]
                label_id[:] = [x - 1 for x in label_id]
                label = [x.strip('>') for x in label]
                label=[x.strip('-') for x in label]
                labels=','.join([x for x in label])
                MV_results2.write(catline+'\n')
                Type.append(types[0])#=Type+[labels]
                TS.append(time_stamp[line_id])
                ID.append(twitterid_data[line_id])
                words=' '.join([token2[x] for x in label_id])
                Name.append([words])
                tweet_geotag=(float(trans_df.lat[line_id]),float(trans_df.long[line_id]))
                if any(x in lines3 for x in ['-LOCATION>']):
                    # labels=[x for i,x in enumerate(token3) if x in label_list3]
                    label_index=[i for i,x in enumerate(token3) if x in Loc_label]
                    location_index = [x - 1 for x in label_index]
                    Location=''
                    for i in range(len(label_index)):
                        Location=Location+token3[location_index[i]]+' ' 
                        if (i<len(label_index)-1):
                            if location_index[i+1]-location_index[i]==2:
                                continue
                        else:
                            Locations=Locations+[Location]
                            Location=''
                    print(Locations)
                    locations = [geolocator.geocode(Locations[i]+" Aarhus, Denmark",timeout=10) for i in range(len(Locations))]
                    Locations=[]
                    if locations[0]:
                    #print(locations[0].address)
                            # print(location.raw)
                    #print(locations[0].raw['osm_type'],locations[0].raw['class'], locations[0].raw['type'])
                        newline3=locations[0].address+'<>'+locations[0].raw['osm_type']+'<>'+locations[0].raw['class']+'<>'+locations[0].raw['type']+'\n' 
                        print(newline3)
                        geolocation=(locations[0].latitude, locations[0].longitude)
                        distance=vincenty(geolocation, tweet_geotag).miles
                        GL.append(geolocation)
                        dist_rank=(3*distance)/20
                        if 0<=dist_rank<=1:
                            dist_rank=2
                        elif 1<dist_rank<=2:
                            dist_rank=1
                        else:
                            dist_rank=0
                        event_likelihood = distance/25.0
                        if event_likelihood>1:
                            likelihood_score=1e-05
                        else:
                            likelihood_score=1-event_likelihood
                        Weight.append(dist_rank)
                    else:
                        GL.append(tweet_geotag)
                        Weight.append(-1)
                else:
                    GL.append(tweet_geotag)
                    Weight.append(-1)
                if not R:
                    R.append(labels)
                    
            elif not R:
                R.append(['other'])
            
    dict_data={'twitterid':twitterid_data, 'raw_text':raw_text_data,'translated_text':trans_text_data,'time':time_stamp,'long':long_data,'lat':long_data,'Results':R}
    # df2 = pd.DataFrame(dict_data)
    weights=-1*np.ones(len(Name))
    if Type:
        # Level=[[x,Type.count(x)] for x in set(Type_list)]
        time_dif,formatted_time_stamps=time_conversion(NOW,TS)
        temp_data=pd.DataFrame({'Id':ID,'Type':np.array(Type),'Name':Name ,'Time':formatted_time_stamps, 'TimeDif':time_dif,'Loc':GL, 'W':Weight,'Radius':Weight})
        grouped_df,Level=compute_level(temp_data,0.1)
        dict_data2={'Id':grouped_df.Id,'Type':grouped_df.Type,'Name':grouped_df.Name ,'Time':grouped_df.Time,'Loc':grouped_df.Loc,'Level':Level, 'Weight':grouped_df.W}
    else:
        dict_data2={} 
    return dict_data2
def Check_End_of_Day(current_time,cursor):
    flag=False
    d=current_time.date()
    t=datetime.time(23,59,59)
    mid_night=datetime.datetime.combine(d,t)
    before_mid_night = mid_night -datetime.timedelta(minutes=5) 
    if before_mid_night< current_time < mid_night:
        current_time= mid_night
        # Stopping the connection with Twitter Streaming API
        #shell_cmd.kill()
        # Archiving the daily Tweet file with the date
        Archive_file=main_data_folder+city+d.strftime('%Y-%m-%d')+'.csv'
        if not os.path.isfile(Archive_file):
            os.rename(main_data_folder+city+'_daily_Tweet.csv',Archive_file)
        sql='DELETE TABLE citypulse1.AarhusTweet'
        cursor.execute(sql)
        time.sleep(20)
        time_dif=mid_night-datetime.datetime.now()
        if time_dif.total_seconds()>0:
            time.sleep(time_dif.total_seconds())
        current_time=datetime.datetime.now()
        flag=True
    return (current_time,flag)         
def load_data_from_mysqlDB(NOW,step,delay):
    
    # Connecting to mySQL DB and reading the data
    db = MySQLdb.connect(host="your mysql DB host", 
                         user="your mysql DB user name", 
                         passwd="your mysql DB pw", 
                         db="cyour mysql DB name") 
    cur = db.cursor()
    Now,ED_flag=Check_End_of_Day(NOW,cur)
    Start=Now.strftime('%Y-%m-%d %H:%M:%S')
    Stop = (Now+step).strftime('%Y-%m-%d %H:%M:%S')
    # Force the machine to sleep until the temporal data is stored in mysql DB
    time.sleep(delay)
    # For Testing: Dummy time_stamps for a testing
    # Start,Stop='2015-10-08 07:30:50','2015-10-09 21:46:33'
    print(Start,Stop)
    # Select temporal data from DB
    query1='SELECT * FROM citypulse1.AarhusTweet WHERE time BETWEEN '+ "'"+ Start+ "'"+ ' AND '+"'"+ Stop+"'"

    cur.execute(query1)
    result_set1 = cur.fetchall()
    if not result_set1:
        noData_flag=True
        return([],[],noData_flag,Now,ED_flag)
    else:
        noData_flag=False
        twitterId,temporal_tweet,Ttemporal_tweet,time_stamp,lat,long=[],[],[],[],[],[]
        for row in  result_set1:
            # print "%s, %s, %s, %s, %s" % (row[0], row[2].replace('\n', ' ').replace('\r', ''), row[3], row[4], row[5])
            twitterId.append(row[0])
            temporal_tweet.append(row[2].replace('\n', ' ').replace('\r', ''))
            time_stamp.append(row[3])
            long.append(row[4])
            lat.append(row[5])
        Ttemporal_tweet=list(gs.translate(temporal_tweet,'en'))
        # For Testing:
        # Ttemporal_tweet=temporal_tweet
        #Translated Tweet
        trans_df = pd.DataFrame({ 'twitterId' : twitterId,
                           'time' : time_stamp,
                           'text' : Ttemporal_tweet,#.str.strip('"')
                           'lat' : lat,#.str.strip('"')
                           'long' : long})#.str.strip('"')
        # Danish Tweet
        raw_df = pd.DataFrame({ 'twitterId' : twitterId,
                           'time' : time_stamp,
                           'text' : temporal_tweet,#.str.strip('"')
                           'lat' : lat,#.str.strip('"')
                           'long' : long})#.str.strip('"')
    # Close the mysql cursor object
    cur.close ()
    # Close the mysql DB connection
    db.close ()
    return(trans_df,raw_df,noData_flag,Now,ED_flag)
delay=step.total_seconds() 
start_flag=1
CRFDic_tag=Load_Tag('CRFDic_tag.txt')
CNN_NER_tag=Load_Tag('CNN_NER_tag.txt')
CRFDic_tag.pop(-1)
CNN_Loc_tag=CNN_NER_tag[:7]
LocTags=['B-LOCATION>','I-LOCATION>']+CNN_Loc_tag
label_list=["-CRIME>", "-SOCIAL>", "-CULTURAL>", "-TRAFFIC>", "-HEALTH>", "-SPORT>", "-WEATHER>","-FOOD>"]
Type_list=["CrimeEvent", "SocialEvent", "CulturalEvent", "TransportationEvent", "HealthEvent", "SportEvent", "EnvironmentalEvent","FoodEvent"]
label_list2=['<B-CRIME>', '<B-SOCIAL>', '<B-CULTURAL>', '<B-TRAFFIC>', '<B-HEALTH>', '<B-SPORT>', '<B-WEATHER>', '<B-FOOD>', '<I-CRIME>', '<I-SOCIAL>', '<I-CULTURAL>', '<I-TRAFFIC>', '<I-HEALTH>', '<I-SPORT>', '<I-WEATHER>', '<I-FOOD>']
Loc_label=[ '<B-LOCATION>','<I-LOCATION>']
gran_event_df=pd.read_csv(dictionary_folder+'GranuralDic.csv', sep="<>")

#Message Bus setting:
Host = "server IP"
Port = 8007
rabbitmqconnection, rabbitmqchannel = RabbitMQ.establishConnection(Host, Port)
# declare exchange
exchange = 'event'
topic = 'Aarhus.Twitter'

#connecting to google translate API
Timer=NOW.minute
gs = goslate.Goslate()
while start_flag:
    Sleep=0
    start = time.clock()
    loaded_data=load_data_from_mysqlDB(NOW,step,delay)
    trans_df,raw_df,noData_flag,Now,ED_flag=loaded_data[0],loaded_data[1],loaded_data[2],loaded_data[3],loaded_data[4]
    if noData_flag:
        stop=time.clock()
        processing_time=stop-start
        if processing_time.total_seconds()>60:
            delay=0
        else:
            delay=step.total_seconds() - processing_time.total_seconds()
        NOW = datetime.datetime.now() - processing_time
        continue
    indexes= trans_df.index
    headers=list(trans_df.columns.values)
    trans_df.to_csv(data_folder+city+'-trans-temporal-Tweets.csv', index=False, header=False,sep="<", encoding='utf-8')
    raw_df.to_csv(data_folder+city+'-raw-temporal-Tweets.csv', index=False,header=False, sep="<", encoding='utf-8')
    temporal_tweet, time_subset,lat_data_subset,long_data_subset=trans_df.text,trans_df.time.str.strip('"'),trans_df.lat,trans_df.long
    temporal_tweet.to_csv(SENNA_DIR+'/trans-temporal-Tweets.txt', index=False, encoding='utf-8')#,encoding='utf-8'
    # Deep learnign part:
    os.chdir(SENNA_DIR)
    sys.path.insert(0,SENNA_DIR)
    # Command line to_utf8 conversion:
    subprocess.Popen("tr -cd '\11\12\15\40-\176' < /home/citypulse/DemoComponents/CityPulseIntegration/CityPulse_Nazli/senna2/trans-temporal-Tweets.txt > /home/citypulse/DemoComponents/CityPulseIntegration/CityPulse_Nazli/senna2/trans-temporal-clean-Tweets.txt",
                     shell=True,
                     close_fds=True,
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE)


    subprocess.Popen("/home/citypulse/DemoComponents/CityPulseIntegration/CityPulse_Nazli/senna2/senna < trans-temporal-clean-Tweets.txt > trans-temporal-clean-Tweets-senna.txt",
                     shell=True,
                     close_fds=True,
                     stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE)
    sys.path.remove(SENNA_DIR)
    time.sleep(20)
    Sleep+=20
    # CRF dictionary based chuncking
    os.chdir(JAVA_DIR)
    sys.path.insert(0,JAVA_DIR)
    if os.path.isfile(data_folder+"trans-temporal-Tweets-9Dict.txt"):
        os.remove(data_folder+"trans-temporal-Tweets-9Dict.txt")
    subprocess.call('java -cp eventannotation.jar org.ccsr.datacollection.createtrainingdata.AnnotateTweetsEvents',
                        shell=True)
    if os.path.isfile(data_folder+"temporal-Tweets-Location.txt"):
        os.remove(data_folder+"temporal-Tweets-Location.txt")
    subprocess.call('java -cp eventannotation.jar org.ccsr.datacollection.createtrainingdata.AnnotateTweetsLocations',
                        shell=True)
    sys.path.remove(JAVA_DIR)

    # Multi-view Learning
    os.chdir(workingDir)
    fix_SENNA_result(SENNA_DIR+"/trans-temporal-clean-Tweets-senna.txt",Sleep)
    dict_data=get_result(NOW,trans_df,raw_df,result_folder+city+'-trans-temporal-Tweets-CNN.txt',data_folder+"trans-temporal-Tweets-9Dict.txt",data_folder+"temporal-Tweets-Location.txt")
    counter=0  
    dict_data_df=pd.DataFrame(dict_data)
    if dict_data:
        RabbitMQ.declareExchange(rabbitmqchannel, exchange, _type="topic")
        for item in dict_data_df.Type:#['Type']:
            tmp_topic=topic+'.'+item
            temporal_message=serializeEvent(dict_data_df.Id[counter], dict_data_df.Name[counter],'Twitter.Aarhus',dict_data_df.Level[counter],dict_data_df.Loc[counter], dict_data_df.Type[counter],dict_data_df.Time[counter])
            print(temporal_message)
            #temporal_message=json.dumps(tmp_dict_data, sort_keys = True)
            RabbitMQ.sendMessage(temporal_message, rabbitmqchannel, exchange, tmp_topic)
            counter+=1
    time.sleep(10)
    Sleep=Sleep+10
    stop=datetime.datetime.now()
    processing_time=stop-start
    print 'Processing time: '+ str(processing_time)
    if ED_flag:
        NOW=Now+Step
    else:
        NOW+=step
    if processing_time.total_seconds()>step.total_seconds():
        delay=0
    else:
        delay=step.total_seconds() - processing_time.total_seconds()