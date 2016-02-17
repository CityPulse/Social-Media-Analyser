- Essential python libraries ofr the code: 
1) numpy 
2) pandas

Note: if you are using python 3.2 or upper please make the following change: from tkinter import * -> from Tkinter import *

Provided Tweets format in the GUI:
- Please ignore the number which you see at the beginig of each tweet as it is just a id number
- The word taggs provided in each tweet (part of text incompassed in '<>' signs) are solely to give knowlage about location terms and event terms which you might not be aware of. Be careful not to let them confuse you as in some cases they might not be reliable but many cases you will find them quite helpful specially if you are not familier with all London locations and public events.

General notes:
- Please select relevent classes for each tweets form the 10 provided categories; Food, Crime, Weather, sport ... (Think of these categories as refering to event which might actually affect the city traffic pattern) 
- The 'Other' class is an indicator of a non-event tweet which 1) its content can not be clustered as any of the provided classes (i.e. personal messages and opinion sharing), 2) has irrelevent and hard to understand content (whatever is hard to understand which can be even a text written in a language other than English)
- The 'Location' class as its name inferes is the class where in text you can detect a location reference. Due to ambiguity of tweets, it is highly possible you can guess an event occurance in a specific location while the type of event can not clearly be resolved. In these occurances pleas just choose the 'Location' class. Obviousely, you can select this class along with other classes for the same tweet as it will provide the actual event location.
- The 'Social' class is the class which includes voting, election, protest and other city related group activities
- Apart fro mthe 'Location' class, please make sure not to make joint selection of other classes unless it is nessecary
- Please do not forget to 'save' your annotation 
- While selecting classes for each tweet, please take note of the words which you belive they should have been tagged as a specific class but their current tag is missing this data.

Extra important notes:
- Please make sure that you actually detect a location term/word/phrases and do not soley rely on the '@' sign as in many cases it might not be place and instead it refers to another twitter user id
- Please ignore your multi-lingual abilities unless there is a common English word within the text 
- It is possible to choose multiple classes for the same tweet but it is not recommended as it will complicate the post processing steps.   
- Please inform me of the amount (quantity) of tweets which you will be able to annotate within 2 weeks time ASAP
