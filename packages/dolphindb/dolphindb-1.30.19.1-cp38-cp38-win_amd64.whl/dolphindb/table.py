from pandas import DataFrame
from dolphindb.vector import Vector
from dolphindb.vector import FilterCond
from dolphindb.settings import get_verbose
import uuid
import copy
import numpy as np
import re
import inspect
import unicodedata
import threading


def _generate_tablename(tableName = None):
    #return "TMP_TBL_" + uuid.uuid4().hex[:8]
    if tableName is None:
        return "TMP_TBL_" + uuid.uuid4().hex[:8]
    else:
        return tableName + "_" + uuid.uuid4().hex[:8]


def _getFuncName(f):
    if isinstance(f, str):
        return f
    else:
        return f.__name__


def normalize_caseless(text):
    return unicodedata.normalize("NFKD", text.casefold())

##
#@if english
#Reference counter for internal use when caching table.
#@endif
class Counter(object):
    def __init__(self):
        self.__lock = threading.Lock()
        self.__value = 1

    ##
    #@if english
    #Increment the reference count
    #@return int: current reference count
    #@endif
    def inc(self):
        with self.__lock:
            self.__value += 1
            return self.__value

    ##
    #@if english
    #Decrease the reference count
    #@return int: current reference count
    #@endif
    def dec(self):
        with self.__lock:
            self.__value -= 1
            return self.__value

    ##
    #@if english
    #Get the current reference count
    #@return int: current reference count
    #@endif
    def val(self):
        with self.__lock:
            return self.__value

