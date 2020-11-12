import sqlite3
from sqlite3 import Error


def openConnection(_dbFile):
    #print("++++++++++++++++++++++++++++++++++")
    #print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print("Connection Success")
    except Error as e:
        print(e)

    #print("++++++++++++++++++++++++++++++++++")

    return conn

def closeConnection(_conn, _dbFile):
    #print("++++++++++++++++++++++++++++++++++")
    #print("Close database: ", _dbFile)

    try:
        _conn.close()
        print("Close success")
    except Error as e:
        print(e)

    #print("++++++++++++++++++++++++++++++++++")

#Initial database setup
############################################
#Creates all the relevant tables
def createTable(_conn):
    #print("++++++++++++++++++++++++++++++++++")
    #print("Create table")

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
                    fl_id decimal(9,0) NOT NULL,
                    fl_issueID char(4) NOT NULL
                    --Do i need to change this part?
                    --fl_artistID decimal(9,0) NOT NULL,
                    --fl_writerID decimal(9,0) NOT NULL
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


        print('tables created')


    except Error as e:
        _conn.rollback()
        print(e)
        
    #print("++++++++++++++++++++++++++++++++++")


#Drops all tables in the database
def dropTable(_conn):
    #print("++++++++++++++++++++++++++++++++++")
    #print("Drop tables")

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

        print('Drop table success')

    except Error as e:
        _conn.rollback()
        print(e)


    #print("++++++++++++++++++++++++++++++++++")


#reads in pull information from text file
def populateIssues(_conn):
    #print("++++++++++++++++++++++++++++++++++")
    #print("Populate issues")

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

        print('Populate Issues success')

    except Error as e:
        _conn.rollback()
        print(e)

    #print("++++++++++++++++++++++++++++++++++")


def viewIssues(_conn):
    #print("++++++++++++++++++++++++++++++++++")
    print("IssueList")

    try:

        sql = """ SELECT *
                    FROM Issues
                    ORDER BY i_id ASC
                """
        cur = _conn.cursor()
        cur.execute(sql)
        readerCount = cur.fetchall()

        for x in readerCount:
            print(str(x[0]) + "\t" + x[1] + "\t" + x[2].split(' ')[0] + "\t" + x[3] + "\t" + x[4])

        print('view Issue list success')
        

    except Error as e:
        _conn.rollback()
        print(e)

    #print("++++++++++++++++++++++++++++++++++")


#Reads in information for writer and artist list
#Reads in information for writer and artist list
def populateCreative(_conn):
    #print("++++++++++++++++++++++++++++++++++")
    #print("Populate creative")

    try:

        inF = open("data/revisedCreator.txt", "r")

        contents = inF.readlines()

        #Since the writer and artists are stored in the same line, we will insert into both lists at the same time

        for x in contents:

            currentLine= x.split('\t')
            currentID = currentLine[0]

            for y in range(len(currentLine)):
                
                currentLine[y] = currentLine[y].split(")")
            

            sql = """ INSERT INTO Artist(a_id, a_name) 
                            VALUES(?, ?)
                    """

            args = [currentID, (currentLine[2][1])]            
            _conn.execute(sql, args)

            sql = """ INSERT INTO Writer(w_id, w_name) 
                            VALUES(?, ?)
                    """

            args = [currentID, (currentLine[1][1])]            
            _conn.execute(sql, args)

            

        print('PopulateCreative success')

    except Error as e:
        _conn.rollback()
        print(e)

    #print("++++++++++++++++++++++++++++++++++")


def viewWriters(_conn):
    #print("++++++++++++++++++++++++++++++++++")
    print("Writer List")

    try:

        sql = """ SELECT DISTINCT(w_name)
                    FROM Writer
                    ORDER BY w_name ASC
                """
        cur = _conn.cursor()
        cur.execute(sql)
        readerCount = cur.fetchall()

        for x in readerCount:
            print(x)

        print('view Writer list success')
        

    except Error as e:
        _conn.rollback()
        print(e)

    #print("++++++++++++++++++++++++++++++++++")


def viewArtists(_conn):
    #print("++++++++++++++++++++++++++++++++++")
    print("Artist List")

    try:

        sql = """ SELECT DISTINCT(a_name)
                    FROM Artist
                    ORDER BY a_name ASC
                """
        cur = _conn.cursor()
        cur.execute(sql)
        readerCount = cur.fetchall()

        for x in readerCount:
            print(x)

        print('view Artist list success')
        

    except Error as e:
        _conn.rollback()
        print(e)

    #print("++++++++++++++++++++++++++++++++++")




