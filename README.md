Kiva JSON Snapshot to SQLite database
=============

## Kiva dump
The Kiva dump can be downloaded from [this page](http://build.kiva.org/)

## Database
The script *createDb.py* creates an SQLite database of schema

![database diagram](https://github.com/fraba/Kiva-JSON-Snapshot-to-SQLite/blob/master/database-diagram.png)

The script takes one mandatory argument: the SQLite database file to create.

```
createDb.py database.db
```

## JSON parsing
The script *parseKivaDump.py* parses the three directories of the Kiva dump and enters the data into the relational database.

The script takes two mandatory arguments: the parent directory of the Kiva dump and the SQLite database file.

```
parseKivaDump.py /path/to/kiva/dump/dir database.db
```