##
#@if english
#DolphinDB Table object
#@endif
class Table(object):
    ##
    #@if english
    #Constructor
    #@param[in] dbPath: database name. The default value is None
    #@param[in] data: data of the table. The default value is None
    #@param[in] tableAliasName: table alias. The default value is None
    #@param[in] partitions: The partitions to be loaded into memory. The default value is None, which means to load all partitions.
    #@param[in] inMem: (deprecated) whether to load the table into memory. True: to load the table into memory. The default value is False.
    #@param[in] schemaInited: whether the table structure has been initialized. True: the table structure has been initialized. The default value is False
    #@param[in] s: The connected session object. The default value is None
    #@param[in] needGC: whether to enable garbage collection. True: enable garbage collection. The default value is True
    #@param[in] isMaterialized: whether table is materialized True: table has been materialized. The default value is False.
    #@endif
    def __init__(self, dbPath=None, data=None, tableAliasName=None, partitions=None, inMem=False, schemaInited=False,
                 s=None, needGC=True, isMaterialized=False):
        if partitions is None:
            partitions = []
        self.__having = None
        self.__top = None
        self.__exec = False
        self.__limit = None
        self.__leftTable = None
        self.__rightTable = None
        self.__merge_for_update = False
        self.__objAddr = None
        self.isMaterialized = isMaterialized
        if tableAliasName is not None:
            self.isMaterialized = True
        if s is None:
            raise RuntimeError("session must be provided")
        self.__tableName = _generate_tablename() if not isinstance(data, str) else data
        self.__session = s  # type : session
        self.__schemaInited = schemaInited
        self.__need_gc = needGC
        if self.__need_gc:
            self.__ref = Counter()
        if not isinstance(partitions, list):
            raise RuntimeError(
                'Column names must be passed in as a list')
        if isinstance(data, dict) or isinstance(data, DataFrame):
            df = data if isinstance(data, DataFrame) else DataFrame(data)
            # if  not self.__tableName.startswith("TMP_TBL_"):
            #    self._setTableName(_generate_tablename())
            if tableAliasName is None:
                self._setTableName(_generate_tablename())
            else:
                self._setTableName(tableAliasName)
            #self.__session.upload({self.__tableName: df})
            self.__objAddr = self.__session.upload({self.__tableName: df})
            self.vecs = {}

            # self.__session.run("share %s as S%s" % (self.__tableName, self.__tableName))
            for colName in df.keys():
                self.vecs[colName] = Vector(name=colName, tableName=self.__tableName, s=self.__session)
            self._setSelect(list(self.vecs.keys()))
        elif isinstance(data, str):
            if dbPath:
                if tableAliasName:
                    self.__tableName = tableAliasName
                else:
                    self.__tableName = data
                runstr = '{tableName} = loadTable("{dbPath}", "{data}",{partitions},{inMem})'
                fmtDict = dict()
                fmtDict['tableName'] = self.__tableName
                fmtDict['dbPath'] = dbPath
                fmtDict['data'] = data
                if len(partitions) and type(partitions[0]) is not str:
                    fmtDict['partitions'] = ('[' + ','.join(str(x) for x in partitions) + ']') if len(
                        partitions) else ""
                else:
                    fmtDict['partitions'] = ('["' + '","'.join(partitions) + '"]') if len(partitions) else ""
                fmtDict['inMem'] = str(inMem).lower()
                runstr = re.sub(' +', ' ', runstr.format(**fmtDict).strip())
                self.__session.run(runstr)
                # runstr = '%s = select * from %s' %(self.__tableName, self.__tableName)
                # self.__session.run(runstr)
            else:
                pass
        elif "orca.core.frame.DataFrame" in str(data.__class__):
            df = s.run(data._var_name)
            self.__init__(data=df, s=self.__session)
        else:
            raise RuntimeError("data must be a remote dolphindb table name or dict or DataFrame")
        self._init_schema()

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        newTable = Table(data=self.__tableName, schemaInited=True, s=self.__session, needGC=self.__need_gc)
        newTable._setExec(self.isExec)
        newTable.isMaterialized = self.isMaterialized
        try:
            newTable.vecs = copy.deepcopy(self.vecs, memodict)
        except AttributeError:
            pass

        try:
            newTable.__schemaInited = copy.deepcopy(self.__schemaInited, memodict)
        except AttributeError:
            pass

        try:
            newTable.__select = copy.deepcopy(self.__select, memodict)
        except AttributeError:
            pass

        try:
            newTable.__where = copy.deepcopy(self.__where, memodict)
        except AttributeError:
            pass

        try:
            newTable.__groupby = copy.deepcopy(self.__groupby, memodict)
        except AttributeError:
            pass

        try:
            newTable.__contextby = copy.deepcopy(self.__contextby, memodict)
        except AttributeError:
            pass

        try:
            newTable.__having = copy.deepcopy(self.__having, memodict)
        except AttributeError:
            pass

        try:
            newTable.__sort = copy.deepcopy(self.__sort, memodict)
        except AttributeError:
            pass

        try:
            newTable.__top = copy.deepcopy(self.__top, memodict)
        except AttributeError:
            pass

        try: 
            newTable.__limit = copy.deepcopy(self.__limit, memodict)
        except AttributeError:
            pass

        try:
            newTable.__csort = copy.deepcopy(self.__csort, memodict)
        except AttributeError:
            pass

        try:
            if self.__need_gc:
                newTable.__ref = self.__ref
                self.__ref.inc()
        except AttributeError:
            pass

        return newTable

    def __copy__(self):
        newTable = Table(data=self.__tableName, schemaInited=True, s=self.__session, needGC=self.__need_gc)
        newTable._setExec(self.isExec)
        newTable.isMaterialized = self.isMaterialized
        try:
            newTable.vecs = copy.copy(self.vecs)
        except AttributeError:
            pass

        try:
            newTable.__schemaInited = copy.copy(self.__schemaInited)
        except AttributeError:
            pass

        try:
            newTable.__select = copy.copy(self.__select)
        except AttributeError:
            pass

        try:
            newTable.__where = copy.copy(self.__where)
        except AttributeError:
            pass

        try:
            newTable.__groupby = copy.copy(self.__groupby)
        except AttributeError:
            pass

        try:
            newTable.__contextby = copy.copy(self.__contextby)
        except AttributeError:
            pass

        try:
            newTable.__having = copy.copy(self.__having)
        except AttributeError:
            pass

        try:
            newTable.__sort = copy.copy(self.__sort)
        except AttributeError:
            pass

        try:
            newTable.__top = copy.copy(self.__top)
        except AttributeError:
            pass

        try:
            newTable.__limit = copy.copy(self.__limit)
        except AttributeError:
            pass

        try:
            newTable.__csort = copy.copy(self.__csort)
        except AttributeError:
            pass

        try:
            if self.__need_gc:
                newTable.__ref = self.__ref
                self.__ref.inc()
        except AttributeError:
            pass

        return newTable

    def __del__(self):
        if self.__need_gc:
            if self.__ref.dec() == 0:
                # print('do __del__')
                try:
                    # this is not a real table name such as join table, no need to undef.
                    if '(' in self.__tableName or ')' in self.__tableName:
                        return
                    #if self.__objAddr is None or self.__objAddr < 0:
                    #    self.__session.run("undef('{}')".format(self.__tableName))
                    #else:
                    #    self.__session.run("undef('{}', VAR, {})".format(self.__tableName, self.__objAddr))
                    if self.__session.isClosed() == False :
                        if self.__objAddr is None or self.__objAddr < 0:
                            self.__session.run("undef('{}')".format(self.__tableName))
                        else:
                            self.__session.run("undef('{}', VAR)".format(self.__tableName))
                except Exception as e:
                    print("undef table '{}' got an exception: ".format(self.__tableName))
                    print(e)
            # else:
            #     print('__del__', self.__ref.val())

    def _setSelect(self, cols):
        self.__schemaInited = True
        if isinstance(cols, tuple):
            cols = list(cols)
        if isinstance(cols, list) is False:
            cols = [cols]

        self.__select = cols

    def _init_schema(self):
        if self.__schemaInited is True:
            return
        # colNames = self.__session.run("colNames(%s)" % self.__tableName)
        schema = self.__session.run("schema(%s)" % self.__tableName)  # type: dict
        colDefs = schema.get('colDefs')  # type: DataFrame
        colNames = colDefs["name"].tolist()
        self.vecs = {}
        self.__columns = colNames
        if colNames is not None:
            if isinstance(colNames, list):
                for colName in colNames:
                    self.vecs[colName] = Vector(name=colName, tableName=self.__tableName, s=self.__session)
                self._setSelect(colNames)
            else:
                self._setSelect(colNames)

    def __getattr__(self, item):
        vecs = object.__getattribute__(self, "vecs")
        if item not in vecs:
            return object.__getattribute__(self, item)
        else:
            return vecs[item]

    def __getitem__(self, colOrCond):
        if isinstance(colOrCond, FilterCond):
            return self.where(colOrCond)
        else:
            return self.select(colOrCond)

    ##
    #@if english
    #Get table name
    #@return Name of the table in DolphinDB
    #@endif
    def tableName(self):
        return self.__tableName

    def _setTableName(self, tableName):
        self.__tableName = tableName
    
    def _getTableName(self):
        return self.__tableName

    def _setLeftTable(self, tableName):
        self.__leftTable = tableName

    def _setRightTable(self, tableName):
        self.__rightTable = tableName

    ##
    #@if english
    #Get the left table of the join
    #@return Table object: the left table of the join
    #@endif
    def getLeftTable(self):
        return self.__leftTable

    ##
    #@if english
    #Get the right table of the join
    #@return Table object: the right table of the join
    #@endif
    def getRightTable(self):
        return self.__rightTable

    ##
    #@if english
    #Get the session where the Table belongs to
    #@return session object: a session
    #@endif
    def session(self):
        return self.__session

    def _addWhereCond(self, conds):
        try:
            _ = self.__where
        except AttributeError:
            self.__where = []

        if isinstance(conds, list) or isinstance(conds, tuple):
            self.__where.extend([str(x) for x in conds])
        else:
            self.__where.append(str(conds))

    def _setSort(self, bys, ascending=True):
        if isinstance(bys, list) or isinstance(bys, tuple):
            self.__sort = [str(x) for x in bys]
        else:
            self.__sort = [str(bys)]
        if (isinstance(ascending, list) or isinstance(ascending, tuple)) and (len(self.__sort) != len(ascending)):
            raise ValueError(f"Length of ascending ({len(ascending)}) != length of bys ({len(self.__sort)})")
        if len(self.__sort) > 1:
            if isinstance(ascending, list) or isinstance(ascending, tuple):
                tem = []
                for i in range(len(self.__sort)):
                    if(ascending[i] == False):
                        tem.append(self.__sort[i] + " desc")
                    else:
                        tem.append(self.__sort[i])
                self.__sort = tem
            else:
                if(ascending == False):
                    tem = []          
                    for x in self.__sort:
                        tem.append(x + " desc")
                    self.__sort = tem
        elif len(self.__sort):
            if(ascending == False):
                self.__sort = [self.__sort[0] + " desc"]

    def _setTop(self, num):
        self.__top = str(num)

    def _setCsort(self, bys, ascending=True):
        if isinstance(bys, list) or isinstance(bys, tuple):
            self.__csort = [str(x) for x in bys]
        else:
            self.__csort = [str(bys)]
        if (isinstance(ascending, list) or isinstance(ascending, tuple)) and (len(self.__csort) != len(ascending)):
            raise ValueError(f"Length of ascending ({len(ascending)}) != length of by ({len(self.__csort)})")
        if len(self.__csort) > 1:
            if isinstance(ascending, list) or isinstance(ascending, tuple):
                tem = []
                for i in range(len(self.__csort)):
                    if(ascending[i] == False):
                        tem.append(self.__csort[i] + " desc")
                    else:
                        tem.append(self.__csort[i])
                self.__csort = tem
            else:
                if(ascending == False):
                    tem = []          
                    for x in self.__csort:
                        tem.append(x + " desc")
                    self.__csort = tem
        elif len(self.__csort):
            if(ascending == False):
                self.__csort = [self.__csort[0] + " desc"]

    def _setLimit(self, num):
        if isinstance(num, list) or isinstance(num, tuple):
            self.__limit = [str(x) for x in num]
        else:
            self.__limit = [str(num)]

    def _setWhere(self, where):
        self.__where = where

    ##
    #@if english
    #Extract the specified columns and return them in a table
    #@param[in] cols: specify the columns to be extracted from table. Can be a string, a tuple of strings or a list of strings.
    #@return a Table object of the specified columns
    #@endif
    def select(self, cols):
        selectTable = copy.copy(self)
        # print("ref of newTable: ", selectTable.__ref.val(), " self.ref: ", self.__ref.val())
        selectTable._setSelect(cols)
        if not self.isMaterialized:
            selectTable.__tableName = f"({self.showSQL()})"
        selectTable.isMaterialized = False
        return selectTable

    ##
    #@if english
    #Generate a Table object containing the specified columns. The execution result is a scalar or vector.
    #@param[in] cols: specify the columns. Can be a string, a tuple of strings or a list of strings.
    #@return a Table object of the specified columns
    #@endif
    def exec(self, cols):
        selectTable = copy.copy(self)
        selectTable._setSelect(cols)
        selectTable._setExec(True)
        if not self.isMaterialized:
            selectTable.__tableName = f"({self.showSQL()})"
        selectTable.isMaterialized = False
        return selectTable

    ##
    #@if english
    #Add query conditions
    #@param[in] conds: query conditions
    #@return Table object with query conditions
    #@endif
    def where(self, conds):
        whereTable = copy.copy(self)
        whereTable._addWhereCond(conds)
        return whereTable

    def _setGroupby(self, groupby):
        try:
            _ = self.__contextby
            raise RuntimeError('multiple context/group-by are not allowed ')
        except AttributeError:
            self.__groupby = groupby

    def _setContextby(self, contextby):
        try:
            _ = self.__groupby
            raise RuntimeError('multiple context/group-by are not allowed ')
        except AttributeError:
            self.__contextby = contextby

    def _setHaving(self, having):
        self.__having = having

    ##
    #@if english
    #Apply group by on Table with specified columns
    #@param[in] cols: name of the grouping columns
    #@return TableGroupby object after adding the groupby
    #@endif
    def groupby(self, cols):
        groupbyTable = copy.copy(self)
        groupby = TableGroupby(groupbyTable, cols)
        groupbyTable._setGroupby(groupby)
        return groupby

    ##
    #@if english
    #Specify parameter for sorting
    #@param[in] bys: the column(s) to sort on
    #@param[in] ascending: the sorting order. True: ascending order.  The default value is True
    #@return Table object after adding sort clause
    #@endif
    def sort(self, bys, ascending=True):
        sortTable = copy.copy(self)
        sortTable._setSort(bys, ascending)
        return sortTable

    ##
    #@if english
    #Retrieve the top n records from table
    #@param[in] num: the number of records to return. Must be a positive number.
    #@return Table object with the top clause
    #@endif
    def top(self, num):
        topTable = copy.copy(self)
        topTable._setTop(num)
        return topTable

    ##
    #@if english
    #Specify sorting column(s) for contextby
    #@param[in] bys: the column(s) to sort on
    #@param[in] ascending: the sorting order. True: ascending order.  The default value is True
    #@return Table object after adding csort clause
    #@endif
    def csort(self, bys, ascending=True):
        csortTable = copy.copy(self)
        csortTable._setCsort(bys, ascending)
        return csortTable

    ##
    #@if english
    #Specify parameters for limit
    #@param[in] num: When used with the contextby clause, the limit clause can use a negative integer to select a limited number of records in the end of each group. In all other cases the limit clause can only use positive integers.
    #Can pass in [x, y] to select data from row x to row y
    #@return Table object after adding the limit clause
    #@endif
    def limit(self, num):
        limitTable = copy.copy(self)
        limitTable._setLimit(num)
        return limitTable

    ##
    #@if english
    #Execute the DolphinDB SQL script
    #@param[in] expr: columns to be executed. Can be a string, tuple, or list.
    #@return SQL query result
    #@endif
    def execute(self, expr):
        if expr:
            self._setSelect(expr)
        pattern = re.compile("select", re.IGNORECASE)
        query = pattern.sub('exec', self.showSQL())
        return self.__session.run(query)

    ##
    #@if english
    #Read-only property
    #Get the row count of the Table
    #@return number of rows in the Table
    #@endif
    @property
    def rows(self):
        # if 'update' in self.showSQL().lower() or 'insert' in  self.showSQL().lower():
        #     return self.__session.run('exec count(*) from %s'% self.__tableName)
        sql = self.showSQL()
        idx = sql.lower().index("from")
        sql_new = "select count(*) as ct " + sql[idx:]
        df = self.__session.run(sql_new)
        if df.shape[0] > 1:
            return df.shape[0]
        else:
            return df['ct'].iloc[0]

    ##
    #@if english
    #read-only property
    #Get the number of columns in the Table
    #@return the number of columns in the Table
    #@endif
    @property
    def cols(self):
        if not self.__columns:
            z = self.__session.run("schema" % self.__tableName)
            self.__columns = z["colDefs"]["name"]
        return len(self.__columns)

    ##
    #@if english
    #read-only property
    #Get all column names of the Table
    #@return all column names of the Table
    #@endif
    @property
    def colNames(self):
        if not self.__columns:
            z = self.__session.run("schema" % self.__tableName)
            self.__columns = z["colDefs"]["name"]
        return self.__columns

    ##
    #@if english
    #read-only property
    #Get summary information of the Table
    #@return summary information of the Table
    #@endif
    @property
    def schema(self):
        schema = self.__session.run("schema(%s)" % self.__tableName)  # type: dict
        colDefs = schema.get('colDefs')  # type: DataFrame
        return colDefs

    ##
    #@if english
    #read-only property
    #Decide whether the Table is to be joined
    #@return bool: True means Table is to be joined
    #@endif
    @property
    def isMergeForUpdate(self):
        return self.__merge_for_update

    ##
    #@if english
    #Mark if a Table is to be joined
    #@param[in] toUpdate: True means to mark the table as to be joined
    #@endif
    def setMergeForUpdate(self, toUpdate):
        self.__merge_for_update = toUpdate

    ##
    #@if english
    #read-only property
    #Whether the SQL statement has an exec clause
    #@return bool: True means the SQL statement has added an exec clause.
    #@endif
    @property
    def isExec(self):
        return self.__exec

    def _setExec(self, isExec):
        self.__exec = isExec

    ##
    #@if english
    #Add pivot by clause to rearrange a column (or multiple columns) of a table on two dimensions. The result is a matrix.
    #@param[in] index: number of rows from the rearrangement
    #@param[in] column: number of columns from the rearrangement
    #@param[in] value: The parameters of the aggregate function. The default value is None.
    #@param[in] aggFunc: the specified aggregate function. The default value is lambda x: x
    #@return TablePivotBy object
    #@endif
    def pivotby(self, index, column, value=None, aggFunc=None):
        """
        create a pivot table.
        see www.dolphindb.com/help/pivotby.html

        :param index: the result table has the same number of rows as # unique values on this column
        :param column: the result table has the same number of columns as # unique values on this column
        :param value: column to aggregate
        :param aggFunc: aggregation function, default lambda x: x
        :return: TablePivotBy object
        """
        pivotByTable = copy.copy(self)
        return TablePivotBy(pivotByTable, index, column, value, aggFunc)

    ##
    #@if english
    #Join two table objects with ANSI SQL
    #@param[in] right: The name of the right table from local or remote server
    #@param[in] how: connection type. The options are {"left", "right", "outer", "inner"}. The default value is "inner".
    #|how | link |
    #|----: | :---- |
    #|left| https://dolphindb.com/help/SQLStatements/TableJoiners/leftjoin.html|
    #|right| https://dolphindb.com/help/SQLStatements/TableJoiners/leftjoin.html|
    #|outer| https://dolphindb.com/help/SQLStatements/TableJoiners/fulljoin.html|
    #|ineer| https://dolphindb.com/help/SQLStatements/TableJoiners/equaljoin.html|
    #@param[in] on: the columns to join on. If the column names are different in two tables, use the left_on and right_on parameters.
    #@param[in] left_on: the column to join on from the left table
    #@param[in] right_on: the column to join on from the right table
    #@param[in] sort: True means to enable sorting. The default value is False.
    #@param[in] merge_for_update: True means marking tables as to be joined.
    #@return the joined Table object
    #@attention A partitioned table can only outer join a another partitioned table. An in-memory table can only outer join another in-memory table.
    #@endif
    def merge(self, right, how='inner', on=None, left_on=None, right_on=None, sort=False, merge_for_update=False):
        howMap = {'inner': 'ej',
                  'left': 'lj',
                  'right': 'lj',
                  'outer': 'fj',
                  'left semi': 'lsj'}
        joinFunc = howMap[how]
        joinFuncPrefix = '' if sort is False or joinFunc == 'fj' else 's'

        if self.isMaterialized:
            leftTableName = self.tableName()
        else:
            leftTableName = f"({self.showSQL()})"

        if right.isMaterialized:
            rightTableName = right.tableName() if isinstance(right, Table) else right
        else:
            rightTableName = f"({right.showSQL()})"

        if how == 'right':
            leftTableName, rightTableName = rightTableName, leftTableName
            left_on, right_on = right_on, left_on

        if on is not None and not isinstance(on, list) and not isinstance(on, tuple):
            on = [on]
        if left_on is not None and not isinstance(left_on, list) and not isinstance(left_on, tuple):
            left_on = [left_on]
        if right_on is not None and not isinstance(right_on, list) and not isinstance(right_on, tuple):
            right_on = [right_on]

        if on is not None:
            left_on, right_on = on, on
        elif left_on is None and right_on is None:
            raise Exception('at least one of {\'on\', \'left_on\', \'right_on\'} must be present')
        elif left_on is not None and right_on is not None and len(left_on) != len(right_on):
            raise Exception('\'left_on\' must have the same length as \'right_on\'')

        if left_on is None and right_on is not None:
            left_on = right_on
        if right_on is None and left_on is not None:
            right_on = left_on

        leftColumnNames = ''.join(['`' + x for x in left_on])
        rightColumnNames = ''.join(['`' + x for x in right_on])
        finalTableName = '%s(%s,%s,%s,%s)' % (
            joinFuncPrefix + joinFunc, leftTableName, rightTableName, leftColumnNames, rightColumnNames)
        # print(finalTableName)
        self._init_schema()
        right._init_schema()
        joinTable = copy.copy(self)
        # leftAliasPrefix = 'lhs_' if how != 'right' else 'rhs_'
        # rightAliasPrefix = 'rhs_' if how != 'right' else 'lhs_'
        # leftSelectCols = [leftTableName + '.' + col + ' as ' + leftTableName + "_" + col for col in self._getSelect()]
        # rightSelectCols = [rightTableName + '.' + col + ' as ' + rightTableName + "_" + col for col in right._getSelect()]
        leftSelectCols = self._getSelect()
        # print(leftSelectCols)
        rightSelectCols = [rightTableName + '.' + col + ' as ' + rightTableName + "_" + col for col in
                           right._getSelect() if col in self._getSelect()]
        # print(rightSelectCols)
        joinTable._setLeftTable(self.tableName())
        joinTable._setRightTable(right.tableName())
        joinTable._setTableName(finalTableName)
        # joinTable._setSelect(leftSelectCols + rightSelectCols)
        joinTable._setSelect('*')
        if merge_for_update:
            joinTable.setMergeForUpdate(True)
        joinTable.isMaterialized = False
        return joinTable

    ##
    #@if english
    #Use asof join to join two Table objects
    #Refer to https://dolphindb.com/help/SQLStatements/TableJoiners/asofjoin.html
    #@param[in] right: The name of the right table from local or remote server
    #@param[in] on: the columns to join on. If the column names are different in two tables, use the left_on and right_on parameters.
    #@param[in] left_on: the column to join on from the left table
    #@param[in] right_on: the column to join on from the right table
    #@return the joined Table object
    #@endif
    def merge_asof(self, right, on=None, left_on=None, right_on=None):
        if self.isMaterialized:
            leftTableName = self.tableName()
        else:
            leftTableName = f"({self.showSQL()})"

        if right.isMaterialized:
            rightTableName = right.tableName() if isinstance(right, Table) else right
        else:
            rightTableName = f"({right.showSQL()})"

        if on is not None and not isinstance(on, list) and not isinstance(on, tuple):
            on = [on]
        if left_on is not None and not isinstance(left_on, list) and not isinstance(left_on, tuple):
            left_on = [left_on]
        if right_on is not None and not isinstance(right_on, list) and not isinstance(right_on, tuple):
            right_on = [right_on]

        if on is not None:
            left_on, right_on = on, on
        elif left_on is None and right_on is None:
            raise Exception('at least one of {\'on\', \'left_on\', \'right_on\'} must be present')
        elif left_on is not None and right_on is not None and len(left_on) != len(right_on):
            raise Exception('\'left_on\' must have the same length as \'right_on\'')

        if left_on is None and right_on is not None:
            left_on = right_on
        if right_on is None and left_on is not None:
            right_on = left_on

        leftColumnNames = ''.join(['`' + x for x in left_on])
        rightColumnNames = ''.join(['`' + x for x in right_on])
        finalTableName = 'aj(%s,%s,%s,%s)' % (leftTableName, rightTableName, leftColumnNames, rightColumnNames)
        self._init_schema()
        right._init_schema()
        joinTable = copy.copy(self)
        # leftAliasPrefix = 'lhs_'
        # rightAliasPrefix = 'rhs_'
        # leftSelectCols = [leftTableName + '.' + col + ' as ' + leftTableName +"_" + col for col in self._getSelect()]
        # rightSelectCols = [rightTableName + '.' + col + ' as ' + rightTableName + "_" + col for col in right._getSelect()]
        leftSelectCols = self._getSelect()
        rightSelectCols = [rightTableName + '.' + col + ' as ' + rightTableName + "_" + col for col in
                           right._getSelect() if col in self._getSelect()]
        joinTable._setLeftTable(self.tableName())
        joinTable._setRightTable(right.tableName())
        joinTable._setTableName(finalTableName)
        joinTable._setSelect('*')
        # joinTable._setSelect(leftSelectCols + rightSelectCols)
        joinTable.isMaterialized = False
        return joinTable

    ##
    #@if english
    #Use window join to join two Table objects
    #@param[in] right: The name of the right table from local or remote server
    #@param[in] leftBound: left boundary (inclusive) of the window. The default value is None.
    #@param[in] rightBound: right boundary (inclusive) of the window. The default value is None.
    #@param[in] aggFunctions: aggregate function. The default value is None.
    #@param[in] on: the columns to join on. If the column names are different in two tables, use the left_on and right_on parameters. The default value is None.
    #@param[in] left_on: the column to join on from the left table. The default value is None.
    #@param[in] right_on: the column to join on from the right table. The default value is None.
    #@param[in] prevailing: whether to use prevailing window join. True: use prevailing window join. The default value is False.
    #@return the joined Table object
    #@endif
    def merge_window(self, right, leftBound=None, rightBound=None, aggFunctions=None, on=None, left_on=None,
                     right_on=None, prevailing=False):
        leftTableName = self.tableName()
        rightTableName = right.tableName() if isinstance(right, Table) else right

        ifPrevailing = False

        if prevailing is not None:
            ifPrevailing = prevailing

        if on is not None and not isinstance(on, list) and not isinstance(on, tuple):
            on = [on]
        if left_on is not None and not isinstance(left_on, list) and not isinstance(left_on, tuple):
            left_on = [left_on]
        if right_on is not None and not isinstance(right_on, list) and not isinstance(right_on, tuple):
            right_on = [right_on]

        if on is not None:
            left_on, right_on = on, on
        elif left_on is None and right_on is None:
            raise Exception('at least one of {\'on\', \'left_on\', \'right_on\'} must be present')
        elif left_on is not None and right_on is not None and len(left_on) != len(right_on):
            raise Exception('\'left_on\' must have the same length as \'right_on\'')

        if left_on is None and right_on is not None:
            left_on = right_on
        if right_on is None and left_on is not None:
            right_on = left_on

        leftColumnNames = ''.join(['`' + x for x in left_on])
        rightColumnNames = ''.join(['`' + x for x in right_on])
        if isinstance(aggFunctions, list):
            aggFunctions = '[' + ','.join(aggFunctions) + ']'
        if ifPrevailing:
            finalTableName = 'pwj(%s,%s,%d:%d,%s,%s,%s)' % (
                leftTableName, rightTableName, leftBound, rightBound, '<' + aggFunctions + '>', leftColumnNames,
                rightColumnNames)
        else:
            finalTableName = 'wj(%s,%s,%d:%d,%s,%s,%s)' % (
                leftTableName, rightTableName, leftBound, rightBound, '<' + aggFunctions + '>', leftColumnNames,
                rightColumnNames)
        # print(finalTableName)
        self._init_schema()
        right._init_schema()
        joinTable = copy.copy(self)
        joinTable._setLeftTable(self.tableName())
        joinTable._setRightTable(right.tableName())
        joinTable._setTableName(finalTableName)
        joinTable._setSelect('*')
        return joinTable

    ##
    #@if english
    #Perform a cross join with another table and return their Cartesian product.
    #@param[in] right: The name of the right table from local or remote server
    #@return the joined Table object
    #@endif
    def merge_cross(self, right):
        leftTableName = self.tableName()
        rightTableName = right.tableName() if isinstance(right, Table) else right
        finalTableName = 'cj(%s,%s)' % (leftTableName, rightTableName)
        self._init_schema()
        right._init_schema()
        joinTable = copy.copy(self)
        joinTable._setLeftTable(self.tableName())
        joinTable._setRightTable(right.tableName())
        joinTable._setTableName(finalTableName)
        joinTable._setSelect("*")
        return joinTable

    def _getSelect(self):
        return self.__select

    def _assembleSelect(self):
        try:
            if len(self.__select) and isinstance(self.__select, list):
                return ','.join(self.__select)
            else:
                return '*'
        except AttributeError:
            return '*'
        except ValueError:
            return '*'

    def _assembleWhere(self):
        try:
            return 'where ' + ' and '.join(self.__where)
        except AttributeError:
            return ''

    def _assembleGroupbyOrContextby(self):
        try:
            return 'group by ' + ','.join(self.__groupby)
        except AttributeError:
            try:
                return 'context by ' + ','.join(self.__contextby)
            except AttributeError:
                return ''

    def _assembleOrderby(self):
        try:
            return 'order by ' + ','.join(self.__sort)
        except AttributeError:
            return ''

    def _assembleCsort(self):
        try:
            return 'csort ' + ','.join(self.__csort)
        except AttributeError:
            return ''
    
    def _assembleLimit(self):
        try:
            if (self.__limit is None):
                return ''
            if len(self.__limit) and isinstance(self.__limit, list):
                return 'limit ' + ','.join(self.__limit)
            else:
                return self.__limit
        except AttributeError:
            return ''

    ##
    #@if english
    #View SQL query
    #@return the SQL query for the current Table
    #@endif
    def showSQL(self):
        import re
        selectOrExec = "exec" if self.isExec else "select"
        queryFmt = selectOrExec + ' {top} {select} from {table} {where} {groupby} {csort} {having} {orderby} {limit}'
        fmtDict = {}
        fmtDict['top'] = ("top " + self.__top) if self.__top else ''
        fmtDict['select'] = self._assembleSelect()
        fmtDict['table'] = self.tableName()
        fmtDict['where'] = self._assembleWhere()
        fmtDict['groupby'] = self._assembleGroupbyOrContextby()
        fmtDict['csort'] = self._assembleCsort()
        fmtDict['having'] = ("having " + self.__having) if self.__having else ''
        fmtDict['orderby'] = self._assembleOrderby()
        fmtDict['limit'] = self._assembleLimit()
        query = re.sub(' +', ' ', queryFmt.format(**fmtDict).strip())
        # print(query)
        # if(self.__tableName.startswith("wj") or self.__tableName.startswith("pwj")):
        #     return self.__tableName

        if get_verbose():
            print(query)
        return query

    ##
    #@if english
    #Append data to Table and execute at once
    #@param[in] table: Table object to be appended
    #@return the appended Table object
    #@attention the data in the DolphinDB server will be modified immediately
    #@endif
    def append(self, table):
        if not isinstance(table, Table):
            raise RuntimeError("Only DolphinDB Table object is accepted")

        runstr = "%s.append!(%s)" % (self.tableName(), table.tableName())
        self.__session.run(runstr)
        return self

    ##
    #@if english
    #Update in-memory table. Must be called to be executed.
    #@param[in] cols: List of names of columns to be updated
    #@param[in] vals: A list of values to be updated
    #@return TableUpdate object
    #@endif
    def update(self, cols, vals):
        tmp = copy.copy(self)
        contextby = self.__contextby if hasattr(self, '__contextby') else None
        having = self.__having if hasattr(self, '__having') else None
        updateTable = TableUpdate(t=tmp, cols=cols, vals=vals, contextby=contextby, having=having)
        updateTable._setMergeForUpdate(self.isMergeForUpdate)
        return updateTable
    
    ##
    #@if english
    #Rename table
    #@param[in] newName: new table name
    #@endif
    def rename(self, newName):
        self.__session.run(newName + '=' + self.tableName())
        self.__tableName = newName

    ##
    #@if english
    #Delete table
    #@return TableDelete object
    #@endif
    def delete(self):
        tmp = copy.copy(self)
        delTable = TableDelete(t=tmp)
        return delTable

    ##
    #@if english
    #Delete columns
    #@param[in] cols: List of columns to be deleted. If an empty list is passed in, all columns of the current Table will be deleted.
    #@return TableDelete object
    #@endif
    def drop(self, cols):
        if cols is not None and len(cols) and isinstance(cols, list):
            runstr = '{table}.drop!([{cols}])'
            fmtDict = dict()
            fmtDict['table'] = self.tableName()
            fmtDict['cols'] = '"' + '","'.join(cols) + '"'
            query = re.sub(' +', ' ', runstr.format(**fmtDict).strip())
            for col in cols:
                for colName in self.__select:
                    if col.lower() == colName.lower():
                        self.__select.remove(colName)
            self.__session.run(query)
        else:
            runstr = '{table}.drop!([{cols}])'
            fmtDict = dict()
            fmtDict['table'] = self.tableName()
            fmtDict['cols'] = "'" + cols + "'"
            query = re.sub(' +', ' ', runstr.format(**fmtDict).strip())
            for colName in self.__select:
                if cols.lower() == colName.lower():
                    self.__select.remove(colName)
        return self

    ##
    #@if english
    #Save execution result as an in-memory table with a specified name.
    #@param[in] newTableName: new table name
    #@return Table object saved with the new table name
    #@endif
    def executeAs(self, newTableName):
        st = newTableName + "=(" + self.showSQL() + ")"
        # print(st)
        self.__session.run(st)
        return Table(data=newTableName, s=self.__session)

    ##
    #@if english
    #Group by specified columns and perform aggregation
    #@param[in] cols: name of the columns to context by
    #@return TableContextby object after adding context by clause
    #@endif
    def contextby(self, cols):
        contextbyTable = copy.copy(self)
        contextbyTable.__merge_for_update = self.__merge_for_update
        contextby = TableContextby(contextbyTable, cols)
        contextbyTable._setContextby(contextby)
        contextbyTable._setTableName(self.tableName())
        return contextby

    ##
    #@if english
    #Calculate Least Squares Regression Coefficients
    #@param[in] Y: dependent variable, column name
    #@param[in] X: argument, list of column names
    #@param[in] INTERCEPT: Whether to include the intercept in the regression. The default value is true, meaning that the system automatically adds a column of "1" to X to generate the intercept.
    #@return a dictionary with ANOVA, RegressionStat, Cofficient and Residual.
    #Refer to https://dolphindb.com/help/FunctionsandCommands/FunctionReferences/o/ols.html
    #@endif
    def ols(self, Y, X, INTERCEPT=True):
        myY = ""
        myX = []

        if isinstance(Y, str):
            myY = Y
        else:
            raise ValueError("Y must be a column name")
        if isinstance(X, str):
            myX = [X]
        elif isinstance(X, list):
            myX = X
        else:
            raise ValueError("X must be a column name or a list of column names")
        if not len(myY) or not len(myX):
            raise ValueError("Invalid Input data")
        schema = self.__session.run("schema(%s)" % self.__tableName)
        if 'partitionColumnName' in schema and schema['partitionColumnName']:
            dsstr = "sqlDS(<SQLSQL>)".replace('SQLSQL', self.showSQL()).replace('select select', 'select')
            runstr = "olsEx({ds},{Y},{X},{INTERCEPT},2)"
            fmtDict = dict()
            fmtDict['table'] = self.tableName()
            fmtDict['Y'] = '"' + myY + '"'
            fmtDict['X'] = str(myX)
            fmtDict['ds'] = dsstr
            fmtDict['INTERCEPT'] = str(INTERCEPT).lower()
            query = re.sub(' +', ' ', runstr.format(**fmtDict).strip())
            # print(query)
            return self.__session.run(query)
        else:
            runstr = "z=exec ols({Y},{X},{INTERCEPT},2) from {table}"
            fmtDict = dict()
            fmtDict['table'] = self.tableName()
            fmtDict['Y'] = myY
            fmtDict['X'] = str(myX)
            fmtDict['INTERCEPT'] = str(INTERCEPT).lower()
            query = re.sub(' +', ' ', runstr.format(**fmtDict).strip())
            # print(query)
            return self.__session.run(query)

    ##
    #@if english
    #Execute SQL statement and return a DataFrame object
    #@return DataFrame object
    #@endif
    def toDF(self):
        """
        execute sql query on remote dolphindb server

        :return: query result as a pandas.DataFrame object
        """
        self._init_schema()
        query = self.showSQL()
        df = self.__session.run(query)  # type: DataFrame
        return df

    ##
    #@if english
    #Execute SQL statement and return a List object
    #@return list[numpy.ndarray...]
    #@attention If the table contains columns of array vectors, the system will try to convert them to NumPy 2D arrays. The conversion will fail if the size of the rows in the array vector are different.
    #@endif
    def toList(self):
        """
        execute sql query on remote dolphindb server

        :return: query result as a list object
        """
        self._init_schema()
        query = self.showSQL()
        list = self.__session.run(query,pickleTableToList=True)  # type: DataFrame
        return list

    toDataFrame = toDF

