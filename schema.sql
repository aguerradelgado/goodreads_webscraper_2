PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS book;

CREATE TABLE book (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title varchar(20) NOT NULL,
    Author varchar(20) NOT NULL,
    Genre varchar(20) NOT NULL,
    Cover varchar(8000)

);

DROP TABLE IF EXISTS BookTable;

CREATE TABLE BookTable (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title varchar(20) NOT NULL UNIQUE,
    Author varchar(20) NOT NULL,
    Genre varchar(20) NOT NULL,
    Cover varchar(8000)
);

DROP TABLE IF EXISTS user;

CREATE TABLE user (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    email varchar(20) NOT NULL
);


DROP TABLE IF EXISTS TBR;

CREATE TABLE TBR (
   U_ID INTEGER,
   B_ID INTEGER,
   added TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (U_ID) REFERENCES user(ID),
   FOREIGN KEY (B_ID) REFERENCES book(ID)


);