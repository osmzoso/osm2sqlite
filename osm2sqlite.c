/*
** osm2sqlite - Reads OpenStreetMap XML data into a SQLite database
**
** Copyright (C) 2022 Herbert Gläser
**
** TODOs:
** Uses Module SAX from libxml2 (deprecated)
** http://xmlsoft.org/html/libxml-SAX.html
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

#define OSM2SQLITE_VERSION "0.6.0"
#define OSM2SQLITE_HELP_INFO \
"osm2sqlite (Version " OSM2SQLITE_VERSION ")\n\n" \
"Reads OpenStreetMap XML data into a SQLite database.\n\n" \
"Usage:\nosm2sqlite FILE_OSM_XML FILE_SQLITE_DB [INDEX]\n\n" \
"Index control:\n" \
" -n, --no-index       No indexes are created\n" \
" -s, --spatial-index  Indexes and spatial index are created\n\n" \
"(SQLite Version " SQLITE_VERSION ")\n" \
"(compile time: " __DATE__ " " __TIME__ "  gcc " __VERSION__ ")\n"

/*
** Public variable for the SAX parser
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
char *zErrMsg = 0;   /* SQLite Error message */
int rc;              /* SQLite Return code */
sqlite3_stmt *stmt_insert_nodes, *stmt_insert_node_tags, *stmt_insert_way_nodes,
  *stmt_insert_way_tags, *stmt_insert_relation_members, *stmt_insert_relation_tags;

/*
** Callback functions
*/
void start_element_callback(void *user_data, const xmlChar *name, const xmlChar **attrs) {

  /* check all attributes of the element */
  while (NULL != attrs && NULL != attrs[0]) {
    if     (!xmlStrcmp(attrs[0], (const xmlChar *)"id"))   attrib_id  = strtoll((const char *)attrs[1], NULL, 10);
    else if(!xmlStrcmp(attrs[0], (const xmlChar *)"ref"))  attrib_ref = strtoll((const char *)attrs[1], NULL, 10);
    else if(!xmlStrcmp(attrs[0], (const xmlChar *)"lat"))  attrib_lat = atof((const char *)attrs[1]);
    else if(!xmlStrcmp(attrs[0], (const xmlChar *)"lon"))  attrib_lon = atof((const char *)attrs[1]);
    else if(!xmlStrcmp(attrs[0], (const xmlChar *)"k"))    strcpy(attrib_k,  (const char *)attrs[1]);
    else if(!xmlStrcmp(attrs[0], (const xmlChar *)"v"))    strcpy(attrib_v,  (const char *)attrs[1]);
    else if(!xmlStrcmp(attrs[0], (const xmlChar *)"type")) strcpy(attrib_type,  (const char *)attrs[1]);
    else if(!xmlStrcmp(attrs[0], (const xmlChar *)"role")) strcpy(attrib_role,  (const char *)attrs[1]);
    attrs = &attrs[2];
  }

  /* save data for each osm element */
  if(!xmlStrcmp(name, (const xmlChar *)"node")) {
    element_node_active = 1;
    sqlite3_bind_int64 (stmt_insert_nodes, 1, attrib_id);
    sqlite3_bind_double(stmt_insert_nodes, 2, attrib_lat);
    sqlite3_bind_double(stmt_insert_nodes, 3, attrib_lon);
    if( sqlite3_step(stmt_insert_nodes)==SQLITE_DONE ) sqlite3_reset(stmt_insert_nodes);
  }
  else if(!xmlStrcmp(name, (const xmlChar *)"way")) {
    element_way_active = 1;
    node_order = 0;
  }
  else if(!xmlStrcmp(name, (const xmlChar *)"relation")) {
    element_relation_active = 1;
    member_order = 0;
  }
  else if(!xmlStrcmp(name, (const xmlChar *)"tag")) {
    if(element_node_active) {
      sqlite3_bind_int64(stmt_insert_node_tags, 1, attrib_id);
      sqlite3_bind_text (stmt_insert_node_tags, 2, attrib_k, -1, NULL);
      sqlite3_bind_text (stmt_insert_node_tags, 3, attrib_v, -1, NULL);
      if( sqlite3_step(stmt_insert_node_tags)==SQLITE_DONE ) sqlite3_reset(stmt_insert_node_tags);
    }
    if(element_way_active) {
      sqlite3_bind_int64(stmt_insert_way_tags, 1, attrib_id);
      sqlite3_bind_text (stmt_insert_way_tags, 2, attrib_k, -1, NULL);
      sqlite3_bind_text (stmt_insert_way_tags, 3, attrib_v, -1, NULL);
      if( sqlite3_step(stmt_insert_way_tags)==SQLITE_DONE ) sqlite3_reset(stmt_insert_way_tags);
    }
    if(element_relation_active) {
      sqlite3_bind_int64(stmt_insert_relation_tags, 1, attrib_id);
      sqlite3_bind_text (stmt_insert_relation_tags, 2, attrib_k, -1, NULL);
      sqlite3_bind_text (stmt_insert_relation_tags, 3, attrib_v, -1, NULL);
      if( sqlite3_step(stmt_insert_relation_tags)==SQLITE_DONE ) sqlite3_reset(stmt_insert_relation_tags);
    }
  }
  else if(!xmlStrcmp(name, (const xmlChar *)"nd")) {
    if(element_way_active) {
      node_order++;
      sqlite3_bind_int64(stmt_insert_way_nodes, 1, attrib_id);
      sqlite3_bind_int64(stmt_insert_way_nodes, 2, attrib_ref);
      sqlite3_bind_int  (stmt_insert_way_nodes, 3, node_order);
      if( sqlite3_step(stmt_insert_way_nodes)==SQLITE_DONE ) sqlite3_reset(stmt_insert_way_nodes);
    }
  }
  else if(!xmlStrcmp(name, (const xmlChar *)"member")) {
    if(element_relation_active) {
      member_order++;
      sqlite3_bind_int64(stmt_insert_relation_members, 1, attrib_id);
      sqlite3_bind_text (stmt_insert_relation_members, 2, attrib_type, -1, NULL);
      sqlite3_bind_int64(stmt_insert_relation_members, 3, attrib_ref);
      sqlite3_bind_text (stmt_insert_relation_members, 4, attrib_role, -1, NULL);
      sqlite3_bind_int  (stmt_insert_relation_members, 5, member_order);
      if( sqlite3_step(stmt_insert_relation_members)==SQLITE_DONE ) sqlite3_reset(stmt_insert_relation_members);
    }
  }
}