##
#@if english
#Table object to be deleted
#@endif
class TableDelete(object):
    ##
    #@if english
    #Constructor
    #@param[in] t: table object to be deleted
    #@endif
    def __init__(self, t):
        self.__t = t

    def _assembleWhere(self):
        try:
            return 'where ' + ' and '.join(self.__where)
        except AttributeError:
            return ''

    def _addWhereCond(self, conds):
        try:
            _ = self.__where
        except AttributeError:
            self.__where = []

        if isinstance(conds, list) or isinstance(conds, tuple):
            self.__where.extend([str(x) for x in conds])
        else:
            self.__where.append(str(conds))

    ##
    #@if english
    #Add query conditions
    #@param[in] conds: query conditions
    #@return A Table object with query conditions
    #@endif
    def where(self, conds):
        self._addWhereCond(conds)
        return self

    ##
    #@if english
    #View SQL query
    #@return the SQL statement for the current TableDelete object
    #@endif
    def showSQL(self):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        caller = calframe[1][3]
        if caller != 'execute' and caller != 'print' and caller != "str" and caller != '<module>':
            return self.__t.showSQL()
        queryFmt = 'delete from {table} {where}'
        fmtDict = {}
        fmtDict['table'] = self.__t.tableName()
        fmtDict['where'] = self._assembleWhere()
        query = re.sub(' +', ' ', queryFmt.format(**fmtDict).strip())
        return query

    ##
    #@if english
    #Execute the DolphinDB SQL script
    #@return SQL query result as pandas.DataFrame
    #@endif
    def execute(self):
        query = self.showSQL()
        self.__t.session().run(query)  # type: DataFrame
        return self.__t

    ##
    #@if english
    #Execute SQL statement and return a DataFrame object
    #@return DataFrame object
    #@endif
    def toDF(self):
        query = self.showSQL()

        df = self.__t.session().run(query)  # type: DataFrame

        return df

