##
#@if english
#@package session package
#including classes session, DBConnectionPool, BatchTableWriter, MultithreadedTableWriter
#@endif

import re
import uuid
import numpy as np
import pandas as pd
import warnings
from dolphindb.table import Table
from dolphindb.database import Database
from dolphindb.settings import *
from threading import Lock
from threading import Thread
from datetime import datetime

import os
import sys
import asyncio
from concurrent.futures import ThreadPoolExecutor

sys.path.append(os.path.dirname(__file__))
import dolphindbcpp  as ddbcpp


def _generate_tablename(tableName = None):
    #return "TMP_TBL_" + uuid.uuid4().hex[:8]
    if tableName is None:
        return "TMP_TBL_" + uuid.uuid4().hex[:8]
    else:
        return tableName + "_" + uuid.uuid4().hex[:8]


def _generate_dbname():
    return "TMP_DB_" + uuid.uuid4().hex[:8]+"DB"

def start_thread_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()


##
#@if english
#DBConnectionPool is the connection pool object where multiple threads can be created to execute scripts in parallel and improve task efficiency.
#@attention To improve efficiency, methods such as run of class DBConnectionPool are packaged into coroutine functions in python.
#@endif
class DBConnectionPool(object):
    ##
    #@if english
    #Constructor of DBConnectionPool, including the number of threads, load balancing, high availability, reconnection, compression and Pickle protocol.
    #@param[in] host: server address. It can be IP address, domain, or LAN hostname, etc.
    #@param[in] port: port name
    #@param[in] threadNum: number of threads, default 10.
    #@param[in] userid: username. The default is an empty string.
    #@param[in] password: password. The default is an empty string.
    #@param[in] loadBalance: whether to enable load balancing. True means enabled (the connections will be distributed evenly across the cluster), otherwise False.
    #@param[in] highAvailability: whether to enable high availability. True means enabled, otherwise False.
    #@param[in] compress: whether to enable compression. True means enabled, otherwise False.
    #@param[in] reConnectFlag: whether to enable reconnection. True means enabled, otherwise False.
    #@param[in] python: whether to enable the Python parser. True means enabled, otherwise False.
    #@attention If the parameter python is True, the script is parsed in Python rather than DolphinDB language.
    #@endif
    def __init__(self, host, port, threadNum=10, userid="", password="", loadBalance=False, highAvailability=False, compress=False, reConnect=False, python=False):
        self.pool = ddbcpp.dbConnectionPoolImpl(host, port, threadNum, userid, password, loadBalance, highAvailability, compress, reConnect, python)
        self.host = host
        self.port = port
        self.userid = userid
        self.password = password
        self.taskId = 0
        self.mutex = Lock()
        self.loop = None
        self.thread = None
    
    ##
    #@if english
    #Coroutine function. Pass the script to the connection pool to call the thread execution with the run method.
    #@param[in] script: DolphinDB script to be executed
    #@param[in] args: arguments to be passed to the function
    #@attention args is only required when script is the function name
    #@param[in] clearMemory: whether to release variables after queries. True means to release, otherwise False.
    #@param[in] pickleTableToList: whether to convert table to list or DataFrame. True: to list, False: to DataFrame.
    #@return execution result
    #@attention When setting pickleTableToList=True and enablePickle=True, if the table contains array vectors, it will be converted to a NumPy 2d array. If the length of each row is different, the execution fails.
    #@endif
    async def run(self, script, *args, **kwargs):
        self.mutex.acquire()
        self.taskId = self.taskId + 1
        id = self.taskId
        self.mutex.release()
        if "clearMemory" not in kwargs.keys():
            kwargs["clearMemory"] = True
        self.pool.run(script, id, *args, **kwargs)
        while True:
            isFinished = self.pool.isFinished(id)
            if(isFinished == 0):
                await asyncio.sleep(0.01)
            else:
                return self.pool.getData(id)
    
    ##
    #@if english
    #Add a task and specify the task ID to execute the script
    #@param[in] script: script to be executed
    #@param[in] taskId: the task ID
    #@param[in] clearMemory: whether to release variables after queries. True means to release, otherwise False.
    #@return execution result
    #@endif
    def addTask(self, script, taskId, clearMemory = True):
        return self.pool.run(script, taskId, clearMemory)

    ##
    #@if english
    #Get the completion status of the specified task
    #@param[in] taskId: the task ID
    #@return True if the task is finished, otherwise False.
    #@endif
    def isFinished(self, taskId):
        return self.pool.isFinished(taskId)

    ##
    #@if english
    #Get data of the specified task
    #@param[in] taskId: the task ID
    #@return data of the task
    #@attention For each task, the data can only be obtained once and will be cleared immediately after the data is obtained
    #@endif
    def getData(self, taskId):
        return self.pool.getData(taskId)

    ##
    #@if english
    #Create and start an event loop
    #@exception Exception: the event loop has been created
    #@endif
    def startLoop(self):
        if(self.loop is not None):
            raise Exception("Event loop is already started!")
        self.loop = asyncio.new_event_loop()
        self.thread = Thread(target=start_thread_loop, args=(self.loop,))
        self.thread.setDaemon(True)
        self.thread.start()  

    ##
    #@if english
    #Execute script tasks asynchronously
    #@param[in] script: script to be executed
    #@param[in] clearMemory: whether to release variables after queries. True means to release, otherwise False.
    #@return concurrent.futures.Future object for receiving data
    #@endif
    def runTaskAsyn(self, script, clearMemory = True):
        DeprecationWarning("Please use runTaskAsync instead of runTaskAsyn.")
        return self.runTaskAsync(script,clearMemory)
    
    ##
    #@if english
    #Execute script tasks asynchronously
    #@param[in] script: script to be executed
    #@param[in] clearMemory: whether to release variables after queries. True means to release, otherwise False.
    #@return concurrent.futures.Future object for receiving data
    #@endif
    def runTaskAsync(self, script, clearMemory = True):
        if(self.loop is None):
            self.startLoop()
            #raise Exception("Event loop is not started yet, please run startLoop() first!")
        task = asyncio.run_coroutine_threadsafe(self.run(script, clearMemory=clearMemory), self.loop)
        return task

    ##
    #@if english
    #Stop the event loop
    #@endif
    async def stopLoop(self):
        await asyncio.sleep(0.01)
        self.loop.stop()

    ##
    #@if english
    #Close the DBConnectionPool, stop the event loop and terminate all asynchronous tasks
    #@endif
    def shutDown(self):
        self.host = None
        self.port = None
        if(self.loop is not None):
            test = asyncio.run_coroutine_threadsafe(self.stopLoop(), self.loop)
            self.thread.join()
            if(self.loop.is_running()):
                self.loop.stop()
            else:
                self.loop.close()
        self.pool.shutDown()
        self.pool = None
        self.loop = None
        self.thread = None

    ##
    #@if english
    #Obtain session ID of all sessions
    #@return: list of thread ID
    #@endif
    def getSessionId(self):
        return self.pool.getSessionId()
