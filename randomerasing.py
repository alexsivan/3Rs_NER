#random erasing
#SIMPLE VERSION: throughput T=2

import json
import random

import jieba  
import jieba.posseg
import jieba.analyse
import pandas as pd

def pos_sentence(sentence):
    sentence_seged = jieba.posseg.cut(sentence)
    outstr_verb = []
    outstr_noun = []
    
    for x in sentence_seged:
        if x.flag=='v' and len(str(x.word))>1:
            outstr_verb.append(str(x.word))
        if x.flag=='n' and len(str(x.word))>1:
            outstr_noun.append(str(x.word))
    return outstr_verb, outstr_noun

def Merge(dict1, dict2): 
    res = {**dict1, **dict2} 
    return res 

def find_all(sub,s):
	index_list = []
	index = s.find(sub)
    
	while index != -1:
		index_list.append([index,index+len(sub)-1])
		index = s.find(sub,index+1)
	
	if len(index_list) > 0:
		return index_list
	else:
		return -1

def findnoun(sentence,entity_list):
    sentence_ori = sentence
    for e in entity_list:
        sentence = sentence.replace(e,'')
    #print(sentence)
    sentence_seged = jieba.posseg.cut(sentence)
    outstr_noun = []
    
    for x in sentence_seged:
        if x.flag=='n':
            outstr_noun.append(str(x.word))
                
    for nn in outstr_noun:
        for e in entity_list:
            if bool([a for a in e if a in nn]):
                outstr_noun = list(set(outstr_noun).difference(set([nn])))       

    return outstr_noun

#words_dict = {'ORG':[], 'LOC':[], 'PER':[],'GPE':[]}
train_fileObject = open('train_randomerasing-new.json','w',encoding='utf8')
with open('train_original.json', 'r', encoding='utf-8') as f:
    i = 0
    lines = f.readlines()
    while i!=len(lines):
        json_line1 = json.loads(lines[i].strip())
        raw_text1 = json_line1['text']
        entity_list1 = []
        if 'label' in json_line1.keys():
            for labelkey in json_line1['label'].keys():
                entity_list1 += list(json_line1['label'][labelkey].keys())
        
        json_line2 = json.loads(lines[i+1].strip())
        raw_text2 = json_line2['text']
        entity_list2 = []
        if 'label' in json_line2.keys():
            for labelkey in json_line2['label'].keys():
                entity_list2 += list(json_line2['label'][labelkey].keys())
        
        raw_text = raw_text1+raw_text2
        entity_list = entity_list1+entity_list2
        j = {'text':raw_text,'label':{}}
        raw_text_before = raw_text
        #print(1)
        #print(entity_list)
        noun =  findnoun(raw_text,entity_list)
        #print(2)
        if len(noun)>3:
            erase = random.sample(noun,2)
        elif len(noun)<3 and len(noun)>0:
            erase = random.sample(noun,1)
        else:
            erase = []
        if len(erase)!=0:
            for er in erase:
                raw_text = raw_text.replace(er,'') 
        if raw_text==raw_text_before:
            i=i+2
            continue
        #
        
        #replace this entity type into your entity type 
        if 'label' in json_line1.keys() or 'label' in json_line2.keys():
            if 'ORG' in json_line1['label'].keys() or 'ORG' in json_line2['label'].keys():
                org_list = []
                if  'ORG' in json_line1['label'].keys() :
                    org_list =org_list+ list(json_line1['label']['ORG'].keys())
                if  'ORG' in json_line2['label'].keys() :
                    org_list =org_list+ list(json_line2['label']['ORG'].keys())
                d_org = {}
                if len(org_list)>1:
                    for org_s in org_list:
                        if find_all(org_s,raw_text)!=-1:
                            d_org.update({org_s:find_all(org_s,raw_text)})
                    j['label'].update({'ORG':d_org})  
                            
            if 'LOC' in json_line1['label'].keys() or 'LOC' in json_line2['label'].keys():
                loc_list = []
                if 'LOC' in json_line1['label'].keys():
                    loc_list =loc_list+ list(json_line1['label']['LOC'].keys())
         
                if 'LOC' in json_line2['label'].keys():
                    loc_list =loc_list+ list(json_line2['label']['LOC'].keys())
                 
                d_loc = {}
                if len(loc_list)>1:
                    for loc_s in loc_list:
                        if find_all(loc_s,raw_text)!=-1:
                            d_loc.update({loc_s:find_all(loc_s,raw_text)})
                    j['label'].update({'LOC':d_loc})  
                            
            if 'PER' in json_line1['label'].keys() or  'PER' in json_line2['label'].keys():
                per_list = []
                if 'PER' in json_line1['label'].keys():
                    per_list  =per_list+ list(json_line1['label']['PER'].keys())
                 
                if 'PER' in json_line2['label'].keys():
                    per_list  =per_list+ list(json_line2['label']['PER'].keys())
                 
                d_per = {}
                if len(per_list)>1:
                    for per_s in per_list:
                        if find_all(per_s,raw_text)!=-1:
                            d_per.update({per_s:find_all(per_s,raw_text)})
                    j['label'].update({'PER':d_per})  
           
            j['text'] = raw_text
            if j['label']!={} and len(j['text'])<150:
                print(j)
                jsObj = json.dumps(j,ensure_ascii=False)+'\n'
                train_fileObject.writelines(jsObj)
        i=i+2
