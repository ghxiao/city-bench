city-bench
==========

`city-bench` is a publicly available collection of geographic datasets for OBDA systems.

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
script, which acts as a data source and calculates the spatial
relations (e.g., contains, next, etc.) between two input RDF files.
The files have to contain individuals with roles from GeoRSS (e.g.,
geo:point) assigned to them. As an external library shapely
(https://pypi.python.org/pypi/Shapely) and GDAL is needed
(http://trac.osgeo.org/gdal/wiki/GdalOgrInPython). The parameter 
for the script are `relation file1 file2 distance`.

`streetGraphReader.py` is another implementation of a  external script
reader. In this reader the input are objects which represent roads in OSM.
From the objects and their geometry (e.g. geo:line) all the nodes and 
edges of the street graph are extracted. The parameter 
for the script are `type` to chose between nodes/edges and `file`.


`transformOSMConcepts.py` is a simple tranformation script for 
converting OSM categories (e.g., restaurant) to concepts.

Mapping Language Syntax
-----------------------

A mapping file has two seperate sections. The first section is 
concerned with general defintions as connection strings 
for databases, file names, scripts, and simple constants. 
A line is ignored and treated a comment if it starts with `#`.

The following definitions are available, where `id` is the  
reference which has to be used in the mapping axioms:

* Postgres/PostGIS connections: `CONNECTION id: conn_string`

   Connection are used for reading and writing from/to (geospatial) databases. We assume the standard data source name notation for conn_string, e.g.,
   
   `CONNECTION id1: HOST=localhost PORT=5432 DBNAME=test USER=postgres PASSWORD=secret`

* Text files: `FILE id: file_string`

   Any text file can function as an input/output source and is read/written line-by-line, where `file_string` has to contain `name=` to define the file url and optional `delimiter=' '`to define the field separator, e.g.,
   
   `FILE id2: name=/Users/patrik/test.csv delimiter=';'`
   

* Python scripts: `SCRIPT id: script_string`
 
   Scripts are eiter used as input sources or as a transformation step for converting values. `script_string` is simply the url of the script file. For instance, 

   `SCRIPT id3: ./spatialRelationsReader.py`

* Constants: `CONST id: const_string`

   Constants are simple strings which are mainly used to write @prefix, @base, ow:imports to output files, e.g.,
   
   `CONST id4: @prefix  geo: <http://www.georss.org/georssl/>`


The second section contains the mapping axioms. An axiom defines a 
single ETL step, the syntax is an extension of the ontop mapping language 
(https://github.com/ontop/ontop/wiki/ObdalibObdaTurtlesyntax).
A mapping axiom has an id and is defined either as a pair of `source` and `target`
or as the triple of `source`, `transform`, and `target`:

<pre>
mappingId map_id
source source_id source_parameter
transform transform_id transform_parameter
target target_id target_parameter
</pre>

The sources `source source_id source_parameter` have to be configured according 
to the type of source:

* Postgres/PostGIS relations: `connection_id  sql_statement`

   The `connection_id` refers to `CONNECTION` from the defintions. 
`sql_statement` defines the SQL "Select-From-Where" statement which is
executed on the refered database.  The result can be processed a set
of n-tuples, which can be accessed by its index in the `target` step. For instance, 

   `source id1  SELECT osm_id, name, ST_AsEWKT(way) AS geo FROM planet_osm_polygon WHERE leisure = 'park'`, reads all the parks (spatial objects) from OSM.


* Text files: `file_id reg_exp`

   Text files are directly linked to the definition in `FILE`. The refered file is read line-by-line resulting in an n-tuple base on the field delimiter. If `reg_exp` is empty all lines are returned, otherwise only the line which fullfile the regular expression are returned. For instance, 
   
   `source id2`

* Python scripts:  `script_id parameter`

    Scripts are the main option to extend the benchmark creation i.a. with the calculation of spatial relations. `parameter` are entered separated by space and can be either constant texts (in double quotes) or variables, which are replaced with the corresponding value on run time. Note that scripts are treated as a data source, hence the methods `open(parameter)` and `read()` have to be implemented.  In the read method n-tuples have to be returned by the python command `yield`.

   `source id3 "contains" id2 id2`, which calls the spatialRelationsReader.py script to calculate the "contains" relation with the same file as the input

* Constants: `constant c_id1 c_id2 ...`

    Constants are the simplest sources and directly written to the target. It is possible to assign a sequence of constants to a single writing step.

   `source constant id4`
   
The targets `target target_id target_parameter` have to be configured according to the type 
of source:

* Postgres/PostGIS relations: `connection_id  sql_statement`

   The `connection_id` is as in the sources, 'sql_statement` defines the SQL "Insert" statement as 
a template, which writes the n-tuples from the source into the database. E.g.,

``` 
    target osm1 INSERT INTO table1 (subj, pred, obj) VALUES('{1}', '{2}', '{3}');
```

* Text files: `file_id output_text`

   The `file_id` is as in the sources, 'output_text` is a textual template, which is written to the file. It can contain as single or multiple lines.  Usually, it will represent triples, which are used for the reasoner. For instance, 

``` 
    target f3  :{1} rdf:type tuwt:Playground, owl:NamedIndividual;
               gml:featurename "{2}"^^xsd:string; 
               geo:polygon "{3}"^^xsd:string.
```

* Console: `stdout output_text`
   For testing purposes, writing to the console is achieved by using `stdout`



Contacts
--------
* [Thomas Eiter](http://www.kr.tuwien.ac.at/staff/eiter/)
* [Patrik Schneider](http://www.kr.tuwien.ac.at/staff/patrik/)
* [Mantas Simkus](http://www.dbai.tuwien.ac.at/staff/simkus/)
* [Guohui Xiao](http://www.ghxiao.org)
