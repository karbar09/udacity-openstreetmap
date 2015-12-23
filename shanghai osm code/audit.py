# -*- coding: utf-8 -*-
"""
Adapted to Project 6
"""
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import requests
import sys
import unicodedata as ud
import string


OSMFILE = "shanghai_china.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

TRANSLATE_URL = "https://www.googleapis.com/language/translate/v2?q=%s&target=%s&source=%s&key=%s"
DETECT_URL = "https://www.googleapis.com/language/translate/v2/detect?q=%s&key=%s"
##YOUR GOOGLE TRANSLATE API KEY
API_KEY = "YOUR_API_KEY"


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

abbrev_mapping = { "St": "Street",
            "St.": "Street",
            "Rd.":"Road",
            "Ave":"Avenue",
            "Ave.":"Avenue"
            }
            
#Mapping misspelled words to there correct spelling
spelling_mapping = {
    "Roaf":"Road",
    "Eat":"East",
    "Rode":"Road",
    "Raod":"Road",
    "Yongkand":"Yongkang"
}

#http://wiki.openstreetmap.org/wiki/WikiProject_China#Generics_in_Chinese
pinyin_mapping = {
    "Dayuan":"Courtyard",
    "Jie":"Street",
    "Dajie":"Main Street",
    "Lu":"Road",
    "Dadao":"Avenue",
    "Xi":"West",
    "Dong":"East",
    "Nan":"South",
    "Bei":"North",
    "Zhong":"Middle",
    "Qiao":"Bridge"
}


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types

#NOT USED
#Intially, was going to apply language detection to each address, 
#before stripping away characters
#But, google charges per character, 
#and I think was not the optimal way to do this.
def detect_language(name):
    response = requests.get(DETECT_URL%(name,API_KEY))
    detect = response.json()['data']['detections'][0][0]['language']
    return detect

#Used - with default settings, translates inou
def translate_language(name,target='zh',source='en'):
    #Dictionary fo
    translated_dict = {
        "East Zhu An Bang Road":"东诸安浜路",
        "Tomson Golf Garden":"汤臣高尔夫花园",
        "Shilong Road":"石龙路",
        "Pudong Avenue":"浦东大道",
        "East Zhaohua Road":"东昭化路",
        "Yuyuan Road":"愚园路",
        "Nanjing Road":"南京路",
        "Middle Yincheng Road":"中银城中路",
        "Dapu Road":"打浦路",
        "Wensan West Road":"文三西路",
        "Xue Yuan Road":"学园路",
        "Qingyang Road (M)":"庆阳路（M）",
        "Pudong avenue":"浦东大道",
        "ZhongShangNanEr Road":"ZhongShangNanEr路",
        "Xingzhou Rd":"星洲路",
        "Gaoyou Road":"高邮路",
        "yongfu Road":"永福路",
        "fumin Road":"富民路",
        "wukang Road":"武康路",
        "Siping":"四平",
        "Wensan West Road":"文三西路",
        "Zhengli Road":"政立路",
        "Xiuyan Road":"岫岩路",
        "3999 XiuPu Road":"XiuPu路3999",
        "NO.588 binhe road":"588号滨河路",
        "ZuChongZhi Road":"祖冲之路",
        "West Ronghua Street":"西荣华街",
        "Zhongxin Road":"中兴路",
        "Wenchang Road":"文昌路",
        "S308":"S308",
        "Zhongxin Road":"中兴路",
        "Ling long Road":"灵长路",
        "Xian Xia Rd":"仙霞路",
        "BaiZhang East Road":"百丈东路",
        "QingShuiQiao Road":"QingShuiQiao路",
        "Tiyuchang Road":"体育场路",
        "Huaihai Street":"淮海街",
        "Lane 1555 Jinshajiang road(west)":"1555弄金沙江路（西）",
        "Yu Yuan Road":"愚园路",
        "Bund":"外滩",
        "106 Zhongjiang Road":"中江路106号",
        "Moyu South Road":"墨玉南路",
        "YanGao Road":"YanGao路",
        "HuanQing Road":"钟焕清路",
        "Qixin Road":"七莘路店",
        "Zhongma Road":"中马道",
        "Haigang Avenue":"海港大道",
        "Shou Ning Road":"守宁路",
        "Taian Road":"泰安路",
        "Wukang":"武康",
        "Yongfu Road":"永福路",
        "Huaihai West road Wellington garden":"淮海西路汇宁花园",
        "Chuansha Road":"川沙路",
        "Jinbang Road":"金榜路",
        "Zhizhaoju Road":"制造局路",
        "Taojiang Road":"桃江路",
        "Taihu Road":"太湖路",
        "Garden Road":"花园路",
        "Suhong Middle Road":"苏虹中路",
        "Weihai Road":"威海路",
        "West Nanjing Road":"南京西路",
        "Hong Song East Road":"香松东路"
        "Hongqiao Road":"虹桥路",
        "Wuzhong Road":"吴中路",
        "East Hongsong Road":"东红松路",
        "Ruijin Er Road":"瑞金二路",
        "Yonkand Road":"Yonkand路",
        "East Zhenchuan Road":"东震川路",
        "TongYi Road":"同益路",
        "Wuzhong Road":"吴中路",
        "Xiangyang":"襄阳",
        "Huashang Rd":"华商路",
        "Wukang Rd":"武康路",
        "Changhua Road":"昌化路",
        "Haizhou Road":"海洲路",
        "Fengxian Road":"奉贤路",
        "Wukang Road":"武康路",
        "Nandang East Road":"Nandang东路",
        "Century Avenue":"世纪大道",
        "XingHai Street":"星海街",
        "Dalian Road":"大连路",
        "Chenhui Road":"晨晖路",
        "Yejiazhai Road":"Yejiazhai路",
        "GongKang Road":"共康路",
        "Yan'an Road":"延安路",
        "Dalian Road":"大连路",
        "Dongsheng Road":"东升路",
        "Huqingping Road":"沪青平公路路",
        "Xiangyin Road, Yangpu District":"翔殷路，杨浦区",
        "Fangzhou Road":"方舟路",
        "CaoXi North Road 99":"漕溪北路99",
        "Yichang Road":"宜昌路",
        "Chengnan Road":"城南店",
        "East Da Ming Road":"东大名路",
        "Moyu South Road":"墨玉南路",
        "Huaihai Middle Road":"淮海中路",
        "Yueyang Road":"岳阳路",
        "hehuaxing":"hehuaxing",
        "Cao'an Road":"曹安路",
        "XingHai Street":"星海街",
        "Jinan Garden":"暨南花园",
        "East Hongxing Road":"东红星路",
        "Suzhou Avenue East":"苏州大道东",
        "Bibo Road":"碧波路"
    }
    if name in translated_dict:
        return translated_dict[name]
    else:
        response = requests.get(TRANSLATE_URL%(name,target,source,API_KEY))
        if response.status_code == 200:
            try:
                translated_text = response.json()['data']['translations'][0]['translatedText']
            except KeyError:
                print "Name: " + name
                print TRANSLATE_URL%(name,target,source,API_KEY)
                print response.json()
                sys.exit(0)
        else:
            print "Name: " + name
            print TRANSLATE_URL%(name,target,source,API_KEY)
            print response.json()
            sys.exit(0)
        print '"'+name+'":"'+translated_text+'"'
        return translated_text
    
