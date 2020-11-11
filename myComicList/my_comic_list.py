import sqlite3
from sqlite3 import Error


def openConnection(_dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

    return conn

def closeConnection(_conn, _dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Close database: ", _dbFile)

    try:
        _conn.close()
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")


#Creates all the relevant tables
def createTable(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Create table")

    try:
        #Issues
        sql = """CREATE TABLE Issues (
                    i_id decimal(9,0) NOT NULL PRIMARY KEY,
                    i_title char(50) NOT NULL,
                    i_issue char(50), --considering removing this
                    i_date date(4,0) NOT NULL,
                    i_srp decimal(2,2) NOT NULL
                )"""
        _conn.execute(sql)

        #readerList
        sql = """CREATE TABLE readerList(
                    r_id  decimal(9,0) NOT NULL PRIMARY KEY,
                    r_name char(50) NOT NULL) """
        _conn.execute(sql)

        #readingList
        sql = """CREATE TABLE ReadingList(
                    rl_readerID decimal(9,0) NOT NULL,
                    rl_issueID char(4)  NOT NULL,
                    rl_ownStat char(10) NOT NULL
                ) """
        _conn.execute(sql)

        #FollowList
        sql = """CREATE TABLE FollowList(
                    fl_id decimal(9,0) NOT NULL PRIMARY KEY,
                    --Do i need to change this part?
                    fl_artistID decimal(9,0) NOT NULL,
                    fl_writerID decimal(9,0) NOT NULL
                ) """
        _conn.execute(sql)

        #artist
        sql = """CREATE TABLE Artist(
                    a_id decimal(9,0) NOT NULL PRIMARY KEY,
                    a_name char(50) NOT NULL
                )"""
        _conn.execute(sql)

        #Writer
        sql = """CREATE TABLE Writer(
                    w_id decimal(9,0) NOT NULL PRIMARY KEY,
                    w_name char(50) NOT NULL
                ) """
        _conn.execute(sql)

        #ReccList
        sql = """CREATE TABLE ReccList(
                    r_aId decimal(9,0) NOT NULL,
                    r_wId decimal(9,0) NOT NULL,
                    r_readerID decimal(9,0) NOT NULL,
                    r_issueID decimal(9,0) NOT NULL
                )"""
        _conn.execute(sql)


        print('success')


    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")


#Drops all tables in the database
def dropTable(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Drop tables")

    try:

        sql = "DROP TABLE Issues"
        _conn.execute(sql)

        sql = "DROP TABLE readerList"
        _conn.execute(sql)

        sql = "DROP TABLE ReadingList"
        _conn.execute(sql)

        sql = "DROP TABLE FollowList"
        _conn.execute(sql)

        sql = "DROP TABLE Artist"
        _conn.execute(sql)

        sql = "DROP TABLE Writer"
        _conn.execute(sql)

        sql = "DROP TABLE ReccList"
        _conn.execute(sql)

        print('success')

    except Error as e:
        _conn.rollback()
        print(e)


    print("++++++++++++++++++++++++++++++++++")


#reads in pull information from text file
def populateIssues(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Populate issues")

    try:

        inF = open("data/pull_w_tabs.txt", "r")

        contents = inF.readlines()

        for x in contents:

            currentIssue = x.split('\t')

            sql = """ INSERT INTO Issues(i_id, i_title, i_issue, i_date, i_srp) 
                            VALUES(?, ?, ?, ?, ?)
                    """

            args = [currentIssue[0], currentIssue[1], currentIssue[2], currentIssue[3], currentIssue[4]]            
            _conn.execute(sql, args)

        print('success')

    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")


#Reads in information for writer and artist list
#Reads in information for writer and artist list
def populateCreative(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Populate creative")

    try:

        inF = open("data/revisedCreator.txt", "r")

        contents = inF.readlines()

        #Since the writer and artists are stored in the same line, we will insert into both lists at the same time

        for x in contents:

            currentLine= x.split('\t')
            

            sql = """ INSERT INTO Artist(a_id, a_name) 
                            VALUES(?, ?)
                    """

            args = [currentLine[0], (currentLine[2])]            
            _conn.execute(sql, args)

            sql = """ INSERT INTO Writer(w_id, w_name) 
                            VALUES(?, ?)
                    """

            args = [currentLine[0], (currentLine[1])]            
            _conn.execute(sql, args)

        print('success')

    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")





def addReader(_conn, reader):
    print("++++++++++++++++++++++++++++++++++")
    print("Add reader")

    try:

        sql = """ SELECT MAX(r_id) 
                    FROM readerList
                """
        cur = _conn.cursor()
        cur.execute(sql)
        readerMaxId = cur.fetchone()
        print(readerMaxId[0])

        if readerMaxId[0] == None:
            nextID = 0
        else:
            nextID = readerMaxId[0]

        nextID = nextID + 1
       

        sql = """ INSERT INTO readerList(r_id, r_name) 
                       VALUES (?, ?)
                """


        args = [str(nextID), reader]            
        _conn.execute(sql, args)

        print('success')
        

    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")



def viewReaderList(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("View ReaderList")

    try:

        sql = """ SELECT *
                    FROM readerList
                """
        cur = _conn.cursor()
        cur.execute(sql)
        readerCount = cur.fetchall()

        for x in readerCount:
            print(x)

        print('success')
        

    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")


#when we are deleting a reader
#we are also shifting down the id numbers to avoid gaps
def deleteReader(_conn, reader):
    print("++++++++++++++++++++++++++++++++++")
    print("Delete reader" + reader)

    try:

        sql = """ SELECT r_id
                    FROM readerList
                    WHERE r_name = ?
                """

        args = [reader]

        cur = _conn.cursor()
        cur.execute(sql, args)
        deletedReader = cur.fetchall()


        sql = """DELETE FROM readerList
                    WHERE r_id = ?"""
        args = [deletedReader[0][0]]
        _conn.execute(sql, args)


        # sql = """UPDATE readerList
        #             SET r_id = (r_id - 1)
        #             WHERE r_id > ? """
        # args = [deletedReader[0][0]]
        # _conn.execute(sql, args)

        print('success')


    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def Q1(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Q1")

    try:

        outF = open("output/1.out","w")
        outF.write("       wId wName                                          wCap        sId        nId\n")
        
        

        sql = """SELECT *
                From warehouse
                ORDER BY w_warehousekey ASC
        """

        cur = _conn.cursor()
        cur.execute(sql)

        


        rows = cur.fetchall()
        for i in range(200):
            wId = '{:>10}'.format(rows[i][0]) 
            wName = '{:<40}'.format(rows[i][1]) #from char to char
            wCap = '{:>11}'.format((rows[i][2]))
            sId = '{:>11}'.format((rows[i][3]))
            nId = '{:>11}'.format((rows[i][4]))


            #print(wId + ' ' + wName + wCap + sId + nId)
            outF.write(wId + ' ' + wName + wCap + sId + nId)
            outF.write("\n")

        outF.close()
    except Error as e:
        print(e)



    print("++++++++++++++++++++++++++++++++++")


def Q2(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Q2")

    try:
        outF = open("output/2.out","w")
        sql = """SELECT n_name, COUNT(w_warehousekey), SUM(w_capacity)
                 FROM warehouse,nation
                 WHERE w_nationkey = n_nationkey
                 GROUP BY n_nationkey
                 ORDER BY COUNT(w_warehousekey) DESC, SUM(w_capacity) DESC, n_name ASC
        """

        cur = _conn.cursor()
        cur.execute(sql)

        outF.write("nation                                         numW     totCap\n")


        rows = cur.fetchall()
        for i in range(21):
            nName = '{:<29}'.format(rows[i][0]) 
            numW = '{:>21}'.format(rows[i][1]) 
            totCap = '{:>11}'.format((rows[i][2]))

            outF.write(nName + ' ' + numW + totCap +"\n")
        outF.close()

    except Error as e:
        print(e)


    print("++++++++++++++++++++++++++++++++++")


def Q3(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Q3")

    try:

        inF = open("input/3.in", "r")
        arg = [inF.readline().replace('\n','')]

        inF.close()
        
        outF = open("output/3.out","w")
        sql = """SELECT s_name, n_name, sq1.warehouseName
                 FROM nation,supplier,
                 (
                 SELECT w_name AS warehouseName, w_suppkey AS wareSupp
                 FROM warehouse,nation
                 WHERE w_nationkey = n_nationkey AND
                     --Change this to var
                     n_name = ?
                 )sq1
                 WHERE sq1.wareSupp = s_suppkey AND
                 n_nationkey = s_nationkey
                 ORDER BY s_name ASC
        """ 

        cur = _conn.cursor()
        
        cur.execute(sql, arg)

        outF.write("supplier             nation               warehouse               \n")


        rows = cur.fetchall()
        
        for row in rows:
            sName = '{:<21}'.format(row[0]) 
            nat = '{:<21}'.format(row[1]) 
            wName = '{:>11}'.format((row[2]))
            outF.write(sName +  nat + wName +"\n")
        outF.close()

    except Error as e:
        print(e)



    print("++++++++++++++++++++++++++++++++++")


def Q4(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Q4")

    try:

        inF = open("input/4.in", "r")
        targetReg = inF.readline().replace('\n','')
        targetCap = inF.readline().replace('\n','')
        args = [targetReg, targetCap]
        inF.close()
        
        outF = open("output/4.out","w")
        sql = """ SELECT w_name, w_capacity
                  FROM warehouse, nation, region
                  WHERE w_nationkey = n_nationkey AND
                      n_regionkey = r_regionkey AND
                      r_name = ? AND
                       (w_capacity >  ?) 
                  ORDER BY w_capacity DESC
        """ 

        cur = _conn.cursor()
        
        cur.execute(sql, args)

        outF.write("warehouse                                  capacity\n")


        rows = cur.fetchall()
        
        for row in rows:
            sName = '{:<43}'.format(row[0]) 
            nat = '{:<21}'.format(row[1]) 
            outF.write(sName +  nat + "\n")
        outF.close()

    except Error as e:
        print(e)



    print("++++++++++++++++++++++++++++++++++")


def Q5(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Q5")

    try:

        inF = open("input/5.in", "r")
        
        targetNat = inF.readline().replace('\n','')
        inF.close()
        
        outF = open("output/5.out","w")
        outF.write("region                           capacity\n")
        outF.close()
        outF = open("output/5.out","a")
        sql = """   SELECT r_name, SUM(w_capacity)
                    FROM warehouse, region,
                    (
                    SELECT w_name AS natName
                    FROM nation,supplier,warehouse
                    WHERE s_suppkey = w_suppkey AND
                        s_nationkey = n_nationkey AND
                        --change this
                        n_name = ?
                    ORDER BY w_name ASC
                    )sq1,

                    (
                    SELECT w_name AS regName
                    FROM warehouse,region,nation
                    WHERE w_nationkey = n_nationkey AND
                        n_regionkey = r_regionkey AND 
                        --Change this
                        r_name = ?
                    )sq2

                    WHERE natName = regName AND
                        w_name = regName AND
                        --delete this
                        r_name = ?
        """ 



        cur = _conn.cursor()
        
        targetReg = 'AFRICA'

        cur.execute(sql, [targetNat, targetReg, targetReg])

        rows = cur.fetchall()
        
        for row in rows:
            sName = '{:<33}'.format(str(row[0])) 
            if str(row[1]) == 'None':
                sName = '{:<33}'.format(targetReg) 
                nat = '{:>8}'.format(str(0))
            else: 
                nat = '{:>8}'.format(str(row[1])) 
            
            outF.write(sName +  nat + "\n")

    
        targetReg = 'AMERICA'

        cur.execute(sql, [targetNat, targetReg, targetReg])

        rows = cur.fetchall()
        
        for row in rows:
            sName = '{:<33}'.format(str(row[0])) 
            if str(row[1]) == 'None':
                sName = '{:<33}'.format(targetReg) 
                nat = '{:>8}'.format(str(0))
            else: 
                nat = '{:>8}'.format(str(row[1])) 
            
            outF.write(sName +  nat + "\n")


        targetReg = 'ASIA'>Nat, targetReg, targetReg

        rows = cur.fetchall()
        
        for row in rows:
            sName = '{:<33}'.format(str(row[0])) 
            if str(row[1]) == 'None':
                sName = '{:<33}'.format(targetReg) 
                nat = '{:>8}'.format(str(0))
            else: 
                nat = '{:>8}'.format(str(row[1])) 
            
            outF.write(sName +  nat + "\n")

            
        targetReg = 'EUROPE'

        cur.execute(sql, [targetNat, targetReg, targetReg])

        rows = cur.fetchall()
        
        for row in rows:
            sName = '{:<33}'.format(str(row[0])) 
            if str(row[1]) == 'None':
                sName = '{:<33}'.format(targetReg) 
                nat = '{:>8}'.format(str(0))
            else: 
                nat = '{:>8}'.format(str(row[1])) 
            
            outF.write(sName +  nat + "\n")

        targetReg = 'MIDDLE EAST'

        cur.execute(sql, [targetNat, targetReg, targetReg])

        rows = cur.fetchall()
        
        for row in rows:
            sName = '{:<33}'.format(str(row[0])) 
            if str(row[1]) == 'None':
                sName = '{:<33}'.format(targetReg) 
                nat = '{:>8}'.format(str(0))
            else: 
                nat = '{:>8}'.format(str(row[1])) 
            
            outF.write(sName +  nat + "\n")
        
        
        
        
        
        outF.close()

    except Error as e:
        print(e)



    print("++++++++++++++++++++++++++++++++++")


def main():
    database = r"data/comicDB.sqlite"

    # create a database connection
    conn = openConnection(database)
    with conn:
        dropTable(conn)
        createTable(conn)
        populateIssues(conn)
        populateCreative(conn)

        addReader(conn, "Bob")
        addReader(conn, "Joe")
        addReader(conn, "Jim")
        addReader(conn, "Bill")
        viewReaderList(conn)

        #DELETING A READER IS ALSO GOING TO NEED TO DELETE THERE FOLLOWING AND READING LISTS
        #ADD THIS
        deleteReader(conn, "Joe")
        addReader(conn, "tim")
        viewReaderList(conn)



    closeConnection(conn, database)


if __name__ == '__main__':
    main()
