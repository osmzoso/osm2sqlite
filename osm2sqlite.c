/*
** osm2sqlite - Reads OpenStreetMap XML data into a SQLite database
**
** Copyright (C) 2022 Herbert Gläser
**
*/
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <inttypes.h>
#include <libxml/tree.h>
#include <libxml/parser.h>
#include <libxml/parserInternals.h>
#include "sqlite3.h"

#define HELP \
"osm2sqlite 0.7.3 " \
"(SQLite " SQLITE_VERSION ", compiled " __DATE__ " " __TIME__ ")\n" \
"\n" \
"Reads OpenStreetMap XML data into a SQLite database.\n" \
"\n" \
"Usage:\nosm2sqlite FILE_OSM_XML FILE_SQLITE_DB [INDEX]\n" \
"\n" \
"Index control:\n" \
" -n, --no-index       No indexes are created\n" \
" -s, --spatial-index  Indexes and spatial index are created\n"

/*
** Public variables
*/
int element_node_active     = 0;  /* SAX marker within element <node>     */
int element_way_active      = 0;  /* SAX marker within element <way>      */
int element_relation_active = 0;  /* SAX marker within element <relation> */
int node_order   = 0;
int member_order = 0;
uint64_t attrib_id  = 0;
uint64_t attrib_ref = 0;
double attrib_lat = 0;
double attrib_lon = 0;
char   attrib_k[2000];    /* There is a 255 character limit for         */
char   attrib_v[2000];    /* key and value length in OSM.               */
char   attrib_type[2000]; /* Therefore 2000 characters should be enough */
char   attrib_role[2000]; /* to avoid a buffer overflow in strcpy().    */

sqlite3 *db;         /* SQLite Database connection */
int rc;              /* SQLite Result code */
sqlite3_stmt *stmt_insert_nodes, *stmt_insert_node_tags, *stmt_insert_way_nodes,
  *stmt_insert_way_tags, *stmt_insert_relation_members, *stmt_insert_relation_tags;

/*
** Abort if a database error has occurred
*/
void abort_db_error(int rc){
  fprintf(stderr, "abort - sqlite error\n");
  fprintf(stderr, "  sqlite result code   : (%i) %s\n", rc, sqlite3_errstr(rc));
  fprintf(stderr, "  sqlite error message : %s\n", sqlite3_errmsg(db));
  sqlite3_close(db);
  exit(EXIT_FAILURE);
}

