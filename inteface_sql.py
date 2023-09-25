import sqlite3
import datetime
from datetime import date
import calendar
import random

connection = None
chitRuleTableNumber = 0


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)


def initDataBase():
    """to initialize data base"""
    retVar = False
    global connection

    try:
        # connecting to the database
        connection = sqlite3.connect("LpChitDb.db")
        retVar = True
    except:
        print("Cannot access database file")
    return retVar


def createRuleTable(chitRuleTableDetail):
    """to create the group table"""
    global connection
    global chitRuleTableNumber

    retVar = False
    # cursor
    crsr = connection.cursor()

    # getting table name
    chitRuleTableName = "LPCHIT_RT" + chitRuleTableDetail.get('groupType')

    # SQL command
    sql_command = "CREATE TABLE " + chitRuleTableName + \
                  "(s_no INTEGER,dueAmount INTEGER, interestAmount INTEGER,DisposeAmount INTEGER);"
    print(sql_command)

    # execute the statement
    crsr.execute(sql_command)

    print(type(chitRuleTableDetail.get('rowCount')))

    for index in range(chitRuleTableDetail.get('rowCount')):
        # SQL command to JRRRTTNTN5HB5BH5BBHB5 the data in the table
        # Sample Command
        # sql_command = "INSERT INTO TableName VALUES (1, 5000, 0, 0,\"NILL\" ,\"2021-08-13\");"
        sql_command = "INSERT INTO " + chitRuleTableName + \
                      " VALUES (" + str(index + 1) + ", " + \
                      str(chitRuleTableDetail.get('dueAmount')[index]) + ", " + \
                      str(chitRuleTableDetail.get('interest')[index]) + ", " + \
                      str(chitRuleTableDetail.get('disposeAmount')[index]) + ");"
        print(sql_command)
        crsr.execute(sql_command)
    # To save the changes in the files. Never skip this.
    # If we skip this, nothing will be saved in the database.
    connection.commit()
    return retVar

def setvendorLotReq(tableName, uname):
    # cursor
    crsr = connection.cursor()
    sql_commad = "UPDATE "+tableName+" SET vendorLotReq=1 where uname=\""+uname+"\";"
    print(sql_commad)
    crsr.execute(sql_commad)
    connection.commit()

def resetvendorLotReq(tableName , uname):
    # cursor
    crsr = connection.cursor()
    sql_commad = "UPDATE " + tableName + " SET vendorLotReq=0 where uname=\"" + uname + "\";"
    print(sql_commad)
    crsr.execute(sql_commad)
    connection.commit()

def resetAllvendorLotReq(tableName):
    # cursor
    crsr = connection.cursor()
    sql_commad = "UPDATE " + tableName + " SET vendorLotReq=0;"
    print(sql_commad)
    crsr.execute(sql_commad)
    connection.commit()


def setUserLotReq(tableName, uname):
    # cursor
    crsr = connection.cursor()
    sql_commad = "UPDATE " + tableName + " SET userLotReq=1 where uname=\"" + uname + "\";"
    print(sql_commad)
    crsr.execute(sql_commad)
    connection.commit()


def resetUserLotReq(tableName, uname):
    # cursor
    crsr = connection.cursor()
    sql_commad = "UPDATE " + tableName + " SET userLotReq=0 where uname=\"" + uname + "\";"
    print(sql_commad)
    crsr.execute(sql_commad)
    connection.commit()


def resetAllUserLotReq(tableName):
    "comment "
    crsr = connection.cursor()
    sql_commad = "UPDATE " + tableName + " SET userLotReq=0;"
    print(sql_commad)
    crsr.execute(sql_commad)
    connection.commit()


def monthlyuserpayrecord(tableName, uname,monthdetail, amountDetails,lastPaidDate):
    """To display current payment detail"""
    crsr = connection.cursor()
    monthList = []
    monthList = ''
    monthcount = 0

    crsr = connection.cursor()
    sql_command = "UPDATE " + tableName +" SET "+monthdetail+"="+amountDetails+ ", lastPaidDate=\'"+lastPaidDate+"\' WHERE uname=\'" + uname + "\';"
    print(sql_command)
    crsr.execute(sql_command)
    connection.commit()

    data = crsr.execute('''SELECT * FROM LPCHIT_DTBB1''')
    for column in data.description:
        if (column[0][0:5] == 'month'):
            if monthcount == 0:
                monthList = [column[0]]
            else:
                monthList.append(column[0])
            # print(column[0])
            monthcount = monthcount + 1
    print(monthList)
    sumMonth = 'COALESCE('

    for monthCat in monthList:
        sumMonth = sumMonth + monthCat +',0)+COALESCE('
    print(sumMonth[:-1])

    sql_command ="UPDATE "+tableName+" SET totalAmountPaid = ("+sumMonth[:-10]+") WHERE uname=\'UID1\';"
    print(sql_command)
    #crsr.execute(sql_command)
    #connection.commit()