##
# deserializer stream blob in multistreamingtable reply
class streamDeserializer(object):
    ##
    #@if english
    #Constructor of streamDeserializer
    #@param[in] sym2table: A dict object indicating the corresponding relationship between the unique identifiers of the tables and the table objects.
    #@param[in] session: A session object. The default is None.
    #@endif
    def __init__(self, sym2table, session = None):
        self.cpp = ddbcpp.streamDeserializer(sym2table)
        if session is not None:
            self.cpp.setSession(session.cpp)

class session(object):
    ##
    #@if english
    #Constructor of session, inluding OpenSSL encryption, asynchronous mode, TCP detection, block granularity matching, compression, Pickle protocol
    #@param[in] host: server address. It can be IP address, domain, or LAN hostname, etc.
    #@param[in] port: port name
    #@attention If neither host nor port is set to None, a connection will be established.
    #@param[in] userid: username. The default is an empty string, meaning not to log in.
    #@param[in] password: password. The default is an empty string, meaning not to log in.
    #@param[in] enableSSL: whether to enable SSL. True means enabled, otherwise False.
    #@param[in] enableASYNC: whether to enable asynchronous communication. True means enabled, otherwise False.
    #@param[in] keepAliveTime: the duration between two keepalive transmissions to detect the TCP connection status. The default value is 30 (seconds). Set the parameter to release half-open TCP connections timely when the network is unstable.
    #@param[in] enableChunkGranularityConfig: whether to enable chunk granularity configuration. True means enabled. The default is False.
    #@param[in] compress: whether to enable compressed communication. True means enabled, otherwise False.
    #@param[in] enablePickle: whether to enable the Pickle protocol. True means enabled, otherwise False.
    #@param[in] python: whether to enable python parser. True means enabled, otherwise False.
    #@attention set enableSSL =True to enable encrypted communication. It's also required to configure ebleHTTPS =true in the server.
    #@attention set enableASYNC =True to enable asynchronous mode and the communication with the server can only be done through the session.run method. As there is no return value, it is suitable for asynchronous writes.
    #@endif
    def __init__(self, host=None, port=None, userid="", password="",enableSSL=False, enableASYNC=False,
                 keepAliveTime=30, enableChunkGranularityConfig=False,compress=False, enablePickle=True,
                 python=False, **kwargs):
        if 'enableASYN' in kwargs.keys():
            enableASYNC = kwargs['enableASYN']
            DeprecationWarning("Please use enableASYNC instead of enableASYN.")
        self.cpp = ddbcpp.sessionimpl(enableSSL, enableASYNC, keepAliveTime,compress,enablePickle,python)
        self.host = host
        self.port = port
        self.userid = userid
        self.password=password
        self.mutex = Lock()
        self.enableEncryption = True
        self.enableChunkGranularityConfig = enableChunkGranularityConfig
        self.enablePickle = enablePickle
        if self.host is not None and self.port is not None:
            self.connect(host, port, userid, password)
    
    def __del__(self):
        self.cpp.close()

    ##
    #@if english
    #Establish connection, including initialization script, high availability, TCP detection
    #@param[in] host: server address. It can be IP address, domain, or LAN hostname, etc.
    #@param[in] port: port name
    #@param[in] userid: username. The default is an empty string, meaning not to log in.
    #@param[in] password: password. The default is an empty string, meaning not to log in.
    #@param[in] startup: the startup script to execute the preloaded tasks immediately after the connection is established. The default is an empty string.
    #@param[in] highAvailability: whether to enable high availability. True means enabled, otherwise False.
    #@param[in] highAvailabilitySites: a list of high-availability nodes, default None.
    #@param[in] keepAliveTime: the duration between two keepalive transmissions to detect the TCP connection status. The default value is 30 (seconds). Set the parameter to release half-open TCP connections timely when the network is unstable.
    #@param[in] reconnect: whether to enable reconnection. True means enabled, otherwise False.
    #@return bool: whether the connection is established. True if established, otherwise False.
    #@endif
    def connect(self, host, port, userid="", password="", startup="", highAvailability=False, highAvailabilitySites=None, keepAliveTime=None, reconnect=False):
        if highAvailabilitySites is None:
            highAvailabilitySites = []
        if keepAliveTime is None:
            keepAliveTime = -1
        return self.cpp.connect(host, port, userid, password, startup, highAvailability, highAvailabilitySites, keepAliveTime, reconnect)

    ##
    #@if english
    #Manually log in to the server.
    #@param[in] userid: username. The default is an empty string.
    #@param[in] password: password. The default is an empty string.
    #@param[in] enableEncryption: whether to enable encrypted transmission for username and password. The default is True.
    #@attention: Fill in userid and password in connect and the user will be logged in automatically
    #@endif
    def login(self,userid, password, enableEncryption=True):
        self.mutex.acquire()
        try:
            self.userid = userid
            self.password = password
            self.enableEncryption = enableEncryption
            self.cpp.login(userid, password, enableEncryption)
        finally:
            self.mutex.release()

    ##
    #@if english
    #Close session connection
    #@endif
    def close(self):
        self.host = None
        self.port = None
        self.cpp.close()
    
    ##
    #@if english
    #Check if the current session has been closed
    #@return bool: True if closed, otherwise False.
    #@endif
    def isClosed(self):
        return self.host is None

    ##
    #@if english
    #Upload Python objects to DolphinDB server
    #@param nameObjectDict: Python dictionary object. The keys of the dictionary are the variable names in DolphinDB and the values are Python objects, which can be numbers, strings, lists, DataFrame, etc.
    #@return Python Address: return the server address of the uploaded object
    #@attention: A pandas DataFrame corresponds to DolphinDB table
    #@endif
    def upload(self, nameObjectDict):
        return self.cpp.upload(nameObjectDict)

    ##
    #@if english
    #Execute script
    #@param[in] script: DolphinDB script to be executed
    #@param[in] args: arguments to be passed to the function
    #@attention: args is only required when script is the function name
    #@param[in] clearMemory: whether to release variables after queries. True means to release, otherwise False.
    #@param[in] pickleTableToList: whether to convert table to list or DataFrame. True: to list, False: to DataFrame.
    #@param[in] fetchSize: the size of a block
    #@return execution result. If fetchSize is specified, a BlockReader object will be returned. Each block can be read with the read() method.
    #@attention fetchSize cannot be less than 8192 Bytes.
    #@attention When setting pickleTableToList=True and enablePickle=True, if the table contains array vectors, it will be converted to a NumPy 2d array. If the length of each row is different, the execution fails.
    #@endif
    def run(self, script, *args, **kwargs):
        if(kwargs):
            if "fetchSize" in kwargs.keys():
                return BlockReader(self.cpp.runBlock(script, **kwargs))
        return self.cpp.run(script, *args, **kwargs)
    

    ##
    #@if english
    #Execute script
    #@param[in] filepath: the path of the file on the server to be executed
    #@param[in] args: arguments to be passed to the function
    #@attention: args is only required when script is the function name
    #@param[in] clearMemory: whether to release variables after queries. True means to release, otherwise False.
    #@param[in] pickleTableToList: whether to convert table to list or DataFrame. True: to list, False: to DataFrame.
    #@return execution result
    #@attention When setting pickleTableToList=True and enablePickle=True, if the table contains array vectors, it will be converted to a NumPy 2d array. If the length of each row is different, the execution fails.
    #@endif
    def runFile(self, filepath, *args, **kwargs):
        with open(filepath, "r") as fp:
            script = fp.read()
            return self.run(script, *args, **kwargs)

    ##
    #@if english
    #Get the session ID of the current session
    #@return: session ID
    #@endif
    def getSessionId(self):
        return self.cpp.getSessionId()

    ##
    #@if english
    #@deprecated Convert all NULL values to 0
    #@endif
    def nullValueToZero(self):
        self.cpp.nullValueToZero()
    
    ##
    #@if english
    #@deprecated Convert all NULL values to NumPy NaN
    #@endif
    def nullValueToNan(self):
        self.cpp.nullValueToNan()

    ##
    #@if english
    #Enable streaming
    #@param[in] port: the subscription port for incoming data. The server will connect to the port automatically.
    #@param[in] threadCount: the number of threads, default 1
    #@endif
    def enableStreaming(self, port, threadCount = 1):
        self.cpp.enableStreaming(port,threadCount)

    ##
    #@if english
    #Subscribe to stream tables in DolphinDB
    #@param[in] host: server address. It can be IP address, domain, or LAN hostname, etc.
    #@param[in] port: port name
    #@param[in] handler: user-defined callback function for processing incoming data
    #@param[in] tableName: name of the published table
    #@param[in] actionName: name of the subscription task. The default is an empty string.
    #@param[in] offset: an integer indicating the position of the first message where the subscription begins. The default value is -1.
    #@attention: If offset is -1 or exceeding the number of rows in the stream table, the subscription starts with the next new message. It cannot be other negative values.
    #@param[in] resub: whether to resubscribe after network disconnection. True means automatic resubscription. The default value is False.
    #@param[in] filter: a vector indicating the filtering columns. Only the rows with values of the filtering column in the vector are published to the subscriber. The default value is None.
    #@param[in] msgAsTable: whether to convert the subscribed data to dataframe. If msgAsTable = True, the subscribed data is ingested into handler as a DataFrame. The default value is False, which means the subscribed data is ingested into handler as a List of nparrays. This optional parameter has no effect if batchSize is not specified.
    #@param[in] batchSize: an integer indicating the number of unprocessed messages to trigger the handler. If it is positive, the handler does not process messages until the number of unprocessed messages reaches batchSize. If it is unspecified or non-positive, the handler processes incoming messages as soon as they come in. The default value is 0.
    #@param[in] throttle: an integer indicating the maximum waiting time (in seconds) before the handler processes the incoming messages. The default value is 1. This optional parameter has no effect if batchSize is not specified.
    #@param[in] userName: username. The default is an empty string, meaning not to log in.
    #@param[in] password: password. The default is an empty string, meaning not to log in.
    #@param[in] streamDeserializer: A deserializer of heterogeneous stream table. The default value is None.
    #@endif
    def subscribe(self, host, port, handler, tableName, actionName="", offset=-1, resub=False, filter=None, msgAsTable=False, batchSize=0, throttle=1,
                  userName="", password="", streamDeserializer=None):
        if not isinstance(msgAsTable, bool):
            raise ValueError("msgAsTable must be a bool")
        if filter is None:
            filter = np.array([],dtype='int64')
        sd=None
        if streamDeserializer is None:
            sd = ddbcpp.streamDeserializer({})
        else:
            sd = streamDeserializer.cpp
        if batchSize > 0:
            self.cpp.subscribeBatch(host, port, handler, tableName, actionName, offset, resub, filter, msgAsTable, batchSize, throttle,userName,password,sd)
        else:
            if msgAsTable:
                raise ValueError("msgAsTable must be False when batchSize is 0")
            self.cpp.subscribe(host, port, handler, tableName, actionName, offset, resub, filter,userName,password,sd)

    ##
    #@if english
    #Unsubscribe
    #@param[in] host: server address. It can be IP address, domain, or LAN hostname, etc.
    #@param[in] port: port name
    #@param[in] tableName: name of the published table
    #@param[in] actionName: name of the subscription task. The default is an empty string.
    #@endif
    def unsubscribe(self, host, port, tableName, actionName=""):
        self.cpp.unsubscribe(host, port, tableName, actionName)

    ##
    #@if english
    #Hash map, which maps DolphinDB objects into hash buckets of size nBucket
    #@param[in] obj: the DolphinDB object to be hashed.
    #@param[in] nBucket: hash bucket size
    #@return hash of the DolphinDB object
    #@endif
    def hashBucket(self, obj, nBucket):
        if not isinstance(nBucket, int) or nBucket <= 0:
            raise ValueError("nBucket must be a positive integer")
        return self.cpp.hashBucket(obj, nBucket)

    ##
    #@if english
    #Get the init script of the session
    #@return string of the init script
    #@endif
    def getInitScript(self):
        return self.cpp.getInitScript()

    ##
    #@if english
    #Set up init script of the session
    #@param[in] script string of the init script
    #@endif
    def setInitScript(self, script):
        self.cpp.setInitScript(script)

    ##
    #@if english
    #Get all subscription topics
    #@return a list of all subscription topics in the format of "host/port/tableName/actionName"
    #@endif
    def getSubscriptionTopics(self):
        return self.cpp.getSubscriptionTopics()

    ##
    #@if english
    #Save the table
    #@param[in] tbl DolphinDB object of the in-memory table to be saved
    #@param[in] dbPath DolphinDB database path
    #@return True
    #@endif
    def saveTable(self, tbl, dbPath):
        tblName = tbl.tableName()
        dbName =  _generate_dbname()
        s1 = dbName+"=database('"+dbPath+"')"
        self.run(s1)
        s2 = "saveTable(%s, %s)" % (dbName, tblName)
        self.run(s2)
        return True

    ##
    #@if english
    #Import text files into DolphinDB as an in-memory table
    #@param[in] remoteFilePath: the remote file path on the server
    #@param[in] delimiter: delimiter, the default value is ','
    #@return a DolphinDB in-memory table
    #@attention The amount of data loaded into the in-memory table must be less than the available memory
    #@endif
    def loadText(self,  remoteFilePath=None, delimiter=","):
        tableName = _generate_tablename()
        runstr = tableName + '=loadText("' + remoteFilePath + '","' + delimiter + '")'
        self.run(runstr)
        return Table(data=tableName, s=self, isMaterialized=True)

    ##
    #@if english
    #Import text files in parallel into DolphinDB as a partitioned in-memory table, which is faster than method loadText
    #@param[in] remoteFilePath: the remote file path on the server
    #@param[in] delimiter: delimiter, the default value is ','
    #@return a DolphinDB in-memory table
    #@endif
    def ploadText(self, remoteFilePath=None, delimiter=","):
        tableName = _generate_tablename()
        runstr = tableName + '= ploadText("' + remoteFilePath + '","' + delimiter + '")'
        self.run(runstr)
        return Table(data=tableName, s=self, isMaterialized=True)

    ##
    #@if english
    #load a DolphinDB table
    #@param[in] tableName: the DolphinDB table name
    #@param[in] dbPath: path to the DolphinDB database, the default value is None
    #@param[in] partitions: the partition columns of the partitioned table, the default value is None
    #@deprecated @param[in] memoryMode: the storage mode, deprecated. True means to load all data into memory, the default value is False.
    #@return DolphinDB table object
    #@endif
    def loadTable(self,tableName,  dbPath=None, partitions=None, memoryMode=False):
        def isDate(s):
            try:
                datetime.strptime(s, '%Y.%m.%d')
                return True
            except ValueError:
                return False

        def isMonth(s):
            try:
                datetime.strptime(s, '%Y.%mM')
                return True
            except ValueError:
                return False

        def isDatehour(s):
            try:
                datetime.strptime(s, '%Y.%m.%dT%H')
                return True
            except ValueError:
                return False

        def isTime(s):
            return isDate(s) or isMonth(s) or isDatehour(s)

        def myStr(x):
            if type(x) is str and not isTime(x):
                return "'" + x + "'"
            else:
                return str(x)

        if partitions is None:
            partitions = []
        if dbPath:
            runstr = '{tableName} = loadTable("{dbPath}", "{data}",{partitions},{inMem})'
            fmtDict = dict()
            tbName = _generate_tablename(tableName)
            fmtDict['tableName'] = tbName
            fmtDict['dbPath'] = dbPath
            fmtDict['data'] = tableName
            if type(partitions) is list:
                fmtDict['partitions'] = ('[' + ','.join(myStr(x) for x in partitions) + ']') if len(partitions) else ""
            else:
                fmtDict['partitions'] = myStr(partitions)

            fmtDict['inMem'] = str(memoryMode).lower()
            runstr = re.sub(' +', ' ', runstr.format(**fmtDict).strip())
            self.run(runstr)
            return Table(data=tbName, s=self, isMaterialized=True)
        else:
            return Table(data=tableName, s=self, needGC=False, isMaterialized=True)

    ##
    #@if english
    #Load records that satisfy the filtering conditions in a SQL query as a partitioned in-memory table
    #@param tableName: the DolphinDB table name
    #@param dbPath: the DolphinDB database where the table is stored
    #@param sql: SQL statement
    #@return Table object
    #@endif
    def loadTableBySQL(self, tableName, dbPath, sql):
        # loadTableBySQL
        runstr = 'db=database("' + dbPath + '")'
        self.run(runstr)
        runstr = tableName + '= db.loadTable("%s")' % tableName
        self.run(runstr)
        tmpTableName = _generate_tablename()
        runstr = tmpTableName + "=loadTableBySQL(<%s>)" % sql
        self.run(runstr)
        return Table(data=tmpTableName, s=self, isMaterialized=True)

    def convertDatetime64(self, datetime64List):
        l = len(str(datetime64List[0]))
        # date and month
        if l == 10 or l == 7:
            listStr = '['
            for dt64 in datetime64List:
                s = str(dt64).replace('-', '.')
                if len(str(dt64)) == 7:
                    s += 'M'
                listStr += s + ','
            listStr = listStr.rstrip(',')
            listStr += ']'
        else:
            listStr = 'datehour(['
            for dt64 in datetime64List:
                s = str(dt64).replace('-', '.').replace('T', ' ')
                ldt = len(str(dt64))
                if ldt == 13:
                    s += ':00:00'
                elif ldt == 16:
                    s += ':00'
                listStr += s + ','
            listStr = listStr.rstrip(',')
            listStr += '])'
        return listStr


    def convertDatabase(self, databaseList):
        listStr = '['
        for db in databaseList:
            listStr += db._getDbName()
            listStr += ','
        listStr = listStr.rstrip(',')
        listStr += ']'
        return listStr

    ##
    #@if english
    #Create database
    #@param[in] dbName: database name, the default value is None
    #@param[in] partitionType: partition type, the default value is None
    #@param[in] partitions: partitioning column name (string or list), the default value is None
    #@param[in] dbPath: database path, the default value is None
    #@param[in] engine: storage engine, can be 'OLAP' or 'TSDB'. The default value is 'OLAP'
    #@param[in] atomic: indicates at which level the atomicity is guaranteed for a write transaction. It can be 'TRANS' or 'CHUNK', the default value is 'TRANS'
    #@param[in] chunkGranularity: the chunk granularity, can be 'TABLE' or 'DATABASE', the default value is None
    #@attention: The parameter chunkGranularity only takes effect when enableChunkGranularityConfig = true
    #@return DolphinDB database object
    #@endif
    def database(self,dbName=None, partitionType=None, partitions=None, dbPath=None, engine=None, atomic=None, chunkGranularity=None):
        if partitions is not None:
            partition_type = type(partitions[0])
        else:
            partition_type = None

        if partition_type == np.datetime64:
            partition_str = self.convertDatetime64(partitions)

        elif partition_type == Database:
            partition_str = self.convertDatabase(partitions)

        elif type(partitions) == np.ndarray and (partition_type == np.ndarray or partition_type == list):
            dataType = type(partitions[0][0])
            partition_str = '['
            for partition in partitions:
                if dataType == date or dataType == month:
                    partition_str += self.convertDateAndMonth(partition) + ','
                elif dataType == datetime:
                    partition_str += self.convertDatetime(partition) + ','
                elif dataType == Database:
                    partition_str += self.convertDatabase(partition) + ','
                else:
                    partition_str += str(partition) + ','
                    partition_str = partition_str.replace('list', ' ')
                    partition_str = partition_str.replace('(', '')
                    partition_str = partition_str.replace(')', '')
            partition_str = partition_str.rstrip(',')
            partition_str += ']'

        else:
            if partition_type is not None:
                partition_str = str(partitions)
            else:
                partition_str = ""

        if dbName is None:
            dbName = _generate_dbname()

        if partitionType:
            if dbPath:
                dbstr =  dbName + '=database("'+dbPath+'",' + str(partitionType) + "," + partition_str
            else:
                dbstr =  dbName +'=database("",' + str(partitionType) + "," + partition_str
        else:
            if dbPath:
                dbstr =  dbName +'=database("' + dbPath + '"'
            else:
                dbstr =  dbName +'=database(""'
        
        if engine is not None:
            dbstr += ",engine='"+engine+"'"
        if atomic is not None:
            dbstr += ",atomic='"+atomic+"'"
        if self.enableChunkGranularityConfig == True :
            dbstr += ",chunkGranularity='"+chunkGranularity+"'"
        
        dbstr+=")"

        self.run(dbstr)
        return Database(dbName=dbName, s=self)

    ##
    #@if english
    #Check if the database exists
    #@param[in] dbUrl: database path
    #@return bool: True if the database exists, otherwise False
    #@endif
    def existsDatabase(self, dbUrl):
        return self.run("existsDatabase('%s')" % dbUrl)

    ##
    #@if english
    #Check if the table exists
    #@param[in] dbUrl: database path
    #@param[in] tableName: table name
    #@return bool: True if the table exists, otherwise False
    #@endif
    def existsTable(self, dbUrl, tableName):
        return self.run("existsTable('%s','%s')" % (dbUrl,tableName))

    ##
    #@if english
    #Delete a database
    #@param[in] dbPath: database path
    #@endif
    def dropDatabase(self, dbPath):
        self.run("dropDatabase('" + dbPath + "')")

    ##
    #@if english
    #Delete one or more partitions of the database
    #@param[in] dbPath: database path
    #@param[in] partitionPaths: a string or list of partition paths
    #@attention: The directory of a partition under the database folder or a list of directories of multiple partitions must start with '/'
    #@param[in] tableName: table name. The default is None, indicating all tables under the partitions are deleted.
    #@endif
    def dropPartition(self, dbPath, partitionPaths, tableName=None):
        db = _generate_dbname()
        self.run(db + '=database("' + dbPath + '")')
        if isinstance(partitionPaths, list):
            pths = ','.join(partitionPaths)
        else:
            pths = partitionPaths

        if tableName:
            self.run("dropPartition(%s,[%s],\"%s\")" % (db, pths, tableName))
        else:
            self.run("dropPartition(%s,[%s])" % (db, pths))

    ##
    #@if english
    #Delete a table
    #@param[in] dbPath: database path
    #@param[in] tableName: table name
    #@endif
    def dropTable(self, dbPath, tableName):
        db = _generate_dbname()
        self.run(db + '=database("' + dbPath + '")')
        self.run("dropTable(%s,'%s')" % (db,tableName))

    ##
    #@if english
    #Import a partitioned in-memory table
    #@param[in] dbPath: database path. The default is an empty string.
    #@param[in] tableName: table name. The default is an empty string.
    #@param[in] partitionColumns: list of strings indicating the partitioning columns, default is None
    #@param[in] remoteFilePath: remote file path. The default is an empty string.
    #@param[in] delimiter: delimiter of each column, the default value is ','
    #@return DolphinDB Table object
    #@endif
    def loadTextEx(self, dbPath="", tableName="",  partitionColumns=None, remoteFilePath="", delimiter=","):
        if partitionColumns is None:
            partitionColumns = []
        isDBPath = True
        if "/" in dbPath or "\\" in dbPath or "dfs://" in dbPath:
            dbstr ='db=database("' + dbPath + '")'
            self.run(dbstr)
            tbl_str = '{tableNameNEW} = loadTextEx(db, "{tableName}", {partitionColumns}, "{remoteFilePath}", {delimiter})'
        else:
            isDBPath = False
            tbl_str = '{tableNameNEW} = loadTextEx('+dbPath+', "{tableName}", {partitionColumns}, "{remoteFilePath}", {delimiter})'
        fmtDict = dict()
        fmtDict['tableNameNEW'] = _generate_tablename()
        fmtDict['tableName'] = tableName
        fmtDict['partitionColumns'] = str(partitionColumns)
        fmtDict['remoteFilePath'] = remoteFilePath
        fmtDict['delimiter'] = delimiter
        # tbl_str = tableName+'=loadTextEx(db,"' + tableName + '",'+ str(partitionColumns) +',"'+ remoteFilePath+"\",'"+delimiter+"')"
        tbl_str = re.sub(' +', ' ', tbl_str.format(**fmtDict).strip())
        self.run(tbl_str)
        if isDBPath:
            return Table(data=fmtDict['tableName'] , dbPath=dbPath, s=self)
        else:
            return Table(data=fmtDict['tableNameNEW'], s=self)

    ##
    #@if english
    #Release the specified object in the session
    #@param[in] varName: variable name in DolphinDB
    #@param[in] varType: variable type in DolphinDB,including "VAR" (variable), "SHARED" (shared variable), "DEF" (function definition)
    #@endif
    def undef(self, varName, varType):
        undef_str = 'undef("{varName}", {varType})'
        fmtDict = dict()
        fmtDict['varName'] = varName
        fmtDict['varType'] = varType
        self.run(undef_str.format(**fmtDict).strip())

    ##
    #@if english
    #Release all objects in the session
    #@endif
    def undefAll(self):
        self.run("undef all")

    ##
    #@if english
    #Clear all cache
    #@param[in] dfs: True: clear cache of all nodes; False (default): only clear the cache of the connected node
    #@endif
    def clearAllCache(self, dfs=False):
        if dfs:
            self.run("pnodeRun(clearAllCache)")
        else:
            self.run("clearAllCache()")

    ##
    #@if english
    #Create a DolphinDB table object and upload it to the server.
    #@param[in] data: data of the table, can be a dictionary, DataFrame or a DolphinDB table name
    #@param[in] dbPath: database path, the default value is None
    #@return DolphinDB table object
    #@endif
    def table(self, data, dbPath=None):
        return Table(data=data, dbPath=dbPath, s=self)

    ##
    #@if english
    #Create a DolphinDB table object and upload it to the server.
    #@param[in] dbPath: database path, the default is None
    #@param[in] data: data of the table, the default value is None
    #@param[in] tableAliasName: alias of the table, the default value is None
    #@param[in] inMem (deprecated): whether to load the table into memory. True: to load the table into memory. The default value is False.
    #@param[in] partitions: the partitions to be loaded into memory, the default value is None, which means to load all partitions.
    #@return DolphinDB table object
    #@endif
    def table(self, dbPath=None, data=None,  tableAliasName=None, inMem=False, partitions=None):
        if partitions is None:
            partitions = []
        return Table(dbPath=dbPath, data=data,  tableAliasName=tableAliasName, inMem=inMem, partitions=partitions, s=self)
    

    def loadPickleFile(self, filePath):
        return self.cpp.loadPickleFile(filePath)
    