#Relating to reader list
######################################3
def addReader(_conn, reader):
    #print("++++++++++++++++++++++++++++++++++")
    #print("Add reader")

    try:

        sql = """ SELECT MAX(r_id) 
                    FROM readerList
                """
        cur = _conn.cursor()
        cur.execute(sql)
        readerMaxId = cur.fetchone()
        

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

        print('Added reader ' + reader + " successfully")
        

    except Error as e:
        _conn.rollback()
        print(e)

    #print("++++++++++++++++++++++++++++++++++")


def viewReaderList(_conn):
    #print("++++++++++++++++++++++++++++++++++")
    print("ReaderList")

    try:

        sql = """ SELECT *
                    FROM readerList
                """
        cur = _conn.cursor()
        cur.execute(sql)
        readerCount = cur.fetchall()

        for x in readerCount:
            print(x)

        print('viewReaderlist success')
        

    except Error as e:
        _conn.rollback()
        print(e)

    #print("++++++++++++++++++++++++++++++++++")


#when we are deleting a reader
#we are also shifting down the id numbers to avoid gaps
def deleteReader(_conn, reader):
    #print("++++++++++++++++++++++++++++++++++")
    #print("Delete reader" + reader)

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



        print("Deleted reader " + reader + " Success")


    except Error as e:
        _conn.rollback()
        print(e)

    #print("++++++++++++++++++++++++++++++++++")



#Relating to following list
##########################################
def addToFollowList(_conn, userID, issueID):
    #print("++++++++++++++++++++++++++++++++++")
    #print("Add " + str(issueID) + " to " + str(userID) + "'s followList")

    try:

        sql = """ INSERT INTO FollowList(fl_id, fl_issueID) 
                    VALUES (?, ?)
                """

        args = [userID, issueID]

        cur = _conn.cursor()
        cur.execute(sql, args)



        print("Added " + str(issueID) + " to " + str(userID) + "'s followList Success")


    except Error as e:
        _conn.rollback()
        print(e)

    #print("++++++++++++++++++++++++++++++++++")  


def deleteFromFollowList(_conn,reader, issue):
    #print("++++++++++++++++++++++++++++++++++")
    #print("Deleting " + str(issue) + " from "  + str(reader) + "'s following list")

    try:

        sql = """ SELECT r_id
                    FROM readerList
                    WHERE r_name = ?
                """

        args = [reader]

        cur = _conn.cursor()
        cur.execute(sql, args)
        deletedReader = cur.fetchall()[0][0]
       


        sql = """DELETE FROM followList
                    WHERE fl_id = ? AND
                    fl_issueID = ?"""
        args = [deletedReader, issue]
        _conn.execute(sql, args)



        print("Deleted " + str(issue) + " from "  + str(reader) + "'s following list Success")


    except Error as e:
        _conn.rollback()
        print(e)

    #print("++++++++++++++++++++++++++++++++++")


#for now we will add in all creators from a specific issue to the following list 
def viewFollowList(_conn, userID):
    #print("++++++++++++++++++++++++++++++++++")
    print("Viewing " + str(userID) + "'s followList")

    try:

        sql = """SELECT w_name AS 'Writers', a_name AS 'Artists'
                    FROM FollowList, Writer,Artist
                    WHERE a_id = fl_issueID AND
                            w_id = fl_issueID AND
                            fl_id = ?
                """

        args = [userID]

        cur = _conn.cursor()
        cur.execute(sql, args)
        following = cur.fetchall()

        for x in following:
            print(x)



        print('success')


    except Error as e:
        _conn.rollback()
        print(e)

    #print("++++++++++++++++++++++++++++++++++")


#Relating to reading list
######################################
def addToReadingList(_conn, userID, issueID,ownership):
    #print("++++++++++++++++++++++++++++++++++")
    #print("Add " + str(issueID) + " to " + str(userID) + "'s reading list")

    try:

        sql = """ INSERT INTO ReadingList(rl_readerID, rl_issueID, rl_ownStat) 
                    VALUES (?, ?, ?)
                """

        args = [userID, issueID, ownership]

        cur = _conn.cursor()
        cur.execute(sql, args)



        print("Added " + str(issueID) + " to " + str(userID) + "'s reading list Success")


    except Error as e:
        _conn.rollback()
        print(e)

    #print("++++++++++++++++++++++++++++++++++")  


