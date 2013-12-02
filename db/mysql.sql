DROP TABLE IF EXISTS job;
CREATE TABLE job (
  guid CHAR(32) PRIMARY KEY,
  title TEXT,
  url TEXT,
  company TEXT,
  location TEXT,
  salary TEXT,
  source TEXT,
  updated DATETIME
) DEFAULT CHARSET=utf8;

