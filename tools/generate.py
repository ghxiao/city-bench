#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getopt, sys
import optparse
import psycopg2
import shlex, subprocess
import collections
import os
import imp
from abc import ABCMeta

import spatialRelationsReader

KeyValue = collections.namedtuple('KeyValue', ['key', 'value'])

# Different dictionaries for connections, files, scripts
dictConnections = {}
dictFiles = {}
dictScripts = {}
dictConstants = {}
listMappings = []


class Mapping:

    id = ""
    mapType = 0
    sourceId = ""
    sourceQuery = ""

    transformId = ""
    transformQuery  = ""

    targetId = ""
    targetOutput = ""
    
    dependency = ""

    def __init__(self, id):
        self.id = id
    
    def display(self):
        print "Id: ", self.id
        print "Source: ", self.sourceId, self.sourceQuery
        print "Transform: ", self.transformId, self.transformQuery
        print "Target: ", self.targetId, self.targetOutput


# Base class for a reader
class Reader:  #__metaclass__ = ABCMeta

    connectionString = ""
    mapObj = None

    #@property
    #def mapObj(self):
    #    return self.__mapObj
    
    def __init__(self, mapping, connection):
        self.mapObj = mapping
        self.connectionString = connection
    

    def open(self):
        # Here comes the open. This does not always be overriten
        a = 0

    def read(self):
        # Here comes the read and yield
        raise NotImplementedError

    def close(self):
        # Here comes the close. This does not always be overriten
        a = 0
        

class FileReader(Reader):


    sepChar = ''
    fileName = ""

    @staticmethod
    def extractFileNameSeparator(fileString):
        # 2 cases with delimiter or without
        posName = fileString.find("name=")
        posSep = fileString.find("delimiter=")
        sepCharRet = ''
        fileNameRet = ""
        
        if posSep < 0:
            fileNameRet = fileString[(posName+5):]
        else:
            fileNameRet = fileString[(posName+5):(posSep-1)]
            sepCharRet = fileString[(posSep+11):(posSep+12)]

        return (fileNameRet, sepCharRet)

                
    def open(self):
        
        (name, sep) = FileReader.extractFileNameSeparator(self.connectionString)
        self.fileName = name
        self.sepChar = sep

    
    def read(self):
        
        with open(self.fileName, 'r') as f1:

            lines = f1.readlines()
            for i in range(len(lines)):
                tuple_file = lines[i]
                if posDel > -1:
                    yield (tuple_file,) #  
                else:
                    tempList = tuple_file.split(sepChar)
                    tuple_sep = tuple(tempList)
                    yield tuple_sep
                #print tuple_file

        f1.closed

#def close():
         

class DatabaseReader(Reader):

    conn_gis = None
    cur_gis = None
    
    def open(self):

        # Connect to a PostGIS database and open a cursor to perform database operations
        self.conn_gis = psycopg2.connect(self.connectionString)
        # Set DB parameter
        self.conn_gis.set_client_encoding('UTF8')
        self.cur_gis = self.conn_gis.cursor()

        
    def read(self):

        self.cur_gis.execute(self.mapObj.sourceQuery)
        
        for tuple_gis in self.cur_gis:

            #tupleOut = self.mapObj.targetOutput
            
            yield tuple_gis

    def close(self):

        self.cur_gis.close()
        self.conn_gis.close()

        
class ScriptReader(Reader):

    scriptReader  = None

    def open(self, input):

        self.scriptReader = ScriptReader.load_from_file(self.connectionString, "CustomScriptReader")
        self.scriptReader.open(input)
 
        
    def read(self):
        
        for line in self.scriptReader.read():
            yield  line
            

    def close(self):

        scriptReader.close()
    
    @staticmethod    
    def load_from_file(filepath, expected_class): # self, 
        class_inst = None

        mod_name,file_ext = os.path.splitext(os.path.split(filepath)[-1])
        #sReader = spatialRelationsReader.CustomScriptReader()
        
        #if os.path.exists(filepath):
        #print "Exists"
        
        if file_ext.lower() == '.py':

            py_mod = imp.load_source(mod_name, filepath)

        elif file_ext.lower() == '.pyc':
            py_mod = imp.load_compiled(mod_name, filepath)

        if hasattr(py_mod, expected_class):
            class_inst = getattr(py_mod, expected_class)()

        return class_inst