##
#@if english
#Table object to be updated
#@endif
class TableUpdate(object):
    ##
    #@if english
    #Constructor
    #@param[in] t: table object to be updated
    #@param[in] cols: List of names of columns to be updated
    #@param[in] vals: A list of values corresponding to the columns to be updated
    #@param[in] contextby: Whether SQL query contains a contextby clause. True means there is.
    #@param[in] having: Whether SQL query contains a having clause. True means there is.
    #@endif
    def __init__(self, t, cols, vals, contextby=None, having=None):
        self.__t = t
        self.__cols = cols
        self.__vals = vals
        self.__contextby = contextby
        self.__having = having
        self.__merge_for_update = False

    def _setMergeForUpdate(self, toMerge):
        self.__merge_for_update = toMerge

    def _assembleUpdate(self):
        query = ""
        for col, val in zip(self.__cols, self.__vals):
            query += col + "=" + val + ","
        return query[:-1]

    def _assembleWhere(self):
        try:
            return 'where ' + ' and '.join(self.__where)
        except AttributeError:
            return ''

    def _addWhereCond(self, conds):
        try:
            _ = self.__where
        except AttributeError:
            self.__where = []

        if isinstance(conds, list) or isinstance(conds, tuple):
            self.__where.extend([str(x) for x in conds])
        else:
            self.__where.append(str(conds))

    ##
    #@if english
    #Add query conditions
    #@param[in] conds: query conditions
    #@return A Table object with query conditions
    #@endif
    def where(self, conds):
        self._addWhereCond(conds)
        return self

    ##
    #@if english
    #View SQL query
    #@return the SQL statement for the current TableUpdate object
    #@endif
    def showSQL(self):
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        caller = calframe[1][3]
        if caller != 'execute' and caller != 'print' and caller != "str" and caller != '<module>':
            return self.__t.showSQL()
        if not self.__merge_for_update:
            queryFmt = 'update {table} set {update} {where} {contextby} {having}'
            fmtDict = {}
            fmtDict['update'] = self._assembleUpdate()
            fmtDict['table'] = self.__t.tableName()
            fmtDict['where'] = self._assembleWhere()
            if self.__contextby:
                fmtDict['contextby'] = 'context by ' + ','.join(self.__contextby)
            else:
                fmtDict['contextby'] = ""
            if self.__having:
                fmtDict['having'] = ' having ' + self.__having
            else:
                fmtDict['having'] = ""
            query = re.sub(' +', ' ', queryFmt.format(**fmtDict).strip())
            if get_verbose():
                print(query)
            return query
        else:
            if self.__t.getLeftTable() is None:
                raise Exception("Join for update missing left table!")
            queryFmt = 'update {table} set {update} from {joinTable} {where} {contextby} {having}'
            fmtDict = {}
            fmtDict['update'] = self._assembleUpdate()
            fmtDict['table'] = self.__t.getLeftTable()
            fmtDict['joinTable'] = self.__t.tableName()
            fmtDict['where'] = self.__t._assembleWhere()
            if self.__contextby:
                fmtDict['contextby'] = 'context by ' + ','.join(self.__t.__contextby)
            else:
                fmtDict['contextby'] = ""
            if self.__having:
                fmtDict['having'] = ' having ' + self.__having
            else:
                fmtDict['having'] = ""
            query = re.sub(' +', ' ', queryFmt.format(**fmtDict).strip())
            self.__t.setMergeForUpdate(False)
            if get_verbose():
                print(query)
            return query

    ##
    #@if english
    #Execute the DolphinDB SQL script
    #@return SQL query result as pandas.DataFrame
    #@endif
    def execute(self):
        query = self.showSQL()
        #print(query)
        self.__t.session().run(query)  # type: DataFrame
        return Table(data=self.__t.tableName(), s=self.__t.session())

    ##
    #@if english
    #Execute SQL statement and return a DataFrame object
    #@return DataFrame object
    #@endif
    def toDF(self):
        query = self.showSQL()
        df = self.__t.session().run(query)  # type: DataFrame
        return df

