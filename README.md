Kiva JSON Snapshot to SQLite database
=============

## Kiva dump
The Kiva dump can be downloaded from [this page](http://build.kiva.org/)

## Database
The script *createdb.py* creates an SQLite database of schema

![database diagram](https://github.com/fraba/Kiva-JSON-Snapshot-to-SQLite/blob/master/database-diagram.png)

## JSON parsing
The script *parseKivaDump.py* parses the three directories of the Kiva dump and enters the data into the relational database