/*
** Callback functions
*/
void start_element_callback(void *user_data, const xmlChar *name, const xmlChar **attrs) {

  /* check all attributes of the element */
  while( NULL!=attrs && NULL!=attrs[0] ){
    if     ( !xmlStrcmp(attrs[0], (const xmlChar *) "id") )   attrib_id  = strtoll((const char *)attrs[1], NULL, 10);
    else if( !xmlStrcmp(attrs[0], (const xmlChar *) "ref") )  attrib_ref = strtoll((const char *)attrs[1], NULL, 10);
    else if( !xmlStrcmp(attrs[0], (const xmlChar *) "lat") )  attrib_lat = atof((const char *)attrs[1]);
    else if( !xmlStrcmp(attrs[0], (const xmlChar *) "lon") )  attrib_lon = atof((const char *)attrs[1]);
    else if( !xmlStrcmp(attrs[0], (const xmlChar *) "k") )    strcpy(attrib_k,  (const char *)attrs[1]);
    else if( !xmlStrcmp(attrs[0], (const xmlChar *) "v") )    strcpy(attrib_v,  (const char *)attrs[1]);
    else if( !xmlStrcmp(attrs[0], (const xmlChar *) "type") ) strcpy(attrib_type,  (const char *)attrs[1]);
    else if( !xmlStrcmp(attrs[0], (const xmlChar *) "role") ) strcpy(attrib_role,  (const char *)attrs[1]);
    attrs = &attrs[2];
  }

  /* save data for each osm element */
  if( !xmlStrcmp(name, (const xmlChar *) "node") ){
    element_node_active = 1;
    sqlite3_bind_int64 (stmt_insert_nodes, 1, attrib_id);
    sqlite3_bind_double(stmt_insert_nodes, 2, attrib_lat);
    sqlite3_bind_double(stmt_insert_nodes, 3, attrib_lon);
    rc = sqlite3_step(stmt_insert_nodes);
    if( rc==SQLITE_DONE ){
      sqlite3_reset(stmt_insert_nodes);
    }else{
      abort_db_error(rc);
    }
  }
  else if( !xmlStrcmp(name, (const xmlChar *) "way") ){
    element_way_active = 1;
    node_order = 0;
  }
  else if( !xmlStrcmp(name, (const xmlChar *) "relation") ){
    element_relation_active = 1;
    member_order = 0;
  }
  else if( !xmlStrcmp(name, (const xmlChar *) "tag") ){
    if( element_node_active ){
      sqlite3_bind_int64(stmt_insert_node_tags, 1, attrib_id);
      sqlite3_bind_text (stmt_insert_node_tags, 2, attrib_k, -1, NULL);
      sqlite3_bind_text (stmt_insert_node_tags, 3, attrib_v, -1, NULL);
      rc = sqlite3_step(stmt_insert_node_tags);
      if( rc==SQLITE_DONE ){
        sqlite3_reset(stmt_insert_node_tags);
      }else{
        abort_db_error(rc);
      }
    }
    if( element_way_active ){
      sqlite3_bind_int64(stmt_insert_way_tags, 1, attrib_id);
      sqlite3_bind_text (stmt_insert_way_tags, 2, attrib_k, -1, NULL);
      sqlite3_bind_text (stmt_insert_way_tags, 3, attrib_v, -1, NULL);
      rc = sqlite3_step(stmt_insert_way_tags);
      if( rc==SQLITE_DONE ){
        sqlite3_reset(stmt_insert_way_tags);
      }else{
        abort_db_error(rc);
      }
    }
    if( element_relation_active ){
      sqlite3_bind_int64(stmt_insert_relation_tags, 1, attrib_id);
      sqlite3_bind_text (stmt_insert_relation_tags, 2, attrib_k, -1, NULL);
      sqlite3_bind_text (stmt_insert_relation_tags, 3, attrib_v, -1, NULL);
      rc = sqlite3_step(stmt_insert_relation_tags);
      if( rc==SQLITE_DONE ){
        sqlite3_reset(stmt_insert_relation_tags);
      }else{
        abort_db_error(rc);
      }
    }
  }
  else if( !xmlStrcmp(name, (const xmlChar *) "nd") ){
    if( element_way_active ){
      node_order++;
      sqlite3_bind_int64(stmt_insert_way_nodes, 1, attrib_id);
      sqlite3_bind_int64(stmt_insert_way_nodes, 2, attrib_ref);
      sqlite3_bind_int  (stmt_insert_way_nodes, 3, node_order);
      rc = sqlite3_step(stmt_insert_way_nodes);
      if( rc==SQLITE_DONE ){
        sqlite3_reset(stmt_insert_way_nodes);
      }else{
        abort_db_error(rc);
      }
    }
  }
  else if( !xmlStrcmp(name, (const xmlChar *) "member") ){
    if( element_relation_active ){
      member_order++;
      sqlite3_bind_int64(stmt_insert_relation_members, 1, attrib_id);
      sqlite3_bind_text (stmt_insert_relation_members, 2, attrib_type, -1, NULL);
      sqlite3_bind_int64(stmt_insert_relation_members, 3, attrib_ref);
      sqlite3_bind_text (stmt_insert_relation_members, 4, attrib_role, -1, NULL);
      sqlite3_bind_int  (stmt_insert_relation_members, 5, member_order);
      rc = sqlite3_step(stmt_insert_relation_members);
      if( rc==SQLITE_DONE ){
        sqlite3_reset(stmt_insert_relation_members);
      }else{
        abort_db_error(rc);
      }
    }
  }
}

void end_element_callback(void *user_data, const xmlChar *name) {
  if     ( !xmlStrcmp(name, (const xmlChar *) "node") )     element_node_active     = 0;
  else if( !xmlStrcmp(name, (const xmlChar *) "way") )      element_way_active      = 0;
  else if( !xmlStrcmp(name, (const xmlChar *) "relation") ) element_relation_active = 0;
}