##
#@if english
#Add pivot by clause to rearrange a column (or multiple columns) of a table on two dimensions. The result is a matrix.
#@endif
class TablePivotBy(object):
    ##
    #@if english
    #Constructor
    #@param[in] t: table object
    #@param[in] index: number of rows from the rearrangement
    #@param[in] column: number of columns from the rearrangement
    #@param[in] value: The parameters of the aggregate function. The default value is None.
    #@param[in] agg: the specified aggregate function. The default value is lambda x: x
    #@endif
    def __init__(self, t, index, column, value=None, agg=None):
        self.__row = index
        self.__column = column
        self.__val = value
        self.__t = t
        self.__agg = agg

    ##
    #@if english
    #Execute SQL statement and return a DataFrame object
    #@return DataFrame object
    #@endif
    def toDF(self):
        query = self.showSQL()
        if get_verbose():
            print(query)
        df = self.__t.session().run(query)  # type: DataFrame

        return df

    toDataFrame = toDF

    def _assembleSelect(self):
        if self.__val is not None:
            return self.__val if self.__agg is None else _getFuncName(self.__agg) + '(' + self.__val + ')'
        return None

    def _assembleTableSelect(self):
        return self.__t._assembleSelect()

    def _assembleWhere(self):
        return self.__t._assembleWhere()

    def _assemblePivotBy(self):
        return 'pivot by ' + self.__row + ',' + self.__column

    ##
    #@if english
    #Save execution result as an in-memory table with a specified name.
    #@param[in] newTableName: new table name
    #@return Table object saved with the new table name
    #@endif
    def executeAs(self, newTableName):
        self.__session.run(newTableName + "=" + self.showSQL())
        return Table(data=newTableName, s=self.__t.session())

    ##
    #@if english
    #View SQL query
    #@return the SQL query for the current Table
    #@endif
    def showSQL(self):
        import re
        selectOrExec = "exec" if self.__t.isExec else "select"
        queryFmt = selectOrExec + ' {select} from {table} {where} {pivotby}'
        fmtDict = {}
        select = self._assembleSelect()
        if select is not None:
            fmtDict['select'] = select
        else:
            fmtDict['select'] = self._assembleTableSelect()
        fmtDict['table'] = self.__t.tableName()
        fmtDict['where'] = self._assembleWhere()
        fmtDict['pivotby'] = self._assemblePivotBy()
        query = re.sub(' +', ' ', queryFmt.format(**fmtDict).strip())
        return query

    ##
    #@if english
    #Execute query and return the specified columns
    #@param[in] colName: a string indicating the column name.
    #@return return numpy.array
    #@endif
    def selectAsVector(self, colName):
        if colName:
            self._setSelect(colName)
        pattern = re.compile("select", re.IGNORECASE)
        query = pattern.sub('exec', self.showSQL())
        return self.__session.run(query)