class ConstantReader(Reader):

    listIDs = []
    constants = {}
    
    def __init__(self, mapping, consts):

        self.mapObj = mapping
        self.constants = consts
        #self.connectionString = connection
        #print consts
 
    def open(self):

        self.listIDs = self.mapObj.sourceQuery.split(' ')
    
    def read(self):

        for index in range(len(self.listIDs)):
            yield (self.constants[self.listIDs[index]],)
            

# Base class for a writer
class Writer:

    connectionString = ""
    mapObj = None

    def __init__(self, mapping, connection):
        self.mapObj = mapping
        self.connectionString = connection

    def open(self):
		# Here comes the open. This does not always be overriten
		a = 0            
    def write(self, tuple):
		# # Here comes the write.
		raise NotImplementedError
		     
    def close(self):
		# Here comes the close. This does not always be overriten
		a = 0        
        
class FileWriter(Writer):

    textfile = None
    fileName = ""
    sepChar = ''
        
    def open(self):
        
        (name, sep) = FileReader.extractFileNameSeparator(self.connectionString)
        self.fileName = name
        self.sepChar = sep
                    
        self.textfile = open(self.fileName, 'a') # w+

    def write(self, tuple):
        
    	try:
        	self.textfile.write(tuple + '\n')

        except Exception, e:
            print e
        

    def close(self):

        self.textfile.closed

class ConsoleWriter(Writer):

	def __init__(self):
		# Nothing to do
		a = 0

	def write(self, tuple):
    	
		print tuple


class DatabaseWriter(Writer):

    conn_gis = None
    cur_gis = None

    def open(self):

        # Connect to a PostGIS database and open a cursor to perform database operations
        self.conn_gis = psycopg2.connect(self.connectionString)
        # Set DB parameter
        self.conn_gis.set_client_encoding('UTF8')
        self.cur_gis = self.conn_gis.cursor()
            
    def write(self, tuple):
        try:
        	#print tuple
        	self.cur_gis.execute(tuple)
        	self.conn_gis.commit()

        except Exception, e:
            print e

    def close(self):

        self.cur_gis.close()
        self.conn_gis.close()
    
        
def main(argv):

    # Parse command line input
    parser = optparse.OptionParser()
    parser.add_option('--mappingFile', action="store", dest="mapFile", default="")
    parser.add_option('--verbose', action="store_true", dest="verbose", default=False)
    (options, args) = parser.parse_args()

    # Read config file
    with open(options.mapFile, 'r') as f1:
        lines = f1.readlines()

        createConnections(lines)
        createMappings(lines)

    f1.closed

    # Loop Mapping and run them
    for i in range(len(listMappings)):
        mapObj = listMappings[i]
        #mapObj.display()

        runMapping(mapObj)

