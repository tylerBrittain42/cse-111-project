--Create table Queries(Count: 7)
CREATE TABLE Issues (
    i_id decimal(9,0) NOT NULL PRIMARY KEY,
    i_title char(50) NOT NULL,
    i_issue char(50), --considering removing this
    i_date date(4,0) NOT NULL,
    i_srp decimal(2,2) NOT NULL
)

CREATE TABLE readerList(
    r_id  decimal(9,0) NOT NULL PRIMARY KEY,
    r_name char(50) NOT NULL
)

CREATE TABLE ReadingList(
    rl_readerID decimal(9,0) NOT NULL,
    rl_issueID char(4)  NOT NULL,
    rl_ownStat char(10) NOT NULL
)

CREATE TABLE FollowList(
    fl_id decimal(9,0) NOT NULL,
    fl_issueID char(4) NOT NULL
    --Do i need to change this part?
    --fl_artistID decimal(9,0) NOT NULL,
    --fl_writerID decimal(9,0) NOT NULL
) 

CREATE TABLE Artist(
    a_id decimal(9,0) NOT NULL PRIMARY KEY,
    a_name char(50) NOT NULL
)

CREATE TABLE Writer(
    w_id decimal(9,0) NOT NULL PRIMARY KEY,
    w_name char(50) NOT NULL
) 

CREATE TABLE ReccList(
    --r_aId decimal(9,0) NOT NULL,
    --r_wId decimal(9,0) NOT NULL,
    r_readerID decimal(9,0) NOT NULL,
    r_issueID decimal(9,0) NOT NULL
)

--Drop Table Queries(Count: 7)
DROP TABLE Issues;
DROP TABLE readerList
DROP TABLE ReadingList;
DROP TABLE FollowList;
DROP TABLE Artist;
DROP TABLE Writer;
DROP TABLE ReccList;

--populateIssues(count: 1)
INSERT INTO Issues(i_id, i_title, i_issue, i_date, i_srp) 
    VALUES(0, 'dummyTitle', 0, 01/01/1992, '23.00')
--




--UpdateReccList queries (Using reader 5 for examples)
--Count: 3

DELETE FROM reccList
    WHERE r_readerID = 1;
--

--Finds other books with same writer or artist
SELECT DISTINCT(i_id)
                    FROM 
                    (
                    SELECT i_id--(i_title || i_issue) AS issueTitle, Writers, a_name --Writers, Writer.w_id
                    FROM Writer,Issues,Artist,
                    (
                    SELECT fl_id , w_name AS 'Writers'--, a_name AS 'Artists', fl_issueID AS sq1_id, *
                    FROM FollowList, Writer,Artist
                    WHERE a_id = fl_issueID AND
                        w_id = fl_issueID AND
                        fl_id = 1
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
                        fl_id = 1 
                    )sq1
                    WHERE Artist.a_name = Artists AND
                        Writer.w_id = i_id AND
                        Artist.a_id = i_id
                    )sq1

--Inserts into reccList
INSERT INTO ReccList(r_readerID, r_issueID) 
    VALUES (1, 513)


--viewReccList(Count: 1)
SELECT (i_title || i_issue) AS issueTitle, i_date, i_srp
FROM Issues, ReccList
WHERE i_id = r_issueID AND
    r_readerID = 1

--viewIssues(Count: 1)
SELECT *
FROM Issues,Writer,Artist
WHERE i_id = a_id AND
    i_id = w_id
ORDER BY i_id ASC

--populateCreative(Count: 2)
INSERT INTO Artist(a_id, a_name) 
    VALUES(0, 'dummyArtist')

INSERT INTO Writer(w_id, w_name) 
    VALUES(0, 'dummyWriter')



--View Writers(Count: 1)
SELECT DISTINCT(w_name)
    FROM Writer
    ORDER BY w_name ASC


--View Artists(Count: 1)
SELECT DISTINCT(a_name)
    FROM Artist
    ORDER BY a_name ASC


--addReader(Count: 2)
SELECT MAX(r_id) 
FROM readerList

INSERT INTO readerList(r_id, r_name) 
    VALUES (6, 'dummy reader')

--viewReaderList(Count: 1)
SELECT *
    FROM readerList

--delete reader(Count: 2)
SELECT r_id
    FROM readerList
    WHERE r_name = 'dummy reader'

DELETE FROM readerList
    WHERE r_id = 6

--addToFollowList(Count: 1)
INSERT INTO FollowList(fl_id, fl_issueID) 
    VALUES (2, 216)

--deleteFromFollowList(Count: 1)
DELETE FROM followList
WHERE fl_id = 2 AND
    fl_issueID =216 

--viewFollowList(Count: 1)
SELECT w_name AS 'Writers', a_name AS 'Artists'
FROM FollowList, Writer,Artist
WHERE a_id = fl_issueID AND
        w_id = fl_issueID AND
        fl_id = 2



--addToReadingList(Count: 1)
INSERT INTO ReadingList(rl_readerID, rl_issueID, rl_ownStat) 
    VALUES (1, 216, 'w')

--deleteFromReadingList(Count: 1)
DELETE FROM ReadingList
    WHERE rl_readerID = 1 AND
    rl_issueID = 216

--changeOwnership
UPDATE readingList
    SET rl_ownStat = 'Q'
    WHERE rl_readerID = 1 AND
        rl_issueID = 216

--viewAllReadingLists
SELECT r_name,i_title,i_issue, rl_ownStat
    FROM ReadingList, readerList, Issues
    WHERE r_id = rl_readerID AND
        i_id = rl_issueID
    ORDER BY rl_readerID, rl_issueID asc

--viewSpecReadingList
SELECT r_name,i_title,i_issue, rl_ownStat
FROM ReadingList, readerList, Issues
WHERE r_id = rl_readerID AND
    i_id = rl_issueID AND
    r_id = 1
ORDER BY rl_issueID asc

