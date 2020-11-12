--Create all tables
CREATE TABLE Issues (
    i_id decimal(9,0) NOT NULL PRIMARY KEY,
    i_title char(50) NOT NULL,
    i_issue char(50), --considering removing this
    i_date date(4,0) NOT NULL,
    i_srp decimal(2,2) NOT NULL
);

CREATE TABLE readerList(
    r_id  decimal(9,0) NOT NULL PRIMARY KEY,
    r_name char(50) NOT NULL);

CREATE TABLE ReadingList(
    rl_readerID decimal(9,0) NOT NULL,
    rl_issueID char(4)  NOT NULL,
    rl_ownStat char(10) NOT NULL
);

CREATE TABLE FollowList(
    fl_id decimal(9,0) NOT NULL PRIMARY KEY,
    --Do i need to change this part?
    fl_artistID decimal(9,0) NOT NULL,
    fl_writerID decimal(9,0) NOT NULL
);

CREATE TABLE Artist(
    a_id decimal(9,0) NOT NULL PRIMARY KEY,
    a_name char(50) NOT NULL
);

CREATE TABLE Writer(
    w_id decimal(9,0) NOT NULL PRIMARY KEY,
    w_name char(50) NOT NULL
);

CREATE TABLE ReccList(
    r_aId decimal(9,0) NOT NULL,
    r_wId decimal(9,0) NOT NULL,
    r_readerID decimal(9,0) NOT NULL,
    r_issueID decimal(9,0) NOT NULL
)

--Drop all tables
DROP TABLE Issues;
DROP TABLE readerList
DROP TABLE ReadingList;
DROP TABLE FollowList;
DROP TABLE Artist;
DROP TABLE Writer;
DROP TABLE ReccList;

.mode "csv"
.separator "\t"
.import /home/tyler/Documents/cse-111/final_project/cse-111-project/data/pull_w_tabs.txt Issues

INSERT INTO readerList(r_id, r_name) VALUES (1, 'Tyler')
DELETE FROM readerList WHERE r_name = 'Tyler'

SELECT * 
FROM readerList

INSERT INTO ReadingList(rl_readerID, rl_issueID, rl_ownStat) VALUES (1, 1, 'Yes')
INSERT INTO ReadingList(rl_readerID, rl_issueID, rl_ownStat) VALUES (2, 4, 'No')
INSERT INTO ReadingList(rl_readerID, rl_issueID, rl_ownStat) VALUES (3, 7, 'Yes')
DELETE FROM ReadingList WHERE rl_ownStat = 'Yes'
UPDATE ReadingList SET rl_ownStat = 'Yes'

SELECT * 
FROM ReadingList


UPDATE readerList
SET r_id = (r_id - 1)
WHERE r_id > ?

SELECT w_name AS 'Writers', a_name AS 'Artists'
FROM FollowList, Writer,Artist
WHERE a_id = fl_issueID AND
        w_id = fl_issueID AND
        fl_id = 5

    
SELECT r_name,i_title,i_issue
FROM ReadingList, readerList, Issues
WHERE r_id = rl_readerID AND
    i_id = rl_issueID
ORDER BY rl_readerID, rl_issueID asc


SELECT r_name,i_title,i_issue, a_name, w_name
FROM ReadingList, readerList, Issues, Artist, Writer
WHERE r_id = rl_readerID AND
    i_id = rl_issueID AND
    r_id = 3 AND 
    w_id = i_id AND
    a_id = i_id
ORDER BY rl_issueID asc



---------------------------
SELECT issueName, Writers, writerQ.Artists
FROM
(
    
    SELECT issueName, Writers, Artists--* 
    FROM
    (
    SELECT fl_id , w_name AS 'Writers', a_name AS 'Artists', fl_issueID AS sq1_id, *
    FROM FollowList, Writer,Artist
    WHERE a_id = fl_issueID AND
        w_id = fl_issueID AND
        fl_id = 5
    )sq1,

    (
    SELECT i_id AS sq2_id, i_title || i_issue AS issueName, w_name AS sqW
    FROM Issues,Writer,Artist
    WHERE i_id = w_id AND
        i_id = a_id
    )
    sq2

    WHERE Writers = sqW 
) writerQ,


(
    
    SELECT issueName2, Artists--* 
    FROM
    (
    SELECT fl_id , w_name AS 'Writers', a_name AS 'Artists', fl_issueID AS sq1_id, *
    FROM FollowList, Writer,Artist
    WHERE a_id = fl_issueID AND
        w_id = fl_issueID AND
        fl_id = 5
    )sq1,

    (
    SELECT i_id AS sq2_id, i_title || i_issue AS issueName2, a_name AS sqA
    FROM Issues,Writer,Artist
    WHERE i_id = w_id AND
        i_id = a_id
    )
    sq2

    WHERE Artists = sqA 
) ArtistQ
WHERE issueName = issueName2



----------------------

SELECT issueName, Writers, writerQ.Artists
FROM
(
    --Grabs all books written by the followed arthors
    SELECT issueName, Writers, Artists--* 
    FROM
    --Grabs artists and writers followed info
    (
    SELECT fl_id , w_name AS 'Writers', a_name AS 'Artists', fl_issueID AS sq1_id, *
    FROM FollowList, Writer,Artist
    WHERE a_id = fl_issueID AND
        w_id = fl_issueID AND
        fl_id = 5
    )sq1,

    --Grabs list of issues with wrtier and artist names
    (
    SELECT i_id AS sq2_id, i_title || i_issue AS issueName, w_name AS sqW
    FROM Issues,Writer,Artist
    WHERE i_id = w_id AND
        i_id = a_id
    )
    sq2

    WHERE Writers = sqW 
    
) writerQ,


(
    
    SELECT issueName2, Artists--* 
    FROM
    (
    SELECT fl_id , w_name AS 'Writers', a_name AS 'Artists', fl_issueID AS sq1_id, *
    FROM FollowList, Writer,Artist
    WHERE a_id = fl_issueID AND
        w_id = fl_issueID AND
        fl_id = 5
    )swq1,

    (
    SELECT i_id AS sq2_id, i_title || i_issue AS issueName2, a_name AS sqA
    FROM Issues,Writer,Artist
    WHERE i_id = w_id AND
        i_id = a_id
    )
    sq2

    WHERE Artists = sqA 
) ArtistQ
WHERE issueName = issueName2



------------
--Selects selects books with the same writers
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
    fl_id = 1 --use 5 to test multi
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

INSERT INTO ReccList(r_readerID, r_issueID) VALUES (?, ?)
DELETE FROM readerList WHERE r_name = 'Tyler'

SELECT (i_title || i_issue) AS issueTitle, i_date, i_srp
FROM Issues, ReccList
WHERE i_id = r_issueID AND
    r_readerID = ?