/*
** create tables, indexes and prepared insert statements
*/
void add_tables() {
  rc = sqlite3_exec(db,
  "CREATE TABLE nodes (\n"
  " node_id      INTEGER PRIMARY KEY,  -- node ID\n"
  " lon          REAL,                 -- longitude\n"
  " lat          REAL                  -- latitude\n"
  ");\n"

  "CREATE TABLE node_tags (\n"
  " node_id      INTEGER,              -- node ID\n"
  " key          TEXT,                 -- tag key\n"
  " value        TEXT                  -- tag value\n"
  ");\n"

  "CREATE TABLE way_nodes (\n"
  " way_id       INTEGER,              -- way ID\n"
  " node_id      INTEGER,              -- node ID\n"
  " node_order   INTEGER               -- node order\n"
  ");\n"

  "CREATE TABLE way_tags (\n"
  " way_id       INTEGER,              -- way ID\n"
  " key          TEXT,                 -- tag key\n"
  " value        TEXT                  -- tag value\n"
  ");\n"

  "CREATE TABLE relation_members (\n"
  " relation_id  INTEGER,              -- relation ID\n"
  " type         TEXT,                 -- type ('node','way','relation')\n"
  " ref          INTEGER,              -- node, way or relation ID\n"
  " role         TEXT,                 -- describes a particular feature\n"
  " member_order INTEGER               -- member order\n"
  ");\n"

  "CREATE TABLE relation_tags (\n"
  " relation_id  INTEGER,              -- relation ID\n"
  " key          TEXT,                 -- tag key\n"
  " value        TEXT                  -- tag value\n"
  ");\n",
  NULL, NULL, NULL);
  if( rc!=SQLITE_OK ) abort_db_error(rc);
}

void create_prep_stmt() {
  #define SQL_INSERT_NODES "INSERT INTO nodes (node_id,lat,lon) VALUES (?1,?2,?3)"
  rc = sqlite3_prepare_v2(db, SQL_INSERT_NODES, -1, &stmt_insert_nodes, NULL);
  if( rc!=SQLITE_OK ) abort_db_error(rc);
  #define SQL_INSERT_NODE_TAGS "INSERT INTO node_tags (node_id,key,value) VALUES (?1,?2,?3)"
  rc = sqlite3_prepare_v2(db, SQL_INSERT_NODE_TAGS, -1, &stmt_insert_node_tags, NULL);
  if( rc!=SQLITE_OK ) abort_db_error(rc);
  #define SQL_INSERT_WAY_NODES "INSERT INTO way_nodes (way_id,node_id,node_order) VALUES (?1,?2,?3)"
  rc = sqlite3_prepare_v2(db, SQL_INSERT_WAY_NODES, -1, &stmt_insert_way_nodes, NULL);
  if( rc!=SQLITE_OK ) abort_db_error(rc);
  #define SQL_INSERT_WAY_TAGS "INSERT INTO way_tags (way_id,key,value) VALUES (?1,?2,?3)"
  rc = sqlite3_prepare_v2(db, SQL_INSERT_WAY_TAGS, -1, &stmt_insert_way_tags, NULL);
  if( rc!=SQLITE_OK ) abort_db_error(rc);
  #define SQL_INSERT_RELATION_MEMBERS "INSERT INTO relation_members (relation_id,type,ref,role,member_order) VALUES (?1,?2,?3,?4,?5)"
  rc = sqlite3_prepare_v2(db, SQL_INSERT_RELATION_MEMBERS, -1, &stmt_insert_relation_members, NULL);
  if( rc!=SQLITE_OK ) abort_db_error(rc);
  #define SQL_INSERT_RELATION_TAGS "INSERT INTO relation_tags (relation_id,key,value) VALUES (?1,?2,?3)"
  rc = sqlite3_prepare_v2(db, SQL_INSERT_RELATION_TAGS, -1, &stmt_insert_relation_tags, NULL);
  if( rc!=SQLITE_OK ) abort_db_error(rc);
}

void destroy_prep_stmt() {
  sqlite3_finalize(stmt_insert_nodes);
  sqlite3_finalize(stmt_insert_node_tags);
  sqlite3_finalize(stmt_insert_way_nodes);
  sqlite3_finalize(stmt_insert_way_tags);
  sqlite3_finalize(stmt_insert_relation_members);
  sqlite3_finalize(stmt_insert_relation_tags);
}