def runMapping(mapObj): 

    fileName = ""
    dataWriter = None
    dataReader  = None

    # Main method for ETLing the data
    print "Transfering " +  mapObj.id
    
    # Create DB/File/Script reader (extract)
    if mapObj.sourceId in dictConnections:

        dataReader = DatabaseReader(mapObj, dictConnections[mapObj.sourceId])
        dataReader.open()
        
    elif mapObj.sourceId in dictFiles:

        dataReader = FileReader(mapObj, dictFiles[mapObj.sourceId])
        dataReader.open()

    elif mapObj.sourceId in dictScripts:

        dataReader = ScriptReader(mapObj, dictScripts[mapObj.sourceId])
        scriptInput = mapObj.sourceQuery
        tempArgs = scriptInput.split('" ')

        for i in range(len(tempArgs)):
            tempID = tempArgs[i].replace('\"', '')
            #if tempArgs[i].find('\"') >= 0:
            #	scriptInput = scriptInput.replace('\"', '') # Input is a constant, just replace parentese
            #else:
            # Replace with file urls
            if tempID in dictFiles:
                (fileName, sep) = FileReader.extractFileNameSeparator(dictFiles[tempID])
                scriptInput = scriptInput.replace(tempArgs[i], fileName)

            # Replace with dabase connections
            if tempID in dictConnections:
                connStr = dictConnections[tempID]
                scriptInput = scriptInput.replace(tempArgs[i],  connStr)
        
        #print scriptInput
        
        dataReader.open(scriptInput)
        
    elif mapObj.sourceId.find("const") >= 0:

        dataReader = ConstantReader(mapObj, dictConstants)
        dataReader.open()
        
    # Create DB/File/... writers for the output
    if mapObj.targetId in dictConnections:

        dataWriter = DatabaseWriter(mapObj, dictConnections[mapObj.targetId])
        dataWriter.open()

    elif mapObj.targetId in dictFiles:

        dataWriter = FileWriter(mapObj, dictFiles[mapObj.targetId])
        dataWriter.open()
    
    # Only constant ID for targets, writes to stdout    
    elif mapObj.targetId =="stdout":
		dataWriter = ConsoleWriter()

    if dataReader == None:
        print mapObj.id + ": Reader can not be created"
        return

            
    # Main part: Iterate with reader, transform, and write to writer
    for tupleIn in dataReader.read():

        #print tuple 
        # Transfrom step, if a script is defined
        if len(mapObj.transformId) > 0:
        	transformScriptUrl = dictScripts[mapObj.transformId]
        	transformScript = ScriptReader.load_from_file(transformScriptUrl, "CustomScriptTransform")
        	
        	# Call script
        	transformScript.open(mapObj.transformQuery.replace('"', ''))
        	tupleTemp = transformScript.map(tupleIn)
        	transformScript.close()
        	
        	# If it returns None, we have to ignore this one 
        	if tupleTemp == None:
        		continue
        	else:
        		tupleIn = tupleTemp
        
        #Replace values of read tuples in result tuple
        tupleOut = mapObj.targetOutput
        
        for i in range(len(tupleIn)):
            repID = '{' + str(i+1) + '}'  # We assume that the indexes start with 
            posID = tupleOut.find(repID)
            posValue = str(tupleIn[i])
            if posID > -1:
                posValue = posValue.replace('"', '').replace("'", '')  # Clean up data and remove double quote, as it causes with some turtle readers
                tupleOut = tupleOut.replace(repID, posValue)
            
        # Write (only if it has some text)
        #print tupleOut
        if(len(tupleOut) > 0):
            dataWriter.write(tupleOut)


    dataWriter.close()

        
def createConnections(lines):

        # Read mapping file for connections, files, scripts, prefix, base, imports
        for i in range(len(lines)):
            nline = lines[i].rstrip()
            
            # Ignore lines which start with hash
            tmpLine =  nline.lstrip()
            if len(tmpLine) > 0 and tmpLine[0] == '#':
            	continue
            
            posConn = nline.find("CONNECTION")
            if posConn > -1: # CONNECTION osm1: host=localhost port=5432 dbname=osm_vienna user=postgres password=ps
                kv = getKeyValueColon(nline)
                dictConnections[kv.key] = kv.value
           
            posFile = nline.find("FILE")
            if posFile > -1: # FILE f1: /Users/patrik/Desktop/OSM_Bench/temp.rdf
                kv = getKeyValueColon(nline)
                dictFiles[kv.key] = kv.value.strip()

            posScript = nline.find("SCRIPT")
            if posScript > -1: # SCRIPT s1: /Users/patrik/Desktop/OSM_Bench/extractRelation.py --relation {1} --role {2} --input1 {3} --input2 {4}
                kv = getKeyValueColon(nline)
                dictScripts[kv.key] = kv.value.strip()

            posPrefix = nline.find("CONST")
            if posPrefix > -1: # CONST tuwt: <http://www.kr.tuwien.ac.at/myits/geoconcepts/terms#>
                kv = getKeyValueColon(nline)
                dictConstants[kv.key] = kv.value.strip()

                