void end_element_callback(void *user_data, const xmlChar *name) {
  if     (!xmlStrcmp(name, (const xmlChar *)"node"))     element_node_active     = 0;
  else if(!xmlStrcmp(name, (const xmlChar *)"way"))      element_way_active      = 0;
  else if(!xmlStrcmp(name, (const xmlChar *)"relation")) element_relation_active = 0;
}

/*
** create tables and prepared insert statements
*/
void create_tables_and_stmt() {
  rc = sqlite3_exec(db,
  "DROP TABLE IF EXISTS nodes;\n"
  "CREATE TABLE nodes (\n"
  " node_id      INTEGER PRIMARY KEY,  -- node ID\n"
  " lon          REAL,                 -- longitude\n"
  " lat          REAL                  -- latitude\n"
  ");\n"

  "DROP TABLE IF EXISTS node_tags;\n"
  "CREATE TABLE node_tags (\n"
  " node_id      INTEGER,              -- node ID\n"
  " key          TEXT,                 -- tag key\n"
  " value        TEXT                  -- tag value\n"
  ");\n"

  "DROP TABLE IF EXISTS way_nodes;\n"
  "CREATE TABLE way_nodes (\n"
  " way_id       INTEGER,              -- way ID\n"
  " node_id      INTEGER,              -- node ID\n"
  " node_order   INTEGER               -- node order\n"
  ");\n"

  "DROP TABLE IF EXISTS way_tags;\n"
  "CREATE TABLE way_tags (\n"
  " way_id       INTEGER,              -- way ID\n"
  " key          TEXT,                 -- tag key\n"
  " value        TEXT                  -- tag value\n"
  ");\n"

  "DROP TABLE IF EXISTS relation_members;\n"
  "CREATE TABLE relation_members (\n"
  " relation_id  INTEGER,              -- relation ID\n"
  " type         TEXT,                 -- type ('node','way','relation')\n"
  " ref          INTEGER,              -- node, way or relation ID\n"
  " role         TEXT,                 -- describes a particular feature\n"
  " member_order INTEGER               -- member order\n"
  ");\n"

  "DROP TABLE IF EXISTS relation_tags;\n"
  "CREATE TABLE relation_tags (\n"
  " relation_id  INTEGER,              -- relation ID\n"
  " key          TEXT,                 -- tag key\n"
  " value        TEXT                  -- tag value\n"
  ");\n",
  NULL, NULL, &zErrMsg);
  if( rc!=SQLITE_OK ){
    fprintf(stderr, "SQL error: %s\n", zErrMsg);
    sqlite3_free(zErrMsg);
  }

  sqlite3_prepare_v2(db,
  "INSERT INTO nodes (node_id,lat,lon) VALUES (?1,?2,?3)",
  -1, &stmt_insert_nodes, NULL);

  sqlite3_prepare_v2(db,
  "INSERT INTO node_tags (node_id,key,value) VALUES (?1,?2,?3)",
  -1, &stmt_insert_node_tags, NULL);

  sqlite3_prepare_v2(db,
  "INSERT INTO way_nodes (way_id,node_id,node_order) VALUES (?1,?2,?3)",
  -1, &stmt_insert_way_nodes, NULL);

  sqlite3_prepare_v2(db,
  "INSERT INTO way_tags (way_id,key,value) VALUES (?1,?2,?3)",
  -1, &stmt_insert_way_tags, NULL);

  sqlite3_prepare_v2(db,
  "INSERT INTO relation_members (relation_id,type,ref,role,member_order) VALUES (?1,?2,?3,?4,?5)",
  -1, &stmt_insert_relation_members, NULL);

  sqlite3_prepare_v2(db,
  "INSERT INTO relation_tags (relation_id,key,value) VALUES (?1,?2,?3)",
  -1, &stmt_insert_relation_tags, NULL);
}

