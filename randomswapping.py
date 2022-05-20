#random swapping
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

def partofentity(entity,entity_list):
    for e in entity_list:
            if bool([a for a in e if a in entity]):
                return True
    return False

train_fileObject = open('train_randomswapping.json','w',encoding='utf8')
with open('train-origin.json', 'r', encoding='utf-8') as f:
    i = 0
    lines = f.readlines()
    
    while i!=len(lines):
        
        json_line1 = json.loads(lines[i].strip())
        json_line1_old = json_line1
        raw_text1 = json_line1['text']
        entity_list1 = []
        j1_keys = list(json_line1_old['label'].keys())
        
        if 'label' in json_line1.keys():
            for labelkey in json_line1['label'].keys():
                entity_list1 += list(json_line1['label'][labelkey].keys())
            #entity type that perform badly
            if 'LOC' in json_line1['label'].keys():
                loc_list1 = list(json_line1['label']['LOC'].keys())       
        
        json_line2 = json.loads(lines[i+1].strip())
        json_line2_old = json_line2
        raw_text2 = json_line2['text']
        entity_list2 = []
        j2_keys = list(json_line2_old['label'].keys())
         
        
        if 'label' in json_line2.keys():
            for labelkey in json_line2['label'].keys():
                entity_list2 += list(json_line2['label'][labelkey].keys())
            #entity type that perform badly
            if 'LOC' in json_line2['label'].keys():
                loc_list2 = list(json_line2['label']['LOC'].keys())
                #print(loc_list2)
           
        #print('=========================================')
        #print(raw_text2)
        #processing sentence2
        #print(json_line2)
        if 'LOC' in j1_keys:
            #print(json_line2)
            loc_swap = random.choice(loc_list1)
            #print(loc_swap)
            span_length = len(loc_swap)
            if span_length<len(raw_text2):
                b_index2 = random.randint(0,len(raw_text2)-span_length-1)
                count=30
                while partofentity(raw_text2[b_index2:b_index2+span_length],entity_list2) and count>0:
                    b_index2 = random.randint(0,len(raw_text2)-span_length-1)
                    count=count-1
                raw_text2 = raw_text2.replace(raw_text2[b_index2:b_index2+span_length],loc_swap)
                #print(entity_list2)
                #print(raw_text2)

                json_line2['text']=raw_text2
                if 'LOC' in json_line2['label'].keys():
                    if raw_text2[b_index2:b_index2+span_length] not in entity_list2:
                        json_line2['label']['LOC'].update({raw_text2[b_index2:b_index2+span_length]:[[b_index2,b_index2+span_length-1]]})
                    else:
                        try:
                            json_line2['label']['LOC'][raw_text2[b_index2:b_index2+span_length]].append([b_index2,b_index2+span_length-1])
                        except:
                            print('error')
                elif 'LOC' not in json_line2['label'].keys():
                    json_line2['label'].update({'LOC':{raw_text2[b_index2:b_index2+span_length]:[[b_index2,b_index2+span_length-1]]}})
                if json_line2['label']!={} and len(json_line2['text'])<150:
                    jsObj = json.dumps(json_line2,ensure_ascii=False)+'\n'
                    print(json_line2)
                    train_fileObject.writelines(jsObj)
                
                #print('=========================================')
        #print(json_line2_old['label'].keys())
        #print(j2_keys)
        if 'LOC' in j2_keys:
            #print(json_line2)
            loc_swap = random.choice(loc_list2)
            #print(loc_swap)
            span_length = len(loc_swap)
            if span_length<len(raw_text1):
                b_index1 = random.randint(0,len(raw_text1)-span_length-1)
                count=30
                while partofentity(raw_text1[b_index1:b_index1+span_length],entity_list1) and count>0:
                    b_index1 = random.randint(0,len(raw_text1)-span_length-1)
                    count=count-1
                raw_text1 = raw_text1.replace(raw_text1[b_index1:b_index1+span_length],loc_swap)
                #print(entity_list2)
                #print(raw_text2)

                json_line1['text']=raw_text1
                if 'LOC' in json_line1['label'].keys():
                    if raw_text1[b_index1:b_index1+span_length] not in entity_list1:
                        json_line1['label']['LOC'].update({raw_text1[b_index1:b_index1+span_length]:[[b_index1,b_index1+span_length-1]]})
                    else:
                        try:
                            json_line1['label']['LOC'][raw_text1[b_index1:b_index1+span_length]].append([b_index1,b_index1+span_length-1])
                        except:
                            print('error')
                elif 'LOC' not in json_line1['label'].keys():
                    json_line1['label'].update({'LOC':{raw_text1[b_index1:b_index1+span_length]:[[b_index1,b_index1+span_length-1]]}})
                if json_line1['label']!={} and len(json_line1['text'])<150:
                    jsObj = json.dumps(json_line1,ensure_ascii=False)+'\n'
                    print(json_line1)
                    train_fileObject.writelines(jsObj)
        i=i+2
        #print(i)