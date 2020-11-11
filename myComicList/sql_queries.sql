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
DROP TABLE ReadingList;
DROP TABLE FollowList;
DROP TABLE Artist;
DROP TABLE Writer;
DROP TABLE ReccList;










.mode "csv"
.separator "\t"
.import /home/tyler/Documents/cse-111/final_project/cse-111-project/data/pull_w_tabs.txt Issues