void add_std_index() {
  rc = sqlite3_exec(db,
  "CREATE INDEX node_tags__node_id            ON node_tags (node_id);\n"
  "CREATE INDEX node_tags__key                ON node_tags (key);\n"
  "CREATE INDEX way_tags__way_id              ON way_tags (way_id);\n"
  "CREATE INDEX way_tags__key                 ON way_tags (key);\n"
  "CREATE INDEX way_nodes__way_id             ON way_nodes (way_id);\n"
  "CREATE INDEX way_nodes__node_id            ON way_nodes (node_id);\n"
  "CREATE INDEX relation_members__relation_id ON relation_members (relation_id);\n"
  "CREATE INDEX relation_members__type        ON relation_members (type, ref);\n"
  "CREATE INDEX relation_tags__relation_id    ON relation_tags (relation_id);\n"
  "CREATE INDEX relation_tags__key            ON relation_tags (key);\n",
  NULL, NULL, NULL);
  if( rc!=SQLITE_OK ) abort_db_error(rc);
}

void add_rtree(char *table) {
  char query[1000] =
  "CREATE VIRTUAL TABLE ";strcat(query, table);strcat(query, " USING rtree(way_id, min_lat, max_lat, min_lon, max_lon);\n"
  "INSERT INTO ");strcat(query, table);strcat(query, " (way_id, min_lat, max_lat, min_lon, max_lon)\n"
  "SELECT way_tags.way_id,min(nodes.lat),max(nodes.lat),min(nodes.lon),max(nodes.lon)\n"
  "FROM way_tags\n"
  "LEFT JOIN way_nodes ON way_tags.way_id=way_nodes.way_id\n"
  "LEFT JOIN nodes ON way_nodes.node_id=nodes.node_id\n"
  "WHERE way_tags.key='");strcat(query, table);strcat(query, "'\n"
  "GROUP BY way_tags.way_id;\n");
  rc = sqlite3_exec(db, query, NULL, NULL, NULL);
  if( rc!=SQLITE_OK ) abort_db_error(rc);
}