##
#@if english
#The table object to which the group by clause is to be added
#@endif
class TableGroupby(object):
    ##
    #@if english
    #Constructor
    #@param[in] t: table object to be added the group by clause
    #@param[in] groupBys: grouping column(s)
    #@param[in] having: Whether SQL query contains a having clause. True means there is.
    #@endif
    def __init__(self, t, groupBys, having=None):
        if isinstance(groupBys, list):
            self.__groupBys = groupBys
        else:
            self.__groupBys = [groupBys]
        self.__having = having
        self.__t = t  # type: Table

    ##
    #@if english
    #Specify parameter for sorting
    #@param[in] bys: the column(s) to sort on
    #@param[in] ascending: the sorting order. True: ascending order.  The default value is True
    #@return Table object after adding sort clause
    #@endif
    def sort(self, bys, ascending=True):
        sortTable = copy.copy(self.__t)
        sortTable._setSort(bys, ascending)
        return TableGroupby(sortTable, self.__groupBys, self.__having)

    ##
    #@if english
    #Specify sorting parameters for context by
    #@param[in] bys: the column to sort on
    #@param[in] ascending: the sorting order. True: ascending order.  The default value is True
    #@return Table object after adding csort clause
    #@endif
    def csort(self, bys, ascending=True):
        csortTable = copy.copy(self.__t)
        csortTable._setCsort(bys, ascending)
        return TableGroupby(csortTable, self.__groupBys, self.__having)

    ##
    #@if english
    #Save execution result as an in-memory table with a specified name.
    #@param[in] newTableName: new table name
    #@return Table object saved with the new table name
    #@endif
    def executeAs(self, newTableName):
        st = newTableName + "=" + self.showSQL()
        # print(st)
        self.__t.session().run(st)
        return Table(data=newTableName, s=self.__t.session())

    def __getitem__(self, item):
        selectTable = self.__t.select(item)
        return TableGroupby(selectTable, groupBys=self.__groupBys, having=self.__having)

    def __iter__(self):
        self.__groupBysIdx = 0
        return self

    ##
    #@if english
    #Get the name of the next group by column
    #@return column name
    #@endif
    def next(self):
        try:
            result = self.__groupBys[self.__groupBysIdx]
        except IndexError:
            raise StopIteration
        self.__groupBysIdx += 1
        return result

    def __next__(self):
        return self.next()

    ##
    #@if english
    #Add having clause
    #@param[in] expr: expression for the having clause
    #@return table object after adding the having clause
    #@endif
    def having(self, expr):
        havingTable = copy.copy(self.__t)
        self.__having = expr
        havingTable._setHaving(self.__having)
        return havingTable

    ##
    #@if english
    #Calculate Least Squares Regression Coefficients
    #@param[in] Y: dependent variable, column name
    #@param[in] X: argument, list of column names
    #@param[in] INTERCEPT: Whether to include the intercept in the regression. The default value is true, meaning that the system automatically adds a column of "1" to X to generate the intercept.
    #@return a dictionary with ANOVA, RegressionStat, Cofficient and Residual.
    #Refer to https://dolphindb.com/help/FunctionsandCommands/FunctionReferences/o/ols.html
    #@endif
    def ols(self, Y, X, INTERCEPT=True):
        return self.__t.ols(Y=Y, X=X, INTERCEPT=INTERCEPT)

    ##
    #@if english
    #Execute query and return the specified column
    #@param[in] colName: a string indicating the column name.
    #@return return numpy.array
    #@endif
    def selectAsVector(self, colName):
        if colName:
            self._setSelect(colName)
        pattern = re.compile("select", re.IGNORECASE)
        query = pattern.sub('exec', self.showSQL())
        return self.__session.run(query)

    ##
    #@if english
    #View SQL query
    #@return the SQL query for the current Table
    #@endif
    def showSQL(self):
        return self.__t.showSQL()

    ##
    #@if english
    #Apply group by on all columns
    #@param[in] func: string or list of strings indicating the aggregate function(s)
    #@return table object after aggregation
    #@endif
    def agg(self, func):
        selectCols = self.__t._getSelect()
        if isinstance(func, list):
            selectCols = [_getFuncName(f) + '(' + x + ')' for x in selectCols for f in
                          func]  # if x not in self.__groupBys
        elif isinstance(func, dict):
            funcDict = {}
            for colName, f in func.items():
                funcDict[colName] = f if isinstance(f, list) else [f]
            selectCols = [_getFuncName(f) + '(' + x + ')' for x, funcs in funcDict.items() for f in
                          funcs]  # if x not in self.__groupBys
        elif isinstance(func, str):
            selectCols = [_getFuncName(func) + '(' + x + ')' for x in selectCols]  # if x not in self.__groupBys
        else:
            raise RuntimeError(
                'invalid func format, func: aggregate function name or a list of aggregate function names'
                ' or a dict of column label/expression->func')
        return self.__t.select(selectCols)

    ##
    #@if english
    #Execute the aggregate function sum
    #@return table object after aggregation
    #@endif
    def sum(self):
        return self.agg('sum')

    ##
    #@if english
    #Execute the aggregate function avg
    #@return table object after aggregation
    #@endif
    def avg(self):
        return self.agg('avg')

    ##
    #@if english
    #Execute the aggregate function count
    #@return table object after aggregation
    #@endif
    def count(self):
        return self.agg('count')

    ##
    #@if english
    #Execute the aggregate function max
    #@return table object after aggregation
    #@endif
    def max(self):
        return self.agg('max')

    ##
    #@if english
    #Execute the aggregate function min
    #@return table object after aggregation
    #@endif
    def min(self):
        return self.agg('min')

    ##
    #@if english
    #Execute the aggregate function first
    #@return table object after aggregation
    #@endif
    def first(self):
        return self.agg('first')

    ##
    #@if english
    #Execute the aggregate function last
    #@return table object after aggregation
    #@endif
    def last(self):
        return self.agg('last')

    ##
    #@if english
    #Execute aggregate function size
    #@return table object after aggregation
    #@endif
    def size(self):
        return self.agg('size')

    ##
    #@if english
    #Execute the aggregate function sum2
    #@return table object after aggregation
    #@endif
    def sum2(self):
        return self.agg('sum2')

    ##
    #@if english
    #Execute aggregate function std
    #@return table object after aggregation
    #@endif
    def std(self):
        return self.agg('std')

    ##
    #@if english
    #execute aggregate function var
    #@return table object after aggregation
    #@endif
    def var(self):
        return self.agg('var')

    ##
    #@if english
    #Execute the aggregate function prod
    #@return table object after aggregation
    #@endif
    def prod(self):
        return self.agg('prod')

    ##
    #@if english
    #Perform aggregate function(s) on specified column(s)
    #@param[in] func: string or list of strings indicating the aggregate function(s)
    #@param[in] cols: ( x, y ) tuple or list of ( x, y ) tuples, where x and y are column labels or column expressions
    #@return Table object
    #@endif
    def agg2(self, func, cols):
        if isinstance(cols, list) is False:
            cols = [cols]
        if isinstance(func, list) is False:
            func = [func]
        if np.sum([1 for x in cols if isinstance(x, tuple) is False or len(x) != 2]):
            raise RuntimeError('agg2 only accepts (x,y) pair or a list of (x,y) pair as cols')
        funcName = [_getFuncName(f) + '(' + x + ',' + y + ')' for f in func for x, y in cols]
        if funcName:
            return self.__t.select(funcName)
        return self.__t.select(self.__t._getSelect())

    ##
    #@if english
    #Perform aggregate function wavg on specified column(s)
    #@param[in] cols: ( x, y ) tuple or list of ( x, y ) tuples, where x and y are column labels or column expressions
    #@return Table object
    #@endif
    def wavg(self, cols):
        return self.agg2('wavg', cols)

    ##
    #@if english
    #Perform aggregate function wsum on specified column(s)
    #@param[in] cols: ( x, y ) tuple or list of ( x, y ) tuples, where x and y are column labels or column expressions
    #@return Table object
    #@endif
    def wsum(self, cols):
        return self.agg2('wsum', cols)

    ##
    #@if english
    #Perform aggregate function cover on specified column(s)
    #@param[in] cols: ( x, y ) tuple or list of ( x, y ) tuples, where x and y are column labels or column expressions
    #@return Table object
    #@endif
    def covar(self, cols):
        return self.agg2('covar', cols)

    ##
    #@if english
    #Perform aggregate function corr on specified column(s)
    #@param[in] cols: ( x, y ) tuple or list of ( x, y ) tuples, where x and y are column labels or column expressions
    #@return Table object
    #@endif
    def corr(self, cols):
        return self.agg2('corr', cols)

    ##
    #@if english
    #Execute SQL statement and return a DataFrame object
    #@return DataFrame object
    #@endif
    def toDF(self):
        query = self.showSQL()
        # print(query)
        df = self.__t.session().run(query)  # type: DataFrame
        return df

