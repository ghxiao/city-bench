city-bench
==========

`city-bench` is a publicly available geographic datasets for OBDA systems.

The benchmarks are created in a simple and extensible way by
employing a rule-based data transformation language to extract
instance data from OpenStreetMap (OSM) geospatial data.

Directories in this repository are:

* [cities](cities): pre-generated OWL files for selected cities
* [queries](queries): predefined SPARQL queries
* [tools](tools): data generation tools, which you can use to create your own benchmark
* [mappings](mappings): a collection of mappings to generate the cities instances 

Data Generation Tools
---------------------

`generate.py` is a Python 2.7 script that resembles the extract, transform, and 
load (ETL) process of classical data transformation tools.  

```console
$ generate.py --mappingFile file.txt  --verbose
```


Mapping Language Syntax
-----------------------

A mapping file has two seperate sections. The first section is 
concerned with general defintions as connection strings 
for databases, file names, scripts, and simple constants. 
The following definitions are possible:

* Postgres connections 

⋅⋅⋅The connection strings for Postgres connection have the the syntax `CONNECTION id: conn_string`.
⋅⋅⋅We use the standard data source name notation for conn_string.  
⋅⋅⋅`CONNECTION id1: HOST=localhost PORT=5432 DBNAME=test USER=postgres PASSWORD=secret`

* Files

* Python scripts

* Constants


The second section contains the mapping axioms, which define a 
single ETL step.


Contacts
--------
* [Thomas Eiter](http://www.kr.tuwien.ac.at/staff/eiter/)
* [Patrik Schneider](http://www.kr.tuwien.ac.at/staff/patrik/)
* [Mantas Simkus](http://www.dbai.tuwien.ac.at/staff/simkus/)
* [Guohui Xiao](http://www.ghxiao.org)