void add_addr() {
  rc = sqlite3_exec(db,
  "--\n"
  "-- Create address tables with coordinates\n"
  "--\n"
  "BEGIN TRANSACTION;\n"
  "--\n"
  "DROP TABLE IF EXISTS addr_street;\n"
  "DROP TABLE IF EXISTS addr_housenumber;\n"
  "DROP VIEW IF EXISTS addr_view;\n"
  "--\n"
  "-- 1. Determine address data from way tags\n"
  "--\n"
  "CREATE TEMP TABLE tmp_addr_way (\n"
  " way_id      INTEGER PRIMARY KEY,\n"
  " postcode    TEXT,\n"
  " city        TEXT,\n"
  " street      TEXT,\n"
  " housenumber TEXT\n"
  ");\n"
  "INSERT INTO tmp_addr_way\n"
  " SELECT way_id,value AS postcode,'','',''\n"
  " FROM way_tags WHERE key='addr:postcode'\n"
  " ON CONFLICT(way_id) DO UPDATE SET postcode=excluded.postcode;\n"
  "INSERT INTO tmp_addr_way\n"
  " SELECT way_id,'',value AS city,'',''\n"
  " FROM way_tags WHERE key='addr:city'\n"
  " ON CONFLICT(way_id) DO UPDATE SET city=excluded.city;\n"
  "INSERT INTO tmp_addr_way\n"
  " SELECT way_id,'','',value AS street,''\n"
  " FROM way_tags WHERE key='addr:street'\n"
  " ON CONFLICT(way_id) DO UPDATE SET street=excluded.street;\n"
  "INSERT INTO tmp_addr_way\n"
  " SELECT way_id,'','','',value AS housenumber\n"
  " FROM way_tags WHERE key='addr:housenumber'\n"
  " ON CONFLICT(way_id) DO UPDATE SET housenumber=excluded.housenumber;\n"
  "--\n"
  "-- 2. Calculate coordinates of address data from way tags\n"
  "--\n"
  "CREATE TEMP TABLE tmp_addr_way_coordinates AS\n"
  "SELECT way.way_id AS way_id,round(avg(n.lon),7) AS lon,round(avg(n.lat),7) AS lat\n"
  "FROM tmp_addr_way AS way\n"
  "LEFT JOIN way_nodes AS wn ON way.way_id=wn.way_id\n"
  "LEFT JOIN nodes     AS n  ON wn.node_id=n.node_id\n"
  "GROUP BY way.way_id;\n"
  "CREATE INDEX tmp_addr_way_coordinates_way_id ON tmp_addr_way_coordinates (way_id);\n"
  "--\n"
  "-- 3. Determine address data from node tags\n"
  "--\n"
  "CREATE TEMP TABLE tmp_addr_node (\n"
  " node_id     INTEGER PRIMARY KEY,\n"
  " postcode    TEXT,\n"
  " city        TEXT,\n"
  " street      TEXT,\n"
  " housenumber TEXT\n"
  ");\n"
  "INSERT INTO tmp_addr_node\n"
  " SELECT node_id,value AS postcode,'','',''\n"
  " FROM node_tags WHERE key='addr:postcode'\n"
  " ON CONFLICT(node_id) DO UPDATE SET postcode=excluded.postcode;\n"
  "INSERT INTO tmp_addr_node\n"
  " SELECT node_id,'',value AS city,'',''\n"
  " FROM node_tags WHERE key='addr:city'\n"
  " ON CONFLICT(node_id) DO UPDATE SET city=excluded.city;\n"
  "INSERT INTO tmp_addr_node\n"
  " SELECT node_id,'','',value AS street,''\n"
  " FROM node_tags WHERE key='addr:street'\n"
  " ON CONFLICT(node_id) DO UPDATE SET street=excluded.street;\n"
  "INSERT INTO tmp_addr_node\n"
  " SELECT node_id,'','','',value AS housenumber\n"
  " FROM node_tags WHERE key='addr:housenumber'\n"
  " ON CONFLICT(node_id) DO UPDATE SET housenumber=excluded.housenumber;\n"
  "--\n"
  "-- 4. Create temporary overall table with all addresses\n"
  "--\n"
  "CREATE TEMP TABLE tmp_addr (\n"
  " addr_id     INTEGER PRIMARY KEY,\n"
  " way_id      INTEGER,\n"
  " node_id     INTEGER,\n"
  " postcode    TEXT,\n"
  " city        TEXT,\n"
  " street      TEXT,\n"
  " housenumber TEXT,\n"
  " lon         REAL,\n"
  " lat         REAL\n"
  ");\n"
  "INSERT INTO tmp_addr (way_id,node_id,postcode,city,street,housenumber,lon,lat)\n"
  " SELECT w.way_id,-1 AS node_id,w.postcode,w.city,w.street,w.housenumber,c.lon,c.lat\n"
  " FROM tmp_addr_way AS w\n"
  " LEFT JOIN tmp_addr_way_coordinates AS c ON w.way_id=c.way_id\n"
  "UNION ALL\n"
  " SELECT -1 AS way_id,n.node_id,n.postcode,n.city,n.street,n.housenumber,c.lon,c.lat\n"
  " FROM tmp_addr_node AS n\n"
  " LEFT JOIN nodes AS c ON n.node_id=c.node_id\n"
  "ORDER BY postcode,city,street,housenumber;\n"
  "--\n"
  "-- 5. Create tables 'addr_street' and 'addr_housenumber' and view 'addr_view' (normalize tables)\n"
  "--\n"
  "CREATE TABLE addr_street (\n"
  " street_id   INTEGER PRIMARY KEY,\n"
  " postcode    TEXT,\n"
  " city        TEXT,\n"
  " street      TEXT,\n"
  " min_lon     REAL,\n"
  " min_lat     REAL,\n"
  " max_lon     REAL,\n"
  " max_lat     REAL\n"
  ");\n"
  "INSERT INTO addr_street (postcode,city,street,min_lon,min_lat,max_lon,max_lat)\n"
  " SELECT postcode,city,street,min(lon),min(lat),max(lon),max(lat)\n"
  " FROM tmp_addr\n"
  " GROUP BY postcode,city,street;\n"
  "CREATE INDEX addr_street_1 ON addr_street (postcode,city,street);\n"
  "CREATE TABLE addr_housenumber (\n"
  " housenumber_id INTEGER PRIMARY KEY,\n"
  " street_id      INTEGER,\n"
  " housenumber    TEXT,\n"
  " lon            REAL,\n"
  " lat            REAL,\n"
  " way_id         INTEGER,\n"
  " node_id        INTEGER\n"
  ");\n"
  "INSERT INTO addr_housenumber (street_id,housenumber,lon,lat,way_id,node_id)\n"
  " SELECT s.street_id,a.housenumber,a.lon,a.lat,a.way_id,a.node_id\n"
  " FROM tmp_addr AS a\n"
  " LEFT JOIN addr_street AS s ON a.postcode=s.postcode AND a.city=s.city AND a.street=s.street;\n"
  "CREATE INDEX addr_housenumber_1 ON addr_housenumber (street_id);\n"
  "--\n"
  "CREATE VIEW addr_view AS\n"
  "SELECT s.street_id,s.postcode,s.city,s.street,h.housenumber,h.lon,h.lat,h.way_id,h.node_id\n"
  "FROM addr_street AS s\n"
  "LEFT JOIN addr_housenumber AS h ON s.street_id=h.street_id;\n"
  "--\n"
  "-- 6. Delete temporary tables\n"
  "--\n"
  "DROP TABLE tmp_addr_way;\n"
  "DROP TABLE tmp_addr_way_coordinates;\n"
  "DROP TABLE tmp_addr_node;\n"
  "DROP TABLE tmp_addr;\n"
  "--\n"
  "COMMIT TRANSACTION;\n"
  "\n",
  NULL, NULL, NULL);
  if( rc!=SQLITE_OK ) abort_db_error(rc);
}