##
#@if english
#The table object to add the context by clause
#@endif
class TableContextby(object):
    ##
    #@if english
    #Constructor
    #@param[in] t: the table object to add the context by clause
    #@param[in] contextBys: names of columns to be grouped for aggregation
    #@param[in] having: Whether SQL query contains a having clause. True means there is.
    #@endif
    def __init__(self, t, contextBys, having=None):
        if isinstance(contextBys, list):
            self.__contextBys = contextBys
        else:
            self.__contextBys = [contextBys]
        self.__t = t  # type: Table
        self.__having = having

    ##
    #@if english
    #Specify parameter for sorting
    #@param[in] bys: the column(s) to sort on
    #@param[in] ascending: the sorting order. True: ascending order.  The default value is True
    #@return Table object after adding sort clause
    #@endif
    def sort(self, bys, ascending=True):
        sortTable = copy.copy(self.__t)
        sortTable._setSort(bys, ascending)
        return TableContextby(sortTable, self.__contextBys)

    ##
    #@if english
    #Specify sorting column(s) for contextby
    #@param[in] bys: the column(s) to sort on
    #@param[in] ascending: the sorting order. True: ascending order.  The default value is True
    #@return Table object after adding csort clause
    #@endif
    def csort(self, bys, ascending=True):
        csortTable = copy.copy(self.__t)
        csortTable._setCsort(bys, ascending)
        return TableContextby(csortTable, self.__contextBys)

    ##
    #@if english
    #Set having clause
    #@param[in] expr: expression for the having clause
    #@return table object after adding the having clause
    #@endif
    def having(self, expr):
        havingTable = copy.copy(self.__t)
        self.__having = expr
        havingTable._setHaving(self.__having)
        return havingTable

    def __getitem__(self, item):
        selectTable = self.__t.select(item)
        return TableContextby(selectTable, contextBys=self.__contextBys)

    def __iter__(self):
        self.__contextBysIdx = 0
        return self

    ##
    #@if english
    #Get the name of the next grouping column for context by
    #@return column name
    #@endif
    def next(self):
        try:
            result = self.__contextBys[self.__contextBysIdx]
        except IndexError:
            raise StopIteration
        self.__contextBysIdx += 1
        return result

    def __next__(self):
        return self.next()

    ##
    #@if english
    #Execute query and return the specified column
    #@param[in] colName: a string indicating the column name
    #@return numpy.array
    #@endif
    def selectAsVector(self, colName):
        if colName:
            self._setSelect(colName)
        pattern = re.compile("select", re.IGNORECASE)
        query = pattern.sub('exec', self.showSQL())
        return self.__session.run(query)

    ##
    #@if english
    #Set the top clause to retrieve the first n records from a Table.
    #@param[in] num: The number of records to return. Must be a positive number.
    #@return the Table object with the top clause
    #@endif
    def top(self, num):
        return self.__t.top(num=num)

    ##
    #@if english
    #Set the limit clause to retrieve the specified number of records from a Table.
    #@param[in] num: When used with the context by clause, the limit clause can use a negative integer to select a limited number of records in the end of each group. In all other cases the limit clause can only use positive integers.
    #can pass in [x, y] to select data from row x to row y
    #@return the Table object with the limit clause
    #@endif
    def limit(self, num):
        return self.__t.limit(num=num)

    ##
    #@if english
    #Set having clause
    #@param[in] expr: expression for the having clause
    #@return table object after adding the having clause
    #@endif
    def having(self, expr):
        havingTable = copy.copy(self.__t)
        self.__having = expr
        havingTable._setHaving(self.__having)
        return havingTable

    ##
    #@if english
    #Save execution result as an in-memory table with a specified name.
    #@param[in] newTableName: new table name
    #@return Table object saved with the new table name
    #@endif
    def executeAs(self, newTableName):
        st = newTableName + "=" + self.showSQL()
        # print(st)
        self.__t.session().run(st)
        return Table(data=newTableName, s=self.__t.session())

    ##
    #@if english
    #View SQL query
    #@return the SQL query for the current Table
    #@endif
    def showSQL(self):
        return self.__t.showSQL()

    ##
    #@if english
    #Apply context by on all columns except the grouping columns
    #@param[in] func: string or list of strings indicating the aggregate function(s)
    #@return table object after aggregation
    #@endif
    def agg(self, func):
        selectCols = self.__t._getSelect()
        if isinstance(func, list):
            selectCols = [_getFuncName(f) + '(' + x + ')' for x in selectCols for f in func if
                          x not in self.__contextBys]
        elif isinstance(func, dict):
            funcDict = {}
            for colName, f in func.items():
                funcDict[colName] = f if isinstance(f, list) else [f]
            selectCols = [_getFuncName(f) + '(' + x + ')' for x, funcs in funcDict.items() for f in funcs if
                          x not in self.__contextBys]
        elif isinstance(func, str):
            selectCols = [_getFuncName(func) + '(' + x + ')' for x in selectCols if x not in self.__contextBys]
        else:
            raise RuntimeError(
                'invalid func format, func: aggregate function name or a list of aggregate function names'
                ' or a dict of column label/expression->func')
        columns = self.__contextBys[:]
        columns.extend(selectCols)
        lowered = [x.lower() for x in columns]
        # for x in self.__t._getSelect():
        #     if x.lower() not in lowered:
        #         columns.append(x)
        #         print(x,'sss')
        return self.__t.select(columns)

    ##
    #@if english
    #Perform aggregate function(s) on specified columns
    #@param[in] func: string or list of strings indicating the aggregate function(s)
    #@param[in] cols: ( x, y ) tuple or list of ( x, y ) tuples, where x and y are column labels or column expressions
    #@return Table object
    #@endif
    def agg2(self, func, cols):
        if isinstance(cols, list) is False:
            cols = [cols]
        if isinstance(func, list) is False:
            func = [func]
        if np.sum([1 for x in cols if isinstance(x, tuple) is False or len(x) != 2]):
            raise RuntimeError('agg2 only accepts (x,y) pair or a list of (x,y) pair as cols')
        funcName = [_getFuncName(f) + '(' + x + ',' + y + ')' for f in func for x, y in cols]
        if funcName:
            self.__t._getSelect().extend(funcName)
        return self.__t.select(self.__t._getSelect())

    ##
    #@if english
    #Update in-memory table. Must be used together with execute.
    #@param[in] cols: List of names of columns to be updated
    #@param[in] vals: A list of values corresponding to the columns to be updated
    #@return TableUpdate object
    #@endif
    def update(self, cols, vals):
        updateTable = TableUpdate(t=self.__t, cols=cols, vals=vals, contextby=self.__contextBys, having=self.__having)
        return updateTable

    ##
    #@if english
    #Execute the aggregate function sum
    #@return table object after aggregation
    #@endif
    def sum(self):
        return self.agg('sum')

    ##
    #@if english
    #Execute the aggregate function avg
    #@return table object after aggregation
    #@endif
    def avg(self):
        return self.agg('avg')

    ##
    #@if english
    #Execute the aggregate function count
    #@return table object after aggregation
    #@endif
    def count(self):
        return self.agg('count')

    ##
    #@if english
    #Execute the aggregate function max
    #@return table object after aggregation
    #@endif
    def max(self):
        return self.agg('max')

    ##
    #@if english
    #Execute the aggregate function min
    #@return table object after aggregation
    #@endif
    def min(self):
        return self.agg('min')

    ##
    #@if english
    #Execute the aggregate function first
    #@return table object after aggregation
    #@endif
    def first(self):
        return self.agg('first')

    ##
    #@if english
    #Execute the aggregate function last
    #@return table object after aggregation
    #@endif
    def last(self):
        return self.agg('last')

    ##
    #@if english
    #Execute aggregate function size
    #@return table object after aggregation
    #@endif
    def size(self):
        return self.agg('size')

    ##
    #@if english
    #Execute the aggregate function sum2
    #@return table object after aggregation
    #@endif
    def sum2(self):
        return self.agg('sum2')

    ##
    #@if english
    #Execute aggregate function std
    #@return table object after aggregation
    #@endif
    def std(self):
        return self.agg('std')

    ##
    #@if english
    #execute aggregate function var
    #@return table object after aggregation
    #@endif
    def var(self):
        return self.agg('var')

    ##
    #@if english
    #Execute the aggregate function prod
    #@return table object after aggregation
    #@endif
    def prod(self):
        return self.agg('prod')

    ##
    #@if english
    #Execute the aggregate function cumsum
    #@return table object after aggregation
    #@endif
    def cumsum(self):
        return self.agg('cumsum')

    ##
    #@if english
    #Execute the aggregate function cummax
    #@return table object after aggregation
    #@endif
    def cummax(self):
        return self.agg('cummax')

    ##
    #@if english
    #Execute the aggregate function cumprod
    #@return table object after aggregation
    #@endif
    def cumprod(self):
        return self.agg('cumprod')

    ##
    #@if english
    #Execute the aggregate function cummin
    #@return table object after aggregation
    #@endif
    def cummin(self):
        return self.agg('cummin')

    ##
    #@if english
    #Execute aggregate function wavg
    #@param[in] cols: ( x, y ) tuple or list of ( x, y ) tuples, where x and y are column labels or column expressions
    #@return table object after aggregation
    #@endif
    def wavg(self, cols):
        return self.agg2('wavg', cols)

    ##
    #@if english
    #Execute the aggregate function wsum
    #@param[in] cols: ( x, y ) tuple or list of ( x, y ) tuples, where x and y are column labels or column expressions
    #@return table object after aggregation
    #@endif
    def wsum(self, cols):
        return self.agg2('wsum', cols)

    ##
    #@if english
    #Execute the aggregate function covar
    #@param[in] cols: ( x, y ) tuple or list of ( x, y ) tuples, where x and y are column labels or column expressions
    #@return table object after aggregation
    #@endif
    def covar(self, cols):
        return self.agg2('covar', cols)

    ##
    #@if english
    #Execute the aggregate function corr
    #@param[in] cols: ( x, y ) tuple or list of ( x, y ) tuples, where x and y are column labels or column expressions
    #@return Table object
    #@endif
    def corr(self, cols):
        return self.agg2('corr', cols)

    ##
    #@if english
    #Execute the aggregate function eachPre
    #@param[in] args: the function and parameters of eachPre
    #@attention args [0]: the function. args [1]: a vector, matrix or table. Apply args [0] over all pairs of consecutive elements of args [1].
    #Reference link: https://dolphindb.com/help/Functionalprogramming/TemplateFunctions/eachPre.html
    #@return table object after aggregation
    #@endif
    def eachPre(self, args):
        return self.agg2('eachPre', args)

    ##
    #@if english
    #Execute the SQL statement and return a DataFrame object
    #@return DataFrame object
    #@endif
    def toDF(self):
        query = self.showSQL()
        # print(query)
        df = self.__t.session().run(query)  # type : DataFrame
        return df


wavg = TableGroupby.wavg
wsum = TableGroupby.wsum
covar = TableGroupby.covar
corr = TableGroupby.corr
count = TableGroupby.count
max = TableGroupby.max
min = TableGroupby.min
sum = TableGroupby.sum
sum2 = TableGroupby.sum2
size = TableGroupby.size
avg = TableGroupby.avg
std = TableGroupby.std
prod = TableGroupby.prod
var = TableGroupby.var
first = TableGroupby.first
last = TableGroupby.last
eachPre = TableContextby.eachPre
cumsum = TableContextby.cumsum
cumprod = TableContextby.cumprod
cummax = TableContextby.cummax
cummin = TableContextby.cummin