/*
** create indexes
*/
void create_index() {
  printf("creating indexes...\n");
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
  NULL, NULL, &zErrMsg);
  if( rc!=SQLITE_OK ){
    fprintf(stderr, "SQL error: %s\n", zErrMsg);
    sqlite3_free(zErrMsg);
  }
}

/*
** create spatial index
*/
void create_spatial_index() {
  printf("creating spatial index...\n");
  rc = sqlite3_exec(db,
  "DROP TABLE IF EXISTS highway;\n"
  "CREATE VIRTUAL TABLE highway USING rtree( way_id, min_lat, max_lat, min_lon, max_lon );\n"
  "INSERT INTO highway (way_id,min_lat,       max_lat,       min_lon,       max_lon)\n"
  "SELECT      way_tags.way_id,min(nodes.lat),max(nodes.lat),min(nodes.lon),max(nodes.lon)\n"
  "FROM      way_tags\n"
  "LEFT JOIN way_nodes ON way_tags.way_id=way_nodes.way_id\n"
  "LEFT JOIN nodes     ON way_nodes.node_id=nodes.node_id\n"
  "WHERE way_tags.key='highway'\n"
  "GROUP BY way_tags.way_id;\n",
  NULL, NULL, &zErrMsg);
  if( rc!=SQLITE_OK ){
    fprintf(stderr, "SQL error: %s\n", zErrMsg);
    sqlite3_free(zErrMsg);
  }
}

/*
** Main
*/
int main(int argc, char **argv){
  /* check parameter */
  int flag_create_index = 1;
  int flag_create_spatial_index = 0;
  if( argc!=3 && argc!=4 ){
    fprintf(stderr, OSM2SQLITE_HELP_INFO);
    return EXIT_FAILURE;
  }
  if( argc==4 && ( strcmp("-n", argv[3])==0 || strcmp("--no-index", argv[3])==0 ) ){
    flag_create_index = 0;
  }
  if( argc==4 && ( strcmp("-s", argv[3])==0 || strcmp("--spatial-index", argv[3])==0 ) ){
    flag_create_index = 1;
    flag_create_spatial_index = 1;
  }

  /* connect to the database */
  rc = sqlite3_open(argv[2], &db);
  if( rc ){
    fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
    sqlite3_close(db);
    return EXIT_FAILURE;
  }
  sqlite3_exec(db, "PRAGMA journal_mode = OFF", NULL, NULL, NULL);
  sqlite3_exec(db, "PRAGMA page_size = 65536", NULL, NULL, NULL);

  /* SAX handler, initialize all fields to zero */
  xmlSAXHandler sh = { 0 };

  /* register callbacks */
  sh.startElement = start_element_callback;
  sh.endElement = end_element_callback;

  /* create the context */
  xmlParserCtxtPtr ctxt;
  if ((ctxt = xmlCreateFileParserCtxt(argv[1])) == NULL) {
    fprintf(stderr, "Error creating context\n");
    return EXIT_FAILURE;
  }
  /* register sax handler with the context */
  ctxt->sax = &sh;

  /* read the data */
  printf("reading '%s' into '%s'...\n", argv[1], argv[2]);
  sqlite3_exec(db, "BEGIN TRANSACTION", NULL, NULL, NULL);
  create_tables_and_stmt();
  xmlParseDocument(ctxt);   /* parse the xml document */
  sqlite3_exec(db, "COMMIT", NULL, NULL, NULL);
  if (flag_create_index) create_index();
  if (flag_create_spatial_index) create_spatial_index();

  /* finish, check if well-formed document */
  if (!ctxt->wellFormed) printf("XML document isn't well formed\n");
  sqlite3_close(db);

  return EXIT_SUCCESS;
}