#Checks if string contains any chinese characters
#Approach motivated by this stack overflow answer: 
#http://stackoverflow.com/questions/16027450/is-there-a-way-to-know-whether-a-unicode-string-contains-any-chinese-japanese-ch/16028174#16028174
#If any exceptions are thrown during decoding, in testing this was because the string contained some chinese characters. so, i return true.
def contains_chinese_chars(name):
    for n in name:
        try:
            letter_name = ud.name(unicode(n,'utf-8'))
            if letter_name.startswith('CJK UNIFIED'):
                return True
        except UnicodeDecodeError:
            return True
        except TypeError:
            return True
    return False

#Removes all ascii characters fom a string
#Used to remove the "english stuff" from a string
def strip_ascii_chars(name):
    #Check if a character is one of the ascii letters or is punctuation (to remove excess parenthesis, periods, hyphens, etc)
    #Similar to http://stackoverflow.com/a/198205/2272135
    def isAscii(s):
        for c in s:
            if c not in string.ascii_letters and c not in string.punctuation:
                return False
        return True
        
    char_array = []
    for n in name:
        if not isAscii(n):
            char_array.append(n)
    
    return "".join(n for n in char_array)
    
def repair_english_name(name):
    name_array = name.split(" ")
    ##Fix Spellings
    for key,val in spelling_mapping.iteritems():
        for i in range(0,len(name_array)):
            if key.lower() == name_array[i].lower():
                name_array[i] = val
    
    #Fix abbreviations
    for key,val in abbrev_mapping.iteritems():
        for i in range(0,len(name_array)):
            if key.lower() == name_array[i].lower():
                name_array[i] = val
    
    #Map pinyin words to english counterpart
    for key,val in pinyin_mapping.iteritems():
        for i in range(0,len(name_array)):
            if key.lower() == name_array[i].lower():
                name_array[i] = val
    
    name = " ".join(i for i in name_array if i not in string.punctuation)
    
    #Remove excess punctuation like hashbangs
    excess_punctuation = ["#"]
    for e in excess_punctuation:
        name = name.replace(e,"")
        
    return name
    
def update_name(name):
    if contains_chinese_chars(name):
        return strip_ascii_chars(name)
    else:
        return translate_language(repair_english_name(name))

def test():
    test_dict = {
        "你好":"你好",
        "南京西路 (nanjing xi road)": "南京西路",
        "Xue Dong Lu": "Xue East Road",
        "West Nanjing Roaf":"West Nanjing Road",
        "Baker Lu":"Baker Road",
        "Jindong Ave.":"Jindong Avenue",
        "Jindong Bei Dadao":"Jindong North Avenue",
        "Nanjing Xi rd.":"Nanjing West Road"
    }
    for key,value in test_dict.iteritems():      
        print key,"==>",update_name(key)
       
    #If you had an API_KEY for google translate, this is the Output 
    """
    West Nanjing Roaf ==> 南京西路
    Jindong Ave. ==> 金东大道
    南京西路 (nanjing xi road) ==> 南京西路   
    你好 ==> 你好
    Nanjing Xi rd. ==> 南京西路
    Baker Lu ==> 贝克路
    Xue Dong Lu ==> 薛东路
    Jindong Bei Dadao ==> 金东北大街
    """


if __name__ == '__main__':
    globals()['API_KEY'] = sys.argv[1]
    test()
