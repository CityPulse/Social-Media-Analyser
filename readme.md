# Version 1.0 Twitter Data collection and Processing


## Description

A Python wrapper for a live twitter NLP processing: 
The CityPulse IoP data processing component is composed of a dedicated Data wrapper in php (DataCollection_Phirehose-master) unit which connects to the Twitter stream API and google translate API to simultanousely collect the data under the form of tweets and to automatically detect the source language and translate the tweets to English to facilitate the data processing step; and a data processing unit which is composed of three sub-components: a Conditional Random Field Name Entity Recognition (see below), a deep learning Convolutional Neural Network for Part of Speech tagging (see below), and a multi-view event extraction which combines the information extracted from the previous sub-components. Given a tweet and its translation, the processing unit assigns it to one of the event classes from the pre-defined class set: {Transportation and Traffic, Weather, Cultural Event, Social Event, Sport and Activity, Health and Safety, Crime and Law, Food and Drink}. 

A web interface is developed which facilitates the visualisation of the extracted city events on a Google map in near real-time. The interface is composed of (a) Google map canvas layer on which the processed and annotated Tweets are displayed with their class-identical icons (b) a live London traffic layer from google traffic API - code coloured paths on the map (c) a bar chart panel which presents the class distribution histogram of daily Tweets and (d) a panel for displaying Twitter timeline. (note: The map interface code is not included in this package)

The map data is updating in 60s time windows by adding the past minute's Tweets to existing ones upto a 60-minutes time window. In practice, the whole data will be updated on hourly bases. Clicking on each event a dialogue box is shown on the map which 	reveals the underlying Tweet content along with its time-stamp. The twitter user id and the name are anonymised for privacy purpose.

The web interface utilises javascript and html coding and reads the annotated data from a CSV rest file of the live NLP processing component.


## System requirements
- Java compiler
- C++ compiler
- Pyton 2.7 or hihgher
- mysql 
- php
- mysql php connector

    
## Dependencies
Data colloction unit requires a mysql database of the following schema to be constructed prior to collection:
	```
	CREATE TABLE `AarhusTweet` (
     `twitterstream` VARCHAR(100) NOT NULL,
     `userid` VARCHAR(100) NOT NULL,
     `text` VARCHAR(500) NOT NULL,
     `time` VARCHAR(100) NOT NULL,
     `lat` VARCHAR(100) NOT NULL,
     `long` VARCHAR(100) NOT NULL,
     `boundingbox` VARCHAR(400) NOT NULL,
    ) ENGINE=MyISAM DEFAULT CHARSET=latin1;
	```
The package needs the senna C++ Convolutional Neural Network package to be installed in the main directory from: 

http://ronan.collobert.com/senna/

It also requires Conditional random field NER tagger which can be downloaded from: 

http://personal.ee.surrey.ac.uk/Personal/N.Farajidavar/Downloads.html

Python package dependencies: Pandas, mysql, matplotlib, pylab, geopy, goslate, pika, rabbitmq

## Running/Usage
Once the dependencies mentioned above are installed, need to run the main code in Python:
	``` python Aarhus_v4.py	```

## Acknowledgments
- Ronan Collobert for his CNN C++ package
- Alias-i for the Conditional Random Field Java package 
- This work has been carried out in the scope of the European Commission’s Seventh Framework Programme funded project CityPulse (FP7	    -609035).

    
## Contact

mailto:n.davar@surrey.ac.uk
http://personal.ee.surrey.ac.uk/Personal/N.Farajidavar/Downloads.html
https://github.com/CityPulse/Twitter

Nazli Davar
ICS, University of Surrey,
Guildford
GU2 7UZ
UK

# Distribution

The original zipfile can be freely distributed, by any means.  However,
I would like to be cited in case if it is used:

Modified versions may be distributed, provided it is indicated as such
in the version text and a source diff is made available.  

==============================
17 Feb, 2016.
