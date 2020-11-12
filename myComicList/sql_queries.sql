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


SELECT r_name,i_title,i_issue
FROM ReadingList, readerList, Issues
WHERE r_id = rl_readerID AND
    i_id = rl_issueID AND
    r_id = 3
ORDER BY rl_issueID asc