##
#@if english
#Read in blocks. Specify the paramter fetchSize for method session.run and it returns a BlockReader object to read in blocks.
#@endif
class BlockReader(object):
    ##
    #@if english
    #Constructor
    #@param[in] blockReader: dolphindbcpp object
    #@endif
    def __init__(self, blockReader):
        self.block = blockReader

    ##
    #@if english
    #Read a piece of data
    #@return Execution result of a script
    #@endif
    def read(self): 
        return self.block.read()

    ##
    #@if english
    #Check if there is data to be read
    #@return bool: True if there is still data not read, otherwise False
    #@endif
    def hasNext(self):
        return self.block.hasNext()

    ##
    #@if english
    #Skip subsequent data
    #@attention: When reading data in blocks, if not all blocks are read, please call the skipAll method to abort the reading before executing the subsequent code.
    #Otherwise, data will be stuck in the socket buffer and the deserialization of the subsequent data will fail.
    #@endif
    def skipAll(self):
        self.block.skipAll()

##
#@if english
#Class for writes to DolphinDB DFS tables
#@attention: DolphinDB does not allow multiple writers to write data to the same partition at the same time, so when the client writes data in parallel with multiple threads, please ensure that each thread writes to a different partition.
#The python API provides PartitionedTableAppender, an easy way to automatically split data writes by partition
#@endif
class PartitionedTableAppender(object):
    ##
    #@if english
    #Constructor of PartitionedTableAppender
    #@param[in] dbPath: DFS database path, the default value is the default is an empty string
    #@param[in] tableName: name of a DFS table
    #@param[in] partitionColName: partitioning column, the default value is the default is an empty string
    #@param[in] dbConnectionPool: connection pool, the default is None
    #@endif
    def __init__(self, dbPath="", tableName="", partitionColName="", dbConnectionPool=None):
        if(isinstance(dbConnectionPool, DBConnectionPool) == False):
            raise Exception("dbConnectionPool must be a dolphindb DBConnectionPool!") 
        self.appender = ddbcpp.partitionedTableAppender(dbPath, tableName, partitionColName, dbConnectionPool.pool)

    ##
    #@if english
    #Append data
    #@param[in] table: data to be written
    #@return int: number of rows written
    #@endif
    def append(self, table):
        return self.appender.append(table)