/*
** Main
*/
int main(int argc, char **argv){
  /* Parameter check */
  int flag_create_index = 1;
  int flag_create_sindex = 0;
  int flag_addr = 0;
  if( argc==3 || argc==4 ){
    if( argc==4 ){
      if( strcmp("-n", argv[3])==0 || strcmp("--no-index", argv[3])==0 ){
        flag_create_index = 0;
      }
      if( strcmp("-s", argv[3])==0 || strcmp("--spatial-index", argv[3])==0 ){
        flag_create_index = 1;
        flag_create_sindex = 1;
      }
      if( strcmp("addr", argv[3])==0 ) flag_addr = 1;
    }
  }else{
    printf(HELP);
    return EXIT_FAILURE;
  }

  /* Database connection */
  rc = sqlite3_open(argv[2], &db);
  if( rc!=SQLITE_OK ) abort_db_error(rc);
  sqlite3_exec(db, "PRAGMA journal_mode = OFF", NULL, NULL, NULL); /* db tuning */
  sqlite3_exec(db, "PRAGMA page_size = 65536", NULL, NULL, NULL);

  /* SAX handler */
  xmlSAXHandler sh = { 0 };                 /* initialize all fields to zero   */
  sh.startElement = start_element_callback; /* register callback functions     */
  sh.endElement = end_element_callback;
  xmlParserCtxtPtr ctxt;                    /* create context                  */
  if( (ctxt = xmlCreateFileParserCtxt(argv[1]))==NULL ){
    fprintf(stderr, "SAX Error : creating context failed\n");
    return EXIT_FAILURE;
  }
  xmlCtxtUseOptions(ctxt, XML_PARSE_NOENT); /* substitute entities, e.g. &amp; */
  ctxt->sax = &sh;                          /* register sax handler in context */

  /* Read the data */
  sqlite3_exec(db, "BEGIN TRANSACTION", NULL, NULL, NULL);
  add_tables();            /* create all tables                     */
  create_prep_stmt();      /* create prepared insert statements     */
  xmlParseDocument(ctxt);  /* read and parse the XML document       */
  if( !ctxt->wellFormed ) fprintf(stderr, "XML document isn't well formed\n");
  if( flag_create_index ) add_std_index();       /* standard indexes                   */
  if( flag_create_sindex ) add_rtree("highway"); /* R*Tree for ways with key='highway' */
  sqlite3_exec(db, "COMMIT", NULL, NULL, NULL);
  if( flag_addr ) add_addr();                    /* create address tables */
  destroy_prep_stmt();     /* destroy prepared statements           */
  sqlite3_close(db);       /* close the database                    */

  return EXIT_SUCCESS;
}

