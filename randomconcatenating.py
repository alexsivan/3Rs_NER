#random concatenating
#SIMPLE VERSION: throughput T=2

import json
import random

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

train_fileObject = open('train_randomconcatenating.json','w',encoding='utf8')
with open('train_original.json', 'r', encoding='utf-8') as f:
    i = 0
    lines = f.readlines()
    while i!=len(lines):
        location = []
        org_name = []
        person_name = []
        
        
        json_line1 = json.loads(lines[i].strip())
        #print(json_line1['label'])
        text1 = json_line1['text']
        #replace this entity type into your entity type 
        if 'LOC' in json_line1['label'].keys():
                location = location+list(json_line1['label']['LOC'].keys())
        if 'ORG' in json_line1['label'].keys():
                org_name = org_name+list(json_line1['label']['ORG'].keys())
        if 'PER' in json_line1['label'].keys():
                person_name = person_name+list(json_line1['label']['PER'].keys())
        
        json_line2 = json.loads(lines[i+1].strip())
        #print(json_line2['label'])
        text2 = json_line2['text']
        if 'LOC' in json_line2['label'].keys():
                location = location+list(json_line2['label']['LOC'].keys())
        if 'ORG' in json_line2['label'].keys():
                org_name = org_name+list(json_line2['label']['ORG'].keys())
        if 'PER' in json_line2['label'].keys():
                person_name = person_name+list(json_line2['label']['PER'].keys())
       
                
        #print('textoriginal:'+text1+text2)
        text_sample = text1.split('，')[-1]+text2.split('，')[0]
        
        j = {'text':text_sample,'label':{}}
        #print('textsample:'+text_sample)
        
        loc_sample = []
        org_sample = []
        per_sample = []
        
        for l in location:
            if l in text_sample:
                loc_sample.append(l)
        for o in org_name:
            if o in text_sample:
                org_sample.append(o)
        for p in person_name:
            if p in text_sample:
                per_sample.append(p)
        
                
         #replace this entity type into your entity type 
        
        j['text'] = text_sample
        
        if len(loc_sample)!=0:
            d_loc = {}
            for ll in loc_sample:
                if find_all(ll,text_sample)!=-1:
                    d_loc.update({ll:find_all(ll,text_sample)})
                    j['label'].update({'LOC':d_loc})  
        if len(org_sample)!=0:
            d_org = {}
            for oo in org_sample:
                if find_all(oo,text_sample)!=-1:
                    d_org.update({oo:find_all(oo,text_sample)})
                    j['label'].update({'ORG':d_org})  
        if len(per_sample)!=0:
            d_per = {}
            for pp in per_sample:
                if find_all(pp,text_sample)!=-1:
                    d_per.update({pp:find_all(pp,text_sample)})
                    j['label'].update({'PER':d_per})  
       
        
        i=i+2
        if len(text_sample)<101 and j['label']!={} : # and len(j['label'].keys())!=0:
            print(j)
            jsObj = json.dumps(j,ensure_ascii=False)+'\n'
            train_fileObject.writelines(jsObj)