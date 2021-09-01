CREATE TABLE version (
    major int NOT NULL,
    minor int NOT NULL
    );
INSERT INTO version VALUES (1,0);
   
CREATE TABLE strings (
    context varchar(255) NOT NULL,
    id      varchar(255) NOT NULL,
    expires timestamp    NOT NULL,
    version smallint     NOT NULL,
    value   varchar(255) NOT NULL,
    PRIMARY KEY (context, id)
    );
   
CREATE TABLE texts (
    context varchar(255) NOT NULL,
    id      varchar(255) NOT NULL,
    expires timestamp    NOT NULL,
    version smallint     NOT NULL,
    value   text         NOT NULL,
    PRIMARY KEY (context, id)
    );
