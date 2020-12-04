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
###############################################################################################################



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
                    --r_aId decimal(9,0) NOT NULL,
                    --r_wId decimal(9,0) NOT NULL,
                    rc_readerID decimal(9,0) NOT NULL,
                    rc_issueID decimal(9,0) NOT NULL
                )"""
        _conn.execute(sql)

        #userCost
        sql = """CREATE TABLE userCost(
                    u_id  decimal(9,0) NOT NULL PRIMARY KEY,
                    u_cost decimal(4,2) NOT NULL
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

        sql = "DROP TABLE UserCost"
        _conn.execute(sql)

        print('Drop table success')

    except Error as e:
        _conn.rollback()
        print(e)


    #print("++++++++++++++++++++++++++++++++++")


#Inserts information from txt file into Issues
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


#Inserts from text file into Writer and Artist tables
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



#Reader List operatoins
############################################################################################################
#Addes a new reader
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


#Views a list of all readers
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
def deleteReader(_conn, reader):
    #print("++++++++++++++++++++++++++++++++++")
    #print("Delete reader" + reader)

    try:



        sql = """DELETE FROM readerList
                    WHERE r_id = ?"""
        args = [reader]
        _conn.execute(sql, args)

        sql = """DELETE FROM FollowList
                    WHERE fl_id = ?"""
        args = [reader]
        _conn.execute(sql, args)

        sql = """DELETE FROM ReadingList
                    WHERE ? = rl_readerID"""
        args = [reader]
        _conn.execute(sql, args)

        sql = """DELETE FROM ReccList
                    WHERE rc_issueID = ?"""
        args = [reader]
        _conn.execute(sql, args)

        sql = """DELETE FROM userCost
                    WHERE u_id = ?"""
        args = [reader]
        _conn.execute(sql, args)





        print("Deleted reader " + reader + " Success")


    except Error as e:
        _conn.rollback()
        print(e)

    #print("++++++++++++++++++++++++++++++++++")




#Recc List 
###############################################################################################################

#Updating is a three step process
#Remove all entries from this readerID
#Select all new recommendations
#insert all new recommendations
#Note: we only update for a single user at a time
#We will call this function anytime a change is made to a user's followinglist
def updateReccList(_conn, readerID):
    #print("++++++++++++++++++++++++++++++++++")
    print("Update Recc List")

    try:

        #Deleting all entries
        sql = """DELETE FROM reccList
                    WHERE rc_readerID = ?"""
        args = [readerID]
        _conn.execute(sql, args)

        #Selecting all new recommendations
        sql = """SELECT DISTINCT(i_id)
                    FROM 
                    (
                    SELECT i_id--(i_title || i_issue) AS issueTitle, Writers, a_name --Writers, Writer.w_id
                    FROM Writer,Issues,Artist,
                    (
                    SELECT fl_id , w_name AS 'Writers'--, a_name AS 'Artists', fl_issueID AS sq1_id, *
                    FROM FollowList, Writer,Artist
                    WHERE a_id = fl_issueID AND
                        w_id = fl_issueID AND
                        fl_id = ?
                    )sq1
                    WHERE Writer.w_name = Writers AND
                        Writer.w_id = i_id AND
                        Artist.a_id = i_id
                    UNION 

                    --Selects issues with the same artists
                    SELECT i_id--(i_title || i_issue) AS issueTitle, Writer.w_name AS Writers, a_name 
                    FROM Writer,Issues,Artist,
                    (
                    SELECT fl_id , a_name AS 'Artists'
                    FROM FollowList, Writer,Artist
                    WHERE a_id = fl_issueID AND
                        w_id = fl_issueID AND
                        fl_id = ? 
                    )sq1
                    WHERE Artist.a_name = Artists AND
                        Writer.w_id = i_id AND
                        Artist.a_id = i_id
                    )sq1
                    """
        cur = _conn.cursor()
        args = [readerID, readerID]
        cur.execute(sql, args)
        toAdd = cur.fetchall()

        #inserting all new recomendations
        for x in toAdd:
            sql = """INSERT INTO ReccList(rc_readerID, rc_issueID) 
                        VALUES (?, ?)"""
            args = [readerID, x[0]]            
            _conn.execute(sql, args)




        print('update recc list success')
        

    except Error as e:
        _conn.rollback()
        print(e)

    #print("++++++++++++++++++++++++++++++++++")


#Views a user's recommended list
#Note: it is rare for a single artist to work on multiple books at a time so the majority of 
#recommendations shown will be based off of the writer
def viewRecclist(_conn, readerID):
    #print("++++++++++++++++++++++++++++++++++")
    print(str(readerID) + "'s recc list")

    try:

        sql = """SELECT (i_title || i_issue) AS issueTitle, i_date, i_srp
                    FROM Issues, ReccList
                    WHERE i_id = rc_issueID AND
                        rc_readerID = ?"""
        cur = _conn.cursor()
        args = [readerID]
        cur.execute(sql, args)
        readerCount = cur.fetchall()

        for x in readerCount:
            print(x[0] + "\t" + x[1] + "\t" + x[2])
            #print(x)
        print('view recc list success')
        

    except Error as e:
        print(e)
        _conn.rollback()




#Issue, writer, artist operations
###############################################################################################################

#Views a list of all of the issues 
def viewIssues(_conn):
    #print("++++++++++++++++++++++++++++++++++")
    print("IssueList")

    try:

        sql = """ SELECT *
                    FROM Issues,Writer,Artist
                    WHERE i_id = a_id AND
                        i_id = w_id
                    ORDER BY i_id ASC
                """
        cur = _conn.cursor()
        cur.execute(sql)
        readerCount = cur.fetchall()

        for x in readerCount:
            print(str(x[0]) + "\t" + x[1] + "\t" + x[2].split(' ')[0] + "\t" + x[3] + "\t" + x[4] + "\t" + x[6] + "\t" + x[8])

        print('view Issue list success')
        

    except Error as e:
        _conn.rollback()
        print(e)

    #print("++++++++++++++++++++++++++++++++++")

#Views a list of all of the writers
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
            print(x[0])

        print('view Writer list success')
        

    except Error as e:
        _conn.rollback()
        print(e)

    #print("++++++++++++++++++++++++++++++++++")

#Views a list of all of the artists
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
            print(x[0])

        print('view Artist list success')
        

    except Error as e:
        _conn.rollback()
        print(e)

    #print("++++++++++++++++++++++++++++++++++")


#Reading list(of a reader) operations
###############################################################################################################

#Adds an issue to a reading list
def addToReadingList(_conn, userID, issueID,ownership):
    #print("++++++++++++++++++++++++++++++++++")
    #print("Add " + str(issueID) + " to " + str(userID) + "'s reading list")

    try:

        #rl_ownStat key
        #w = want
        #o = own
        #m = maybe
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

#Deletes deletes an issue from a reading list
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

#Changes the ownnership status of a single issue from a reading 
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

#View everyone's reading list
def viewAllReadingLists(_conn):
    #print("++++++++++++++++++++++++++++++++++")
    print("View all reading lists")

    try:

        sql = """ SELECT r_name,i_title,i_issue, rl_ownStat
                    FROM ReadingList, readerList, Issues
                    WHERE r_id = rl_readerID AND
                        i_id = rl_issueID
                    ORDER BY rl_readerID, rl_issueID asc
                """
        cur = _conn.cursor()
        cur.execute(sql)
        readerCount = cur.fetchall()



        for x in readerCount:
            print(x[0] + "\t" + x[1] + "\t" + x[2].split(' ')[0] + "\t" + x[3])

        print('success')
        

    except Error as e:
        _conn.rollback()
        print(e)

    #print("++++++++++++++++++++++++++++++++++")


#View a specific reading list
def viewSpecReadingList(_conn, readerID):
    #print("++++++++++++++++++++++++++++++++++")
    print("View " + str(readerID) + "s reading lists")

    try:

        sql = """SELECT rl_issueID,i_title,i_issue, rl_ownStat
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
            print(str(x[0]) + "\t" + x[1] + "\t" + x[2].split(' ')[0] + "\t" + x[3])

        print('success')
        

    except Error as e:
        _conn.rollback()
        print(e)

    #print("++++++++++++++++++++++++++++++++++")


#Follow list
###############################################################################################################
#Creators are added to a followlist based on an issue that they create


#Adds a creative team to a follow list
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


#Deletes a creative team from a follow list
def deleteFromFollowList(_conn,reader, issue):
    #print("++++++++++++++++++++++++++++++++++")
    #print("Deleting " + str(issue) + " from "  + str(reader) + "'s following list")

    try:

        #Can find reader id given a name
        # sql = """ SELECT r_id
        #             FROM readerList
        #             WHERE r_name = ?
        #         """

        # args = [reader]

        # cur = _conn.cursor()
        # cur.execute(sql, args)
        # deletedReader = cur.fetchall()[0][0]
       


        sql = """DELETE FROM followList
                    WHERE fl_id = ? AND
                    fl_issueID = ?"""
        #args = [deletedReader, issue]
        args = [reader, issue]
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

        sql = """SELECT fl_issueID, w_name AS 'Writers', a_name AS 'Artists'
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


#Calculates the cost of a user's list
#same 3 steps as recc list
def updateUserCost(_conn):
    #print("++++++++++++++++++++++++++++++++++")
    

    try:
        #Delete
        sql = """DELETE FROM userCost"""
        _conn.execute(sql)

        #Select
        sql = """SELECT r_id, SUM(SUBSTR(i_srp, 7)) AS 'pullList price'
                    FROM Issues, ReadingList, readerList
                    WHERE i_id = rl_issueID AND
                        rl_readerID = r_ID AND
                        rl_ownStat = 'w'
                    GROUP BY r_name
                """

        cur = _conn.cursor()
        cur.execute(sql)
        toAdd = cur.fetchall()



        for x in toAdd:
            sql = """INSERT INTO userCost(u_id, u_cost)
                        VALUES(?, ?)"""
            args = [x[0], x[1]]
            _conn.execute(sql, args)

        print('update cost success')
        

    except Error as e:
        _conn.rollback()
        print(e)

    #print("++++++++++++++++++++++++++++++++++")

def viewSingleUserCost(_conn, userID):
    #print("++++++++++++++++++++++++++++++++++")

    try:

        sql = """SELECT r_name, u_cost
                    FROM userCost,readerList
                    WHERE u_id = r_id AND
                    r_ID = ?
                    """
        args = [userID]
        cur = _conn.cursor()
        cur.execute(sql,args)
        readerCount = cur.fetchall()

        for x in readerCount:
            print(x)
            #print(x)
        print('view cost list success')
        

    except Error as e:
        print(e)
        _conn.rollback()


def viewAllUserCost(_conn):
    #print("++++++++++++++++++++++++++++++++++")

    try:

        sql = """SELECT r_name, u_cost
                    FROM userCost,readerList
                    WHERE u_id = r_id
                    """
        cur = _conn.cursor()
        cur.execute(sql)
        readerCount = cur.fetchall()

        for x in readerCount:
            print(x)
            #print(x)
        print('view cost list success')
        

    except Error as e:
        print(e)
        _conn.rollback()

#Rearrange THESE IN LATER
##############################################3333

def updateReadingList(_conn, id):
    print('update reading list called\n')
    viewSpecReadingList(_conn,id)
    
    print()
    
    print('  1) {0:>10}'.format('Add'))
    print('  2) {0:>10}'.format('Delete'))
    print('  3) {0:>10}'.format('Edit Ownership status'))
    
    option = input("Select an action: ")

    toDel = 1
    toAdd = 1
    toStat = 'w'
    print('\n')

    if option == '1':
        viewIssues(_conn)
        print('Enter the key and ownership status(w, o, m)')
        print('Enter 0 to stop adding issues')
        while(int(toAdd) != 0):
            toAdd = input('Key:')
            if (int(toAdd) != 0):
                toStat = input('Ownership status: ')
                addToReadingList(_conn,id,int(toAdd),toStat)
    elif option == '2':
        viewSpecReadingList(_conn,id)
        print('Enter the key of the Issue you want deleted')
        print('Enter 0 to stop deleting')
        print('\n')
        while(int(toDel) != 0):
            toDel = input('Key:')
            if (int(toDel) != 0):
                deleteFromReadingList(_conn,id,toDel)
            viewSpecReadingList(_conn,id)
    elif option == '3':
        viewSpecReadingList(_conn,id)
        print('Enter the key and new ownership status(w, o, m)')
        print('Enter 0 to stop adding issues')
        while(int(toAdd) != 0):
            toAdd = input('Key:')
            if (int(toAdd) != 0):
                toStat = input('New ownership status: ')
                changeOwnership(_conn,id,int(toAdd),toStat)
            viewSpecReadingList(_conn,id)        
        
            

def updateFollowList(_conn, id):
    viewFollowList(_conn, id)
    
    print()
    
    print('  1) {0:>10}'.format('Add'))
    print('  2) {0:>10}'.format('Delete'))
    print('  3) {0:>10}'.format('Exit'))
    
    option = input("Select an action: ")

    toDel = 1
    toAdd = 1
    print('\n')

    if option == '1':
        viewIssues(_conn)
        print('Enter the key of the creative team you wish to follow')
        print('Enter 0 to stop')
        while(int(toAdd) != 0):
            toAdd = input('Key:')
            if (int(toAdd) != 0):
                addToFollowList(_conn,id,toAdd)

    elif option == '2':
        viewFollowList(_conn,id)
        print('Enter the key of the creative team you want deleted')
        print('Enter 0 to stop deleting')
        print('\n')
        while(int(toDel) != 0):
            toDel = input('Key:')
            if (int(toDel) != 0):
                deleteFromFollowList(_conn,id,toDel)
    
    updateReccList(_conn,id)
            
        


def getName(_conn, id):
    #print("++++++++++++++++++++++++++++++++++")
    try:

        sql = """ SELECT r_name
                    FROM readerList
                    WHERE r_id = ?
                """
        args = [id]
        cur = _conn.cursor()
        cur.execute(sql, args)
        reader = cur.fetchall()

        return(reader[0][0])

        print('viewReaderlist success')
        

    except Error as e:
        _conn.rollback()
        print(e)

def switchUser(_conn, id):
    viewReaderList(_conn)
    print('Enter the user id that you wish to select')
    newId = int(input('User id: '))
    return(newId)

def updateUser(_conn, id):
    print('update user list called\n')
    viewReaderList(_conn)
    
    print()
    newName = input('New name: ')
    addReader(_conn,newName)




    a = """   
    print('  1) {0:>10}'.format('Add'))
    print('  2) {0:>10}'.format('Delete'))
    
    option = input("Select an action: ")

    tempKey = 1
    print('\n')
    id = str(id)

    if option == '1':
        newName = input('New name: ')
        addReader(_conn,newName)
    elif option == '2':
        viewReaderList(_conn)
        print('Enter the key of the user you want deleted')
        print('Enter 0 to stop deleting')
        print('\n')
        while((tempKey) != 0):
            tempKey = input('Key:')
            if(int(tempKey) == id):
                print('Cannot delete self')
            elif (int(tempKey) != 0):
                deleteReader(_conn, tempKey)
            viewReaderList(_conn)"""
    
#Relating to formatting
###############################################################################################################

#Resets the database
def resetDB(conn):
    dropTable(conn)
    createTable(conn)
    populateIssues(conn)
    populateCreative(conn)

def topBorder():
    top = ""
    for x in range(140):
        top = top + "_"
    print(top)
    

def botBorder():
    bot = ""
    for x in range(140):
        bot = bot + "_"
    print(bot)        

def prompt(conn,id):

    #ref setnece
    #print('{0:>100}'.format('test'))
    topBorder()
    print('  {0:^100}'.format('My Comic List'))
    print()
    print(' User: '  + getName(conn,id))
    print('  {0:^140}'.format('Reading List Actions'))
    print('  1) {0:>10}'.format('View Issues'))
    print('  2) {0:>10}'.format('View My Reading List'))
    print('  3) {0:>10}'.format('Update Reading List'))
    print('  4) {0:>10}'.format('View All Reading Lists'))

    print('  {0:^140}'.format('Follow List Actions'))
    print('  5) {0:>10}'.format('View Following List'))
    print('  6) {0:>10}'.format('Update Following List')) #Stopped here
    print('  7) {0:>10}'.format('View Recc List'))

    print('  {0:^140}'.format('Cost List Actions')) 
    print('  8) {0:>10}'.format('View My Cost List'))
    print('  9) {0:>10}'.format('View Everyones Cost List'))

    print('  {0:^140}'.format('Adminstrative Actions'))
    print('  10) {0:>10}'.format('View Users'))
    print('  11) {0:>10}'.format('Switch User'))
    print('  12) {0:>10}'.format('Add User'))
    print('  13) {0:>10}'.format('Reset Database'))
    print('  14) {0:>10}'.format('EXIT\n'))

    #botBorder()


def main():
    database = r"data/comicDB.sqlite"
    option = 15
    currUser = 1



    # create a database connection
    conn = openConnection(database)
    with conn:
        #Testing intitial database setup
        #REMOVE THIS LINE POST TESTING
        #resetDB(conn)



        while option != '14':
            
            prompt(conn,currUser)
            option = input('Select an action: ')

            if option == '1':
                viewIssues(conn)
            elif option == '2':
                viewSpecReadingList(conn,currUser)
            elif option == '3':
                updateReadingList(conn,currUser)   
            elif option == '4':  
                viewAllReadingLists(conn)  
            elif option == '5':
                viewFollowList(conn,currUser)
            elif option == '6':
                updateFollowList(conn,currUser)
            elif option == '7':
                viewRecclist(conn,currUser)
            elif option == '8':
                updateUserCost(conn)
                viewSingleUserCost(conn,currUser)
            elif option == '9':
                updateUserCost(conn)               
                viewAllUserCost(conn)
            elif option == '10':     
                viewReaderList(conn)
            elif option == '11':
                currUser = switchUser(conn, id)
            elif option == '12':
                updateUser(conn, id)    
            elif option == '13':
                resetDB(conn)

            if option != '14':
                spam = input("")


        
        
        



    closeConnection(conn, database)


if __name__ == '__main__':
    main()
