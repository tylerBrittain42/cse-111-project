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


def createTable(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Create table")

    try:
        sql = """CREATE TABLE warehouse (
                    w_warehousekey DECIMAL(9,0) NOT NULL,
                    w_name CHAR(100) NOT NULL,
                    w_capacity DECIMAL(6, 0) NOT NULL,
                    w_suppkey DECIMAL(9,0) NOT NULL,
                    w_nationkey DECIMAL(2,0) NOT NULL)"""
        _conn.execute(sql)



    except Error as e:
        _conn.rollback()
        print(e)

    print("++++++++++++++++++++++++++++++++++")


def dropTable(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Drop tables")

    try:
        sql = "DROP TABLE warehouse"
        _conn.execute(sql)


    except Error as e:
        _conn.rollback()
        print(e)


    print("++++++++++++++++++++++++++++++++++")


def populateTable(_conn):
    print("++++++++++++++++++++++++++++++++++")
    print("Populate table")

    try:
        curKey = 0
        for i in range(100):
            curKey = curKey + 1


            #Grabs the relevant date for the supplier
            #sql = """SELECT (s_name || '___' || n_name) AS name, s_suppkey, n_nationkey, sum(p_size)
            sql = """SELECT (s_name || '___' || n_name) AS name, sum(p_size), s_suppkey, n_nationkey
                FROM lineitem, orders, customer,nation, supplier, part
                WHERE l_orderkey = o_orderkey AND
                    o_custkey = c_custkey AND
                    c_nationkey = n_nationkey AND
                    s_suppkey = l_suppkey AND
                    p_partkey = l_partkey AND
                    --CHANGE TO WHATEVER
                    l_suppkey = ?
                GROUP BY c_nationkey
                ORDER BY COUNT(*) DESC, n_name ASC
                LIMIT 2"""
            args = [(i+1)]

            cur = _conn.cursor()
            cur.execute(sql,args)

            #w_warehousekey, w_name, w_capacity, w_suppkey, w_nationkey
            rows = cur.fetchall()

            sql = """SELECT sum(p_size)
                        FROM lineitem, orders, customer,nation, supplier, part
                        WHERE l_orderkey = o_orderkey AND
                            o_custkey = c_custkey AND
                            c_nationkey = n_nationkey AND
                            s_suppkey = l_suppkey AND
                            p_partkey = l_partkey AND
                            --CHANGE TO WHATEVER
                            l_suppkey = ?
                        GROUP BY c_nationkey
                        ORDER BY SUM(p_size) DESC
                        --ORDER BY COUNT(*) DESC, n_name ASC
                        LIMIT 1
            """
            cur = _conn.cursor()
            cur.execute(sql,args)
            cap = cur.fetchall()
            



            #First warehouse
            sql = """ INSERT INTO warehouse(w_warehousekey, w_name, w_capacity, w_suppkey, w_nationkey) 
                            VALUES(?, ?, ?, ?, ?)
                    """

            args = [curKey, rows[0][0], (cap[0][0] * 2), rows[0][2], rows[0][3]]

            # if(rows[0][1] > rows [1][1]):
            #     args = [curKey, rows[0][0], (rows[0][1] * 2), rows[0][2], rows[0][3]]
            # else:
            #     args = [curKey, rows[0][0], (rows[1][1] * 2), rows[0][2], rows[0][3]]


            _conn.execute(sql, args)
            
            curKey = curKey + 1


            #Second warehouse
            sql = """ INSERT INTO warehouse(w_warehousekey, w_name, w_capacity, w_suppkey, w_nationkey) 
                            VALUES(?, ?, ?, ?, ?)
                    """

            args = [curKey, rows[1][0], (cap[0][0] * 2), rows[1][2], rows[1][3]]

            # if(rows[0][1] > rows [1][1]):
            #     args = [curKey, rows[1][0], (rows[0][1] * 2), rows[1][2], rows[1][3]]
            # else:
            #     args = [curKey, rows[1][0], (rows[1][1] * 2), rows[1][2], rows[1][3]]


            _conn.execute(sql, args)

            

   


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


        targetReg = 'ASIA'

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
        #dropTable(conn)
        createTable(conn)
        #populateTable(conn)

        # #works
        # Q1(conn)
        # #works
        # Q2(conn)
        # #works
        # Q3(conn)
        # #works
        # Q4(conn)
        # Q5(conn)

    closeConnection(conn, database)


if __name__ == '__main__':
    main()
