DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FirstName VARCHAR(20) NOT NULL,
    LastName VARCHAR(20) NOT NULL,
    Age Integer(3),
    Street VARCHAR(30),    
    Apartment VARCHAR(10),
    Zipcode Integer(10),
    State VARCHAR(10),
    Email VARCHAR(30),
    Budget Float(10,2) NOT NULL,
    Base  Float(10,2)
);