def deleteFromReadingList(_conn,reader, issue):
    #print("++++++++++++++++++++++++++++++++++")
    #print("Deleting " + str(issue) + " from "  + str(reader) + "'s reading list")

    try:



        sql = """DELETE FROM ReadingList
                    WHERE rl_readerID = ? AND
                    rl_issueID = ?"""
        args = [reader, issue]
        _conn.execute(sql, args)



        print("Deleted " + str(issue) + " from "  + str(reader) + "'s reading list Success")


    except Error as e:
        _conn.rollback()
        print(e)

    #print("++++++++++++++++++++++++++++++++++")


def changeOwnership(_conn, readerID, issueID, newStatus):
    #print("++++++++++++++++++++++++++++++++++")
    #print("Updating "  + str(readerID) + "'s reading list")

    try:



        sql = """UPDATE readingList
                    SET rl_ownStat = ?
                    WHERE rl_readerID = ? AND
                    rl_issueID = ?"""
        args = [newStatus, readerID, issueID]
        _conn.execute(sql, args)



        print("Updated "  + str(readerID) + "'s reading list Success")


    except Error as e:
        _conn.rollback()
        print(e)

    #print("++++++++++++++++++++++++++++++++++")


def viewAllReadingLists(_conn):
    #print("++++++++++++++++++++++++++++++++++")
    print("View all reading lists")

    try:

        sql = """ SELECT r_name,i_title,i_issue
                    FROM ReadingList, readerList, Issues
                    WHERE r_id = rl_readerID AND
                        i_id = rl_issueID
                    ORDER BY rl_readerID, rl_issueID asc
                """
        cur = _conn.cursor()
        cur.execute(sql)
        readerCount = cur.fetchall()



        for x in readerCount:
            print(x[0] + "\t" + x[1] + "\t" + x[2].split(' ')[0])

        print('success')
        

    except Error as e:
        _conn.rollback()
        print(e)

    #print("++++++++++++++++++++++++++++++++++")


def viewSpecReadingList(_conn, readerID):
    #print("++++++++++++++++++++++++++++++++++")
    print("View " + str(readerID) + "s reading lists")

    try:

        sql = """SELECT r_name,i_title,i_issue
                    FROM ReadingList, readerList, Issues
                    WHERE r_id = rl_readerID AND
                        i_id = rl_issueID AND
                        r_id = ?
                    ORDER BY rl_issueID asc
                """

        args = [readerID] 
        cur = _conn.cursor()
        cur.execute(sql, args)
        readerCount = cur.fetchall()



        for x in readerCount:
            print(x[0] + "\t" + x[1] + "\t" + x[2].split(' ')[0])

        print('success')
        

    except Error as e:
        _conn.rollback()
        print(e)

    #print("++++++++++++++++++++++++++++++++++")


def q5(_conn):
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


        #targetReg = 'ASIA'>Nat, targetReg, targetReg

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



    #print("++++++++++++++++++++++++++++++++++")


def main():
    database = r"data/comicDB.sqlite"

    # create a database connection
    conn = openConnection(database)
    with conn:
        print('\n')
        dropTable(conn)
        createTable(conn)
        populateIssues(conn)
        populateCreative(conn)
        print('\n')

        addReader(conn, "Bob")
        addReader(conn, "Joe")
        addReader(conn, "Jim")
        addReader(conn, "Bill")
        print('\n')
        viewReaderList(conn)
        print('\n')
        deleteReader(conn, "Joe")
        addReader(conn, "tim")
        print('\n')
        viewReaderList(conn)
        print('\n')


        addToFollowList(conn, 5, 20)
        addToFollowList(conn, 1, 193)
        addToFollowList(conn, 5, 196)
        deleteFromFollowList(conn,'tim' , 20)
        print('\n')
        viewFollowList(conn, 5)
        print('\n')


        addToReadingList(conn,5,20,'o')
        addToReadingList(conn,5,196 ,'o')
        addToReadingList(conn, 1, 193, 'w')
        addToReadingList(conn,3, 189, 'w')
        addToReadingList(conn,3, 534, 'w')
        deleteFromReadingList(conn, 5, 20)
        changeOwnership(conn, 5, 196, 'E')
        print('\n')
        viewAllReadingLists(conn)
        print('\n')
        viewSpecReadingList(conn, 3)
        print('\n')
        #viewIssues(conn)
        print('\n')
        #viewWriters(conn)
        #print('\n')
        #viewArtists(conn)


    closeConnection(conn, database)


if __name__ == '__main__':
    main()
