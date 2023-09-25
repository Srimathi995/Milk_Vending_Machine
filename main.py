import sys
import inteface_sql
import datetime



def createNewRuleChit():
    """Create New Chit is used to create the Chit table using SQL"""
    print('createNewChit')
    # to Initialize Sql
    inteface_sql.initDataBase()

    chitRuleTableDetail = {'groupType': 'BB', 'rowCount': 10,
                           'dueAmount': [5000, 4000, 4000, 4250, 4250, 4500, 4500, 4800, 4900, 4950],
                           'interest': [0, 1000, 1000, 750, 750, 500, 500, 200, 100, 50],
                           'disposeAmount': [0, 37500, 37500, 40000, 40000, 42500, 42500, 45500, 46500, 47000]}
    inteface_sql.createRuleTable(chitRuleTableDetail)
    inteface_sql.closeDataBase()


def createNewDerivedChit():
    """Derived chit is used to get all the detailed information about the chit"""
    print('createNewChit')
    # to Initialize Sql
    chitDerivedTableDetail = {'groupType': 'BB', 'monthCount': 10,
                              'uname': ['UID1', 'UID2', 'UID3', 'UID4', 'UID5', 'UID6', 'UID7', 'UID8', 'UID9',
                                        'UID10'],
                              'startDate': '2021-08-15'}
    inteface_sql.initDataBase()
    inteface_sql.createDeriveVendorTable(chitDerivedTableDetail)
    inteface_sql.closeDataBase()


def displayChit():
    """display Chit is used to list the Chit table using SQL"""
    print('displayChit')
    # display LPCHITBB001 table
    inteface_sql.initDataBase()
    inteface_sql.listAllRuleChitName()
    inteface_sql.closeDataBase()


def displayTableContent(tableName):
    """To display table content """
    inteface_sql.initDataBase()
    inteface_sql.dispTable(tableName)
    inteface_sql.closeDataBase()


def setVendorReq():
    inteface_sql.initDataBase()
    inteface_sql.setvendorLotReq("LPCHIT_DTBB1", "UID4")
    inteface_sql.closeDataBase()

def resetVendorReq():
    inteface_sql.initDataBase()
    inteface_sql.resetvendorLotReq("LPCHIT_DTBB1", "UID4")
    inteface_sql.closeDataBase()

def resetAllVendorReq():
    inteface_sql.initDataBase()
    inteface_sql.resetAllvendorLotReq("LPCHIT_DTBB1")
    inteface_sql.closeDataBase()

def updateMonthPay():
    inteface_sql.initDataBase()
    inteface_sql.monthlyuserpayrecord('LPCHIT_DTBB1', 'UID1', 'month1', '5000', '2021-08-18')
    inteface_sql.closeDataBase()

def pickSpecificChit(tableName):
    """pick a lottery for specific chit"""
    print('pickSpecificChit')
    inteface_sql.initDataBase()
    inteface_sql.picklotterySql("LPCHIT_DTBB1")
    inteface_sql.closeDataBase()


def main():
    """Main function"""
    print('main')
    # create while(1) function
    while True:
        print("Enter the below to proceed:")
        print("1. Create base rule chit table")
        print("2. Create derived chit table ")
        print("3. Display all Chit ")
        print("4. Display Specific table content")
        print("5. Set Vendor Req")
        print("6.Reset Vendor Req")
        print("7. Reset All Vendor Req ")
        print("8. Pick a lot from the specific chit ")
        print("9. update monthly paid detail")
        print("10. Exit program")

        try:
            user_input = int(input())
        except:
            print("please enter integer input")
            continue

        if (user_input >= 1 and user_input <= 10):
            print("User Selected: " + str(user_input))
            if user_input == 1:
                createNewRuleChit()
            elif user_input == 2:
                createNewDerivedChit()
            elif user_input == 3:
                displayChit()
            elif user_input == 4:
                displayTableContent('LPCHIT_DTBB1')
            elif user_input == 5:
                setVendorReq()
            elif user_input == 6:
                resetVendorReq()
            elif user_input == 7:
                resetAllVendorReq()
            elif user_input == 8:
                pickSpecificChit('LPCHIT_DTBB1')
            elif user_input == 9:
                updateMonthPay()
            elif user_input == 10:
                sys.exit()
            else:
                print("Invalid Selection Please try valid Selection")
        else:
            print("Invalid Selection Please try valid Selection")


if __name__ == '__main__':
    main()
