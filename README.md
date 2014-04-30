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

`generate.py` is a Python 2.7 script that resembles the extract,
transform, and load (ETL) process of classical data transformation
tools. The main input is the mapping file which contains ETL steps
specified in the next section. The only external library need is the
psycopg2 (https://pypi.python.org/pypi/psycopg2), which is the
PostgreSQL//PostGIS database adapter.

```console $ generate.py --mappingFile file.txt --verbose ```

`spatialRelationsReader.py` is an example implemenation of an external
script which acts as a data source and calculates the spatial
relations (e.g., contains, next, etc.) between two input RDF files,
The files should contain individuals with roles from GeoRSS (e.g.,
geo:point) assigned to them. As an external library shapely
(https://pypi.python.org/pypi/Shapely) and GDAL is needed
(http://trac.osgeo.org/gdal/wiki/GdalOgrInPython).

Mapping Language Syntax
-----------------------

A mapping file has two seperate sections. The first section is 
concerned with general defintions as connection strings 
for databases, file names, scripts, and simple constants. 
The following definitions are possible, where `id`is the 
reference which has to be used in the mapping axioms:

* Postgres//PostGIS connections: `CONNECTION id: conn_string`

   Connection are used for reading and writing to a (geospatial) database. We assume the standard data source name notation for conn_string, , e.g.,
   
   `CONNECTION id1: HOST=localhost PORT=5432 DBNAME=test USER=postgres PASSWORD=secret`

* Text files: `FILE id: file_string`

   Any text file can function as an input/output source and is read/written line-by-line, where `file_string` has to contain `name=` to define the file url and optional `delimiter=' '`to define the field separator, e.g.,
   
   `FILE id2: name=/Users/patrik/test.csv delimiter=';'`
   

* Python scripts: `SCRIPT id: script_string`
 
   Scripts are eiter used as input sources or as a transform step for converting values. `script_string` is simply the url of the script file. Note that for input scripts, the methods `open()` and `read()` have to be implemented. In the read method tuples have to be returned by the python command `yield`. E.g., 

   `SCRIPT id3: ./spatialRelationsReader.py`

* Constants: `CONST id: const_string`

   Constants are simple strings which are mainly used to write @prefix, @base, ow:imports to output files, e.g.,
   
   `CONST id4: @prefix  geo: <http://www.georss.org/georssl/>`


The second section contains the mapping axioms, which define a 
single ETL step, the syntax is an extension of the ontop mapping language 
(https://github.com/ontop/ontop/wiki/ObdalibObdaTurtlesyntax).




Contacts
--------
* [Thomas Eiter](http://www.kr.tuwien.ac.at/staff/eiter/)
* [Patrik Schneider](http://www.kr.tuwien.ac.at/staff/patrik/)
* [Mantas Simkus](http://www.dbai.tuwien.ac.at/staff/simkus/)
* [Guohui Xiao](http://www.ghxiao.org)
