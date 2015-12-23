#OpenStreetMap Data Wrangling with MongoDB
Author: Karthik Rajasethupathy
Map Area: [Shanghai, China http://www.openstreetmap.org/relation/913067]

#Why Shanghai?
I am currently living in China. I am not fluent in mandarin, but I can recognize some basic characters (such as street types), and thought it would be interesting to see what kind of inconsistencies and localization problems might arrise in this data.

#Problems Encountered
There are many issues with this dataset. To simplify the task, I focused on the street naming conventions and found three classes of issues:

    1. Malformed Street Names
            <tag k="addr:street" v="3"/> --> This is not a street name
    2. Mispellings and Abbreviations
            <tag k="addr:street" v="Wukang Roaf"/> --> "Wukang Road"
            <tag k="addr:street" v="Haigang Ave."/> --> "Haigang Avenue"
    3. Pinyin spelling of Chinese Words
            <tag k="addr:street" v="Nandang Dong Lu"/>  --> "Nadang East Road", Dong = East and Lu = Road!
            <tag k="addr:street" v="Suzhou Dadao Dong"/> --> "Suzhou Avenue East", Dadao = Avenue and Dong = East
    4. Removing Excess Punctuation
            For consistency, changing numbers from #399 -> 399
    5. Street address (addr:street) is sometimes in chinese, sometimes in english, and sometimes in both languages. 
            <tag k="addr:street" v="南期昌路"/>
            <tag k="addr:street" v="Weihai Road"/>
            <tag k="addr:street" v="仙霞西路 (Xianxia West Rd)"/>
            Is this a mistake? If so, which cases are correct?
    

##Malformed Streets
    Here are two (not infrequent) values that provided for the addr:street key.
        "S308"
        "3"
    I deal with this by skipping this tag when building the json file the osm file.

##Mispellings and Abbreviations
    Similar to project 6, there are many abbreviations and misspelled street names (Roaf, Rode, Raod -> Road). It could be possible to do some fuzzy matching, but I went with the direct search and replace.
    For abbreviations, I used the same approach as what we used in project 6, and simply added a couple of frequently used abbreiviations to the mapping dictionary.

##Pinyin Spelling of Chinese words
    This is an interesting case. Often times, the chinese pinyin of a word is written in the english street name. For example: Yongkang __Lu__ instead of Yongkang __Road__. On the osm street wiki, i found a list of chinese generics for street mappings and made a mapping dictionary for these names (see http://wiki.openstreetmap.org/wiki/WikiProject_China#Generics_in_Chinese).

##Removing Excess Punctuation
    No further explanation

##Street Address
    I first checked the openstreetmap wiki pages to see what the naming convention is for areas where localization is an issue. Specifically, for China, I came across the following document: http://wiki.openstreetmap.org/wiki/Multilingual_names#China
    From the above link, we can see that a standard entry is typically like this (I cannot gaurantee that this is the agreed upon consensus, but most contributors seem to follow this schema):
        name=<Chinese>
        name:zh=<Chinese>
        name:en=<English>
        name:zh_pinyin=<Chinese pinyin (with tones)>
    So, the way I wanted to treat this issue is to do the following. 
            <tag k="addr:street" v="南期昌路"/> -> Correct, leave it
            <tag k="addr:street" v="Weihai Road"/> -> Translate to Chinese
            <tag k="addr:street" v="Nandang Dong Roaf"/> -> Convert pinyin (Dong-> East), Fix spellings (Roaf -> Road), translate to Chinese
            <tag k="addr:street" v="仙霞西路 (Xianxia West Rd)"/> -> Keep chinese, remove english
###Approach
    Given: 
        1. An addr:street value v (the base value, addr:street, not addr:street:*) 
        2. A language translation tool (I made an account with google translate api)
    
    Algorithm:
        1 If string contains chinese characters
            1.1 remove all english characters from string -> return result.
        2 Else 
            2.1 Correct spellings (Roaf - > Road)
            2.2 Fix abbreviations (Ave. -> Avenue)
            2.3 Map pinyin spellings to english  (Dong -> East)
            2.4 Remove excess punctuation from String (#3999 Something Road -> 3999 Something Road)
            2.5 Translate processed english string to chinese -> return result
###Explanation
    So, I want to first check if there are any chinese (going with a broad definition here: non-roman) characters in the string. If so, I'm going to assume that the chinese characters do fully represent the street address. Then, once again, I clean the string of the "english stuff". This assumption satisfies 99% of mixed language cases in this dataset. But, I do acknowledge that it is not a foolproof approach to dealing with mixed strings. 
    In case 2, we have a string that contains no chinese characters. Here, I fix spellings, fix abbreviations, map pinyin to english, and remove some excess punctuation, then translate the processed string through the google translate api. The result will replace the original string. Once again, this is not foolproof if the pinyin for the streetname is wrong. 
    If fact, there are 2 cases that this approach fails to address:

        1. No spaces between psuedo - pinyin:
            [Pinyin should have the tone information, most pinyin i see in this dataset does not contain tonal info, hence, i call this psuedo-pinyin.] 
            Sometimes, pinyin has spaces, and sometimes the pinyin has no spaces between characters, e.g.: nihao vs. ni hao
            Google translate api doesn't always deal with no space pinyin (NSP) well. For example:
            A. 
                Actual: ZhongShangNanEr Road -> Google Translate Api -> ZhongShangNanEr路
                Ideally: ZhongShangNanEr Road -> Google Translate Api -> 中商南二路
                What we need: ZhongShangNanEr Road -> (?) Zhong Shang Nan Er Road -> Google Translate Api -> 中商南二路
            B. However, in some other cases, Google takes care of this.
                Actual: BaiZhang East Road -> Google Translate Api -> 百丈东路
            
            Case A is not handled well. Case B is handled well. I am not sure how to address case A. But, I acknowledge it's an issue and we may need a library that can break up pinyin in an appropriate way.
            
        2. Mispelled pinyin:  
            Yonkand Road -> Google Translate Api -> Yonkand路
            Now, I know the contributor actually meant to write Yongkang Road, instead of Yongkand Road. These cases need to be addressed on a case by case basis.
        

#Data Overview
    > File Sizes:
        shanghai_china.osm - 485.4 mb
        shanghai_china.osm.json - 527.8 mb
    
    ##Number of Documents
    > db.shanghai_osm.count()
    2422310
    
    ##Number of Nodes
    > db.shanghai_osm.find({type:"node"}).count()
    2166547

    ##Number of Ways
    > db.shanghai_osm.find({type:"way"}).count()
    255451    


#Additional Ideas
    Some Idea
    Extra Queries
    Conclusion


#Important Queries:

db.shanghai_osm.aggregate([{"$group":{_id:"$address.street",total:{"$sum":1}}},{"$sort":{"total":1}}]);
db.shanghai_osm.find({'address.street':{"$exists":1}}).pretty()
db.shanghai_osm.aggregate([{"$match":{"type":{"$exists":1}}},{"$group":{_id:"$created.user",total:{"$sum":1}}},{"$sort":{"total":1}}])