##
#@if english
#Class of table appender
#As the only temporal data type in Python pandas is datetime64, all temporal columns of a DataFrame are converted into nanotimestamp type after uploaded to DolphinDB.
#Each time we use tableInsert or insert into to append a DataFrame with a temporal column to an in-memory table or DFS table, we need to conduct a data type conversion for the time column.
#For automatic data type conversion, Python API offers tableAppender object.
#@endif
class tableAppender(object) :
    ##
    #@if english
    #Constructor of tableAppender
    #@param[in] dbPath: the path of a DFS database. Leave it unspecified for in-memory tables. The default is an empty string
    #@param[in] tableName: table name, the default is an empty string
    #@param[in] ddbSession: a session connected to DolphinDB server, the default is None
    #@param[in] action: the action when appending. Now only supports "fitColumnType", indicating to convert the data type of temporal column.
    #@endif
    def __init__(self, dbPath="", tableName="", ddbSession=None, action="fitColumnType"):
        if(isinstance(ddbSession, session) == False):
            raise Exception("ddbSession must be a dolphindb session!")
        if(action == "fitColumnType"):
            self.tableappender = ddbcpp.autoFitTableAppender(dbPath, tableName, ddbSession.cpp)
        else:
            raise Exception("other action not supported yet!")
    
    ##
    #@if english
    #Append data
    #@param[in] table: data to be written
    #@return int: number of rows written
    #@endif
    def append(self, table):
        return self.tableappender.append(table)  

