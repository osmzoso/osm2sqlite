/*
** Reads OpenStreetMap data in XML format into a SQLite database
**
** Uses Module SAX from libxml2 (deprecated)
** http://xmlsoft.org/html/libxml-SAX.html
**
** gcc osm2sqlite.c -lxml2 -o osm2sqlite
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
char   attrib_k[1000];
char   attrib_v[1000];
char   attrib_type[1000];
char   attrib_role[1000];

sqlite3 *db;         /* SQLite Database connection */
char *zErrMsg = 0;   /* SQLite Error message */
int rc;              /* SQLite Return code */

/*
** Callback functions
*/
void start_element_callback(void *user_data, const xmlChar *name, const xmlChar **attrs) {
  printf("  --Beginning of element : %s \n", name);

  /* Alle Attribute des Element auswerten */
  while (NULL != attrs && NULL != attrs[0]) {
    printf("    --attrib: %s = %s\n",attrs[0],attrs[1]);

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

  /* Name des Element auswerten */
  if(!xmlStrcmp(name, (const xmlChar *)"node")) {
    element_node_active = 1;
    printf("INSERT INTO nodes (node_id,lat,lon) VALUES (%I64d,%12.8f,%12.8f);\n", attrib_id, attrib_lat, attrib_lon);
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
      printf("INSERT INTO node_tags (node_id,key,value) VALUES (%I64d,'%s','%s');\n", attrib_id, attrib_k, attrib_v);
    }
    if(element_way_active) {
      printf("INSERT INTO way_tags (way_id,key,value) VALUES (%I64d,'%s','%s');\n", attrib_id, attrib_k, attrib_v);
    }
    if(element_relation_active) {
      printf("INSERT INTO relation_tags (relation_id,key,value) VALUES (%I64d,'%s','%s');\n", attrib_id, attrib_k, attrib_v);
    }
  }
  else if(!xmlStrcmp(name, (const xmlChar *)"nd")) {
    if(element_way_active) {
      node_order++;
      printf("INSERT INTO way_nodes (way_id,node_order,node_id) VALUES (%I64d,%d,%I64d);\n", attrib_id, node_order, attrib_ref);
    }
  }
  else if(!xmlStrcmp(name, (const xmlChar *)"member")) {
    if(element_relation_active) {
      member_order++;
      printf("INSERT INTO relation_members (relation_id,type,ref,role,member_order) VALUES (%I64d,'%s',%I64d,'%s',%d);\n", attrib_id, attrib_type, attrib_ref, attrib_role, member_order);
    }
  }
}

void end_element_callback(void *user_data, const xmlChar *name) {
  printf("  --Ending of element : %s \n", name);

  if     (!xmlStrcmp(name, (const xmlChar *)"node"))     element_node_active     = 0;
  else if(!xmlStrcmp(name, (const xmlChar *)"way"))      element_way_active      = 0;
  else if(!xmlStrcmp(name, (const xmlChar *)"relation")) element_relation_active = 0;
}

/*
**
*/
void create_tables() {
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
}

/*
** Main
*/
int main(int argc, char **argv){
  /* connect to the database */
  rc = sqlite3_open("osm.sqlite3", &db);
  if( rc ){
    fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
    sqlite3_close(db);
    return EXIT_FAILURE;
  }

  /* Initialize all fields to zero */
  xmlSAXHandler sh = { 0 };

  /* register callbacks */
  sh.startElement = start_element_callback;
  sh.endElement = end_element_callback;

  xmlParserCtxtPtr ctxt;

  /* create the context */
  if ((ctxt = xmlCreateFileParserCtxt(argv[1])) == NULL) {
    fprintf(stderr, "Error creating context\n");
    return EXIT_FAILURE;
  }
  /* register sax handler with the context */
  ctxt->sax = &sh;

  /* create the tables in the database */
  create_tables();

  /* parse the xml document */
  xmlParseDocument(ctxt);
  /* well-formed document? */
  if (ctxt->wellFormed) {
    printf("XML Document is well formed\n");
  } else {
    fprintf(stderr, "XML Document isn't well formed\n");
    xmlFreeParserCtxt(ctxt);
    return EXIT_FAILURE;
  }

  /* free the memory */
  xmlFreeParserCtxt(ctxt);

  return EXIT_SUCCESS;
}
