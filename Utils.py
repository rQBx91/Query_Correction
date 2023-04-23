import os
import xml.etree.ElementTree as ET
from Document import Document_Object
from tqdm import tqdm
import json
from InMemIndex import InMemIndex

scriptPath = os.getcwd()

def Build(Index: InMemIndex) -> None:

    loadFromJSON(Index, scriptPath+'/resources/DocumentStore.json')
    Index.buildVocab()
    Index.store2Disk(scriptPath+'/resources/Index.pickle')
    Index.store2DiskFreq(scriptPath+'/resources/FrequencyIndex.pickle')
    Index.store2DiskVocab(scriptPath+'/resources/VocabularyIndex.pickle')

def Load() -> InMemIndex:
    Index = InMemIndex()
    Index.loadFromDisk(scriptPath+'/resources/Index.pickle') 
    Index.loadFromDiskFreq(scriptPath+'/resources/FrequencyIndex.pickle')
    Index.loadFromDiskVocab(scriptPath+'/resources/VocabularyIndex.pickle')
    return Index

def checkIndex():
    if os.path.exists(scriptPath+'/resources/Index.pickle') and\
          os.path.exists(scriptPath+'/resources/FrequencyIndex.pickle') and\
              os.path.exists(scriptPath+'/resources/VocabularyIndex.pickle'):
        return True
    return False

def FormatSuggestions(sugguestions:list, N:int) -> str:
    result = ''
    if sugguestions == None:
        return 'No result found'
    for i,item in enumerate(sugguestions):
        if i == N:
            break
        confidence = "{:.3f}".format(item[1]*100)
        result += f'sugguestions: {item[0]} --> confidence: {confidence}%\n'
        i += 1
    return result

def parseXML(path, count=-1):
    dict = {}
    if count == -1:
        print('Parsing XML as tree: ', end='')
        xml_tree = ET.parse(path)
        xml_root = xml_tree.getroot()
        print('Done')

        print('Get tree lenght: ', end='')
        lenght = 0
        for item in xml_root.iter('doc'):
            lenght += 1
        print('Done')

        xml_root = xml_tree.getroot()
        cnt = 0
        for item in tqdm(xml_root.iter('doc'), desc='Parsing XML file', total=lenght ):
            dict[cnt] = [item[0].text, item[1].text, item[2].text]
            cnt += 1
    
    elif count > 0:
        print('Parsing XML as tree: ', end='')
        xml_tree = ET.parse(path)
        xml_root = xml_tree.getroot()
        print('Done')

        print('Get tree lenght: ', end='')
        lenght = 0
        for item in xml_root.iter('doc'):
            lenght += 1
        print('Done')

        xml_root = xml_tree.getroot()
        cnt = 0
        for item in tqdm(xml_root.iter('doc'), desc='Parsing XML file', totoal=lenght):
            if cnt >= count:
                break
            dict[cnt] = [item[0].text, item[1].text, item[2].text]
            cnt += 1

    return dict


def loadFromJSON(Index: InMemIndex ,path):
        with open(path, 'r', encoding='utf8') as jsonFile:
            print('Parsing JSON file: ', end='')
            jsonDict = json.loads(jsonFile.read())
            print('Done')
            docList = []
            for id in tqdm(jsonDict, desc='Building Index from JSON file'):
                abstract = jsonDict[id]['abstract']
                if abstract == None:
                    abstract = ''
                doc = Document_Object(int(id), jsonDict[id]['title'], jsonDict[id]['url'], abstract)
                Index.addDoc(doc)
            