##
#@if english
#Class of table upsert
#@endif
class tableUpsert(object) :
    def __init__(self, dbPath="", tableName="", ddbSession=None, ignoreNull = False, keyColNames = [], sortColumns=[]):
        if(isinstance(ddbSession, session) == False):
            raise Exception("ddbSession must be a dolphindb session!")
        self.tableupsert = ddbcpp.autoFitTableUpsert(dbPath, tableName, ddbSession.cpp,ignoreNull,keyColNames,sortColumns)
    ##
    #@if english
    #upsert data
    #@param[in] table: data to be written
    #@return int: number of rows written
    #@endif
    def upsert(self, table):
        return self.tableupsert.upsert(table)  

##
#@if english
#Class of batch writer for asynchronous batched writes
#Support batched writes to in-memory table and distributed table.
#@endif
class BatchTableWriter(object):
    ##
    #@if english
    #Constructor
    #@param[in] host: server address
    #@param[in] port: port name
    #@param[in] userid: username
    #@param[in] password: password
    #@param[in] acquireLock: whether to acquire a lock in the Python API, True (default) means to acquire a lock.
    #@attention: It's required to acquire the lock for concurrent API calls
    #@endif
    def __init__(self, host, port, userid="", password="", acquireLock=True):
        self.writer = ddbcpp.batchTableWriter(host, port, userid, password, acquireLock)
    
    ##
    #@if english
    #Add a table to be written to
    #@param[in] dbPath: the database path for a disk table; leave it empty for an in-memory table. The default value is an empty string.
    #@param[in] tableName: The table name, the default value is an empty string
    #@param[in] partitioned: whether is a partitioned table. True (default) indicates a partitioned table.
    #@attention: If the table is a non-partitioned table on disk, it's required to set partitioned=False.
    #@endif
    def addTable(self, dbPath="", tableName="", partitioned=True):
        self.writer.addTable(dbPath, tableName, partitioned)

    ##
    #@if english
    #Get the current write status
    #@param[in] dbPath: database name, the default value is an empty string
    #@param[in] tableName: table name, the default value is an empty string
    #@return tuple(int, bool, bool):
    #indicating the depth of the current writing queue, whether the current table is being removed (True if being removed), and whether the background thread exits due to an error (True if exits due to an error)
    #@endif
    def getStatus(self, dbPath="", tableName=""):
        return self.writer.getStatus(dbPath, tableName)

    ##
    #@if english
    #Get the status of all tables except for the removed ones
    #@return: The result is a table:
    #| DatabaseName | TableName | WriteQueueDepth | sentRows | Removing | Finished |
    #| ----: | :----: | :----: | :----: | :----: | :---- |
    #| 0 | tglobal | 0 | 5 | False | False |
    #@endif
    def getAllStatus(self):
        return self.writer.getAllStatus()

    ##
    #@if english
    #Obtain unwritten data. The method is mainly used to obtain the remaining unwritten data if an error occurs when writing.
    #@param[in] dbPath: database name, the default value is an empty string
    #@param[in] tableName: table name, the default value is an empty string
    #@return DataFrame of unwritten data
    #@endif
    def getUnwrittenData(self, dbPath="", tableName=""):
        return self.writer.getUnwrittenData(dbPath, tableName)

    ##
    #@if english
    #Release the resources occupied by the table added by the addTable method. The first time the method is called, it returns if the thread has exited
    #@param[in] dbPath: database name, the default value is an empty string
    #@param[in] tableName: table name, the default value is an empty string
    #@endif
    def removeTable(self, dbPath="", tableName=""):
        self.writer.removeTable(dbPath, tableName)

    ##
    #@if english
    #Insert a single row of data
    #@param[in] dbPath: database name, the default value is an empty string
    #@param[in] tableName: table name, the default value is an empty string
    #@param[in] args: variable-length argument, indicating a row of data to be inserted
    #@endif
    def insert(self, dbPath="", tableName="", *args):
        self.writer.insert(dbPath, tableName, *args)