def createMappings(lines):

        # Read file for mappings
        actMapID = savMapID = ""
        mappingLines = []
                                        
        for i in range(len(lines)):
            nline = lines[i]
            
             # Ignore lines which start with hash
            tmpLine =  nline.lstrip()
            if len(tmpLine) > 0 and tmpLine[0] == '#':
            	continue
           
            # The mappingID is the indicator, when a single mapping is finished, new id -> new mapping
            posImport = nline.find("mappingId")
            if posImport > -1:
                kv = getKeyValueSpace(nline)
                actMapID = kv.value
                 
                if actMapID != savMapID and len(savMapID) > 0:
                    mapObj = createMappingObj(savMapID, mappingLines)
                    listMappings.append(mapObj)
                    
                    mappingLines = []

                savMapID = actMapID
                    
            # Simply keep all mapping lines in an array
            if len(actMapID) > 0:
                mappingLines.append(nline)


        if len(actMapID) > 0:
            mapObj = createMappingObj(actMapID, mappingLines)
            listMappings.append(mapObj)


def createMappingObj(id, lines):

    linesForType = []
    typeOfLine = saveType = 0   # 1 = Source, 2 = Transform, 3 = Target, 4 = Dependency

    
    mapObj = Mapping(id.rstrip())

    for i in range(len(lines)):
        nline = lines[i]
        
        posSource = nline.find("source")
        if posSource > -1:
           typeOfLine = 1

        posTrans = nline.find("transform")
        if posTrans > -1:
           typeOfLine = 2

        posTarget = nline.find("target")
        if posTarget > -1:
           typeOfLine = 3

        posDep = nline.find("dependency")
        if posDep > -1:
           typeOfLine = 4

        if saveType != typeOfLine and saveType > 0:
           #print saveType, linesForType
           createMappingPart(mapObj, saveType, linesForType)
           linesForType = []

        if typeOfLine > 0:
           linesForType.append(nline)

           
        saveType = typeOfLine
        

    if saveType > 0:
        #print saveType, linesForType
        createMappingPart(mapObj, saveType, linesForType)

    return mapObj
        
def createMappingPart(mapObj, type, lines):

    tempId = ""
    tempText = "" 

    mapObj.mapType = type

    
    for i in range(len(lines)):
        nline = lines[i]

        # First line is different and the standard case
        if i == 0 and type != 4:
           # Input has the structure TYPE ID TEXT....
           # We skip the first token TYPE and use ID and TEXT
           kv1 = getKeyValueSpace(nline)
           kv2 = getKeyValueSpace(kv1.value)
           tempId = kv2.key
           tempText = kv2.value
        else:
           tempText = tempText + nline
    
    
    if type == 1:
        mapObj.sourceId = tempId
        mapObj.sourceQuery = tempText.rstrip()
    elif type == 2:
        mapObj.transformId = tempId
        mapObj.transformQuery = tempText.rstrip()
    elif type == 3:
        mapObj.targetId = tempId
        mapObj.targetOutput = tempText.rstrip()
        #print type, tempId, tempText
    elif type == 4:
        mapObj.dependency = tempText.rstrip()
   

def getKeyValueSpace(text):

    p = text.find(" ")
    if p > 0:
        kv = KeyValue(text[:p], text[p+1:])
    else:
        kv = KeyValue("","")
    
    return kv

def getKeyValueColon(text):

    p = text.find(":")
    if p > 0:
        type_id = text[0:p] .split(' ')
        kv = KeyValue(type_id[1], text[p+1:]) 
    else:
        raise NameError('Incorrect syntax in line ', i)

    return kv


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])