def getRuleTableAmountDetails(groupType):
    """To get Due and Interest amount from the Rule Table"""
    # cursor
    crsr = connection.cursor()
    # getting table name
    chitRuleTableName = "LPCHIT_RT" + groupType
    sql_command = "SELECT dueAmount, interestAmount FROM "+chitRuleTableName+";"

    crsr.execute(sql_command)
    AmountDetail = crsr.fetchall()
    print(AmountDetail)
    return AmountDetail


def createDeriveVendorTable(chitDerivedTableDetail):
    """used to create Derived Table"""
    global connection
    global chitRuleTableNumber
    monthCat = ''

    retVar = False
    # cursor
    crsr = connection.cursor()

    chitRuleTableNumber = chitRuleTableNumber + 1
    chitRuleTableName = "LPCHIT_DT" + chitDerivedTableDetail.get('groupType') + str(chitRuleTableNumber)
    for index in range(chitDerivedTableDetail.get('monthCount')):
        #month1 DATE,month2 DATE
        monthCat = monthCat+"month" + str(index+1) + " INTEGER,"
    for index in range(10):
        vendorLotReq =0

    # SQL command to create a table in the database
    sql_command = "CREATE TABLE " + chitRuleTableName + \
                  "(\nsNo INTEGER,uname VARCHAR(30)," + monthCat + \
                  " lotteryDate DATE,dueDate DATE,lastPaidDate DATE" + \
                  "penality INTEGER,totalAmountPaid INTEGER," + \
                  "userLotReq BIT, vendorLotReq BIT\n);"
    print(sql_command)
    crsr.execute(sql_command)
    connection.commit()

    #Getting Amount details from Rule Table
    AmountDetails = getRuleTableAmountDetails(chitDerivedTableDetail.get('groupType'))
    #Convert Date String in to Object
    date_time_obj = datetime.datetime.strptime(chitDerivedTableDetail.get('startDate'), '%Y-%m-%d')


    for index in range(len(AmountDetails)):
        sql_command = "INSERT INTO " + chitRuleTableName + \
                      " (sNo,uname,dueDate) VALUES (" + str(index+1) + ", '" + \
                      chitDerivedTableDetail.get('uname')[index] + "', \'" + \
                       add_months(date_time_obj, index).strftime('%Y-%m-%d')+"\');"
        print(sql_command)
        # execute the statement
        crsr.execute(sql_command)

    # To save the changes in the files. Never skip this.
    # If we skip this, nothing will be saved in the database.
    connection.commit()
    return retVar


def closeDataBase():
    # close the connection
    connection.close()


def listAllRuleChitName():
    # connecting to the database
    global connection
    # connection = sqlite3.connect("LpChitDb.db")
    # cursor
    if connection == None:
        initDataBase()
    crsr = connection.cursor()
    # crsr.execute("SELECT name FROM sqlite_master WHERE type='table';") #for example
    crsr.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'LPCHIT_%';")
    print(crsr.fetchall())


def dispTable(tableName):
    # connecting to the database
    global connection
    crsr = connection.cursor()
    sql_command = "SELECT * from "+tableName
    crsr.execute(sql_command)
    print(crsr.fetchall())


def picklotterySql(tableName):
    '''used to pick a lottery for table name '''
    global connection
    # cursor
    crsr = connection.cursor()
    sql_command = "select uname from "+tableName+" where vendorLotReq=1;"
    print(sql_command)
    crsr.execute(sql_command)
    if len(crsr.fetchall()) == 0:
        print("No Vendor Req")
        sql_command = "select uname from " + tableName + " where lotteryDate IS NULL; "
    else:
        print("No Vendor Req")
        sql_command = "select uname from "+tableName+" where lotteryDate IS NULL AND vendorLotReq=1;"

    crsr.execute(sql_command)
    unameLotteryList = crsr.fetchall()
    print(unameLotteryList)

    # using random.choice() to
    # get a random number
    random_num = random.choice(unameLotteryList)

    # printing random number
    print("Selected Lottery uname is : " + random_num[0])

    today = date.today()

    sql_command = "UPDATE " + tableName + " SET lotteryDate='" +today.strftime("%Y-%m-%d")+ "' WHERE uname='"+random_num[0]+"';"
    print(sql_command)
    crsr.execute(sql_command)
    connection.commit()
    resetAllvendorLotReq(tableName)