##
#@if english
#MTW error codes and messages
#@endif
class ErrorCodeInfo(object):
    ##
    #@if english
    #Constructor
    #@param[in] errorCode: error code, the default is None
    #@param[in] errorInfo: error information, the default is None
    #@endif
    def __init__(self,errorCode=None,errorInfo=None):
        self.errorCode=errorCode
        self.errorInfo=errorInfo
    def __repr__(self):
        errorCodeText = ""
        if self.hasError():
            errorCodeText = self.errorCode
        else:
            errorCodeText = None
        outStr="errorCode: %s\n" % errorCodeText
        outStr+=" errorInfo: %s\n" % self.errorInfo
        outStr += object.__repr__(self)
        return outStr
    
    ##
    #@if english
    #Check if an error has occurred
    #@return True if an error occurred, otherwise False
    #@endif
    def hasError(self):
        return self.errorCode is not None and len(self.errorCode) > 0
    
    ##
    #@if english
    #Check if data have been written successfully
    #@return True if the write is successful, otherwise False
    #@endif
    def succeed(self):
        return self.errorCode is None or len(self.errorCode) < 1

##
#@if english
#Get the status of MTW
#@endif
class MultithreadedTableWriterThreadStatus(object):
    ##
    #@if english
    #@var threadId thread ID
    #@var sentRows number of sent rows
    #@var unsentRows number of rows to be sent
    #@var sendFailedRows number of rows failed to be sent
    ## Constructor
    #@param[in] threadId: thread ID
    #@endif
    def __init__(self,threadId=None):
        self.threadId=threadId
        self.sentRows=None
        self.unsentRows=None
        self.sendFailedRows=None

##
#@if english
#The status information of MTW
#@endif
class MultithreadedTableWriterStatus(ErrorCodeInfo):
    ##
    #@if english
    #@var isExiting whether the threads are exiting
    #@var sentRows number of sent rows
    #@var unsentRows number of rows to be sent
    #@var sendFailedRows number of rows failed to be sent
    #@var threadStatus a list of the thread status
    #@endif
    def __init__(self):
        self.isExiting=None
        self.sentRows=None
        self.unsentRows=None
        self.sendFailedRows=None
        self.threadStatus=[]

    def update(self,statusDict):
        threadStatusDict=statusDict["threadStatus"]
        del statusDict["threadStatus"]
        self.__dict__.update(statusDict)
        for oneThreadStatusDict in threadStatusDict:
            oneThreadStatus=MultithreadedTableWriterThreadStatus()
            oneThreadStatus.__dict__.update(oneThreadStatusDict)
            self.threadStatus.append(oneThreadStatus)
    
    def __repr__(self):
        errorCodeText = ""
        if self.hasError():
            errorCodeText = self.errorCode
        else:
            errorCodeText = None
        outStr="%-14s: %s\n" % ("errorCode",errorCodeText)
        if self.errorInfo is not None:
            outStr += " %-14s: %s\n" % ("errorInfo",self.errorInfo)
        if self.isExiting is not None:
            outStr += " %-14s: %s\n" % ("isExiting",self.isExiting)
        if self.sentRows is not None:
            outStr += " %-14s: %s\n" % ("sentRows",self.sentRows)
        if self.unsentRows is not None:
            outStr += " %-14s: %s\n" % ("unsentRows",self.unsentRows)
        if self.sendFailedRows is not None:
            outStr += " %-14s: %s\n" % ("sendFailedRows",self.sendFailedRows)
        if self.threadStatus is not None:
            outStr += " %-14s: \n" % "threadStatus"
            outStr += " \tthreadId\tsentRows\tunsentRows\tsendFailedRows\n"
            for thread in self.threadStatus:
                outStr+="\t"
                if thread.threadId is not None:
                    outStr+="%8d"%thread.threadId
                outStr+="\t"
                if thread.sentRows is not None:
                    outStr+="%8d"%thread.sentRows
                outStr+="\t"
                if thread.unsentRows is not None:
                    outStr+="%10d"%thread.unsentRows
                outStr+="\t"
                if thread.sendFailedRows is not None:
                    outStr+="%14d"%thread.sendFailedRows
                outStr+="\n"
        outStr += object.__repr__(self)
        return outStr

##
#@if english
#A multi-threaded writer is an ungrade of BatchTableWriter with support for multi-threaded concurrent writes.
#@endif
class MultithreadedTableWriter(object):
    ##
    #@if english
    #Constructor
    #@param[in] host: host name
    #@param[in] port: port number
    #@param[in] userId: username
    #@param[in] password: password
    #@param[in] dbPath: the DFS database path or in-memory table name
    #@param[in] tableName: the DFS table name. Leave it unspecified for an in-memory table
    #@param[in] useSSL: whether to enable SSL. The default value is False
    #@param[in] enableHighAvailability: whether to enable high availability. The default value is False
    #@param[in] highAvailabilitySites: a list of ip:port of all available nodes, the default value is an empty list
    #@param[in] batchSize: the number of messages in batch processing, the default value is 1
    #@param[in] throttle: the waiting time (in seconds) before the server processes the incoming data if the number of data written from the client does not reach batchSize
    #@param[in] threadCount: the number of working threads to be created, the default is 1.
    #@attention: For a dimension table, threadCount must be 1
    #@param[in] partitionCol: a string indicating the partitioning column, the default is an empty string. The parameter only takes effect when threadCount>1.
    #For a partitioned table, it must be the partitioning column; for a stream table, it must be a column name; for a dimension table, the parameter does not work.
    #@param[in] compressMethods: a list of the compression methods used for each column. If unspecified, the columns are not compressed. The compression methods include:
    #"LZ4": LZ4 algorithm; "DELTA": Delta-of-delta encoding
    #@param[in] mode: The write mode. It can be Append (default) or Upsert.
    #@param[in] modeOption: The parameters of function upsert!. It only takes effect when mode is Upsert. The default is None.
    #@endif
    def __init__(self, host, port, userId, password, dbPath, tableName, useSSL, enableHighAvailability = False,
                            highAvailabilitySites = [], batchSize = 1, throttle = 1,threadCount = 1,
                            partitionCol ="", compressMethods = [], mode = "", modeOption=[]):
        self.writer = ddbcpp.multithreadedTableWriter(host, port, userId, password, dbPath, tableName, useSSL,
                            enableHighAvailability, highAvailabilitySites, batchSize, throttle,threadCount,
                            partitionCol, compressMethods, mode, modeOption)

    ##
    #@if english
    #Get the current writer status and return a MultithreadedTableWriterStatus object.
    #@return: MultithreadedTableWriterStatus object.
    def getStatus(self):
        status=MultithreadedTableWriterStatus()
        status.update(self.writer.getStatus())
        return status
    ##
    #@if english
    #Get unwritten data. Return a nested list where each element is a record.
    #The obtained data can be passed as an argument to method insertUnwrittenData.
    #@endif
    def getUnwrittenData(self):
        return self.writer.getUnwrittenData()
    ##
    #@if english
    #Insert a single row of data
    #@param[in] args: variable-length argument, indicating a row of data to be inserted
    #@return: ErrorCodeInfo object
    #@endif
    def insert(self, *args):
        errorCodeInfo=ErrorCodeInfo()
        errorCodeInfo.__dict__.update(self.writer.insert(*args))
        return errorCodeInfo
    ##
    #@if english
    #Insert unwritten data. The result is in the same format as insert. The difference is that insertUnwrittenData can insert multiple records at a time.
    #@param[in] unwrittenData: the data that has not been written to the server. You can obtain the object with method getUnwrittenData.
    #@return: ErrorCodeInfo object
    #@endif
    def insertUnwrittenData(self, unwrittenData):
        errorCodeInfo=ErrorCodeInfo()
        errorCodeInfo.__dict__.update(self.writer.insertUnwrittenData(unwrittenData))
        return errorCodeInfo
    ##
    #@if english
    #Wait until all working threads complete their tasks
    #After calling the method, MultithreadedTableWriter will wait until all working threads complete their tasks.
    #@endif
    def waitForThreadCompletion(self):
        self.writer.waitForThreadCompletion()
