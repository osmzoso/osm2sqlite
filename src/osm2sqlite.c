/*
** osm2sqlite - Reads OpenStreetMap XML data into a SQLite database
**
** Copyright (C) 2022-2024 Herbert Gläser
**
*/
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <inttypes.h>
#include <sqlite3.h>
#include <libxml/tree.h>
#include <libxml/parser.h>
#include <libxml/parserInternals.h>

#define NODE 1
#define WAY 2
#define RELATION 3

void show_help() {
  printf(
  "osm2sqlite 0.9.3\n"
  "\n"
  "Reads OpenStreetMap XML data into a SQLite database.\n"
  "\n"
  "Usage:\nosm2sqlite SQLITE_DATABASE OSM_XML_FILE [OPTION]...\n"
  "\n"
  "Options:\n"
  "  rtree         Add R*Tree indexes\n"
  "  addr          Add address tables\n"
  "  graph         Add graph table\n"
  "  noindex       Do not create indexes (not recommended)\n"
  "\n"
  "When OSM_XML_FILE is -, read standard input.\n"
  );
  printf("\n(SQLite %s is used)\n\n", sqlite3_libversion());
}

/*
** Public variables
*/
sqlite3 *db;         /* SQLite Database connection */
int rc;              /* SQLite Result code */
sqlite3_stmt *stmt_insert_nodes, *stmt_insert_node_tags, *stmt_insert_way_nodes,
             *stmt_insert_way_tags, *stmt_insert_relation_members, *stmt_insert_relation_tags;

/*
** Abort if a database error has occurred
*/
void abort_db_error(int rc) {
  fprintf(stderr, "abort osm2sqlite - (%i) %s - %s\n", rc, sqlite3_errstr(rc), sqlite3_errmsg(db));
  sqlite3_close(db);
  exit(EXIT_FAILURE);
}

/*
** Callback functions
*/
void start_element_callback(void *user_data, const xmlChar *name, const xmlChar **attrs) {
  static int element_active = 0;   /* marker which element is active */
  static int node_order = 0;
  static int member_order = 0;
  static int64_t attrib_id = 0;
  static int64_t attrib_ref = 0;
  static double attrib_lat = 0;
  static double attrib_lon = 0;
  static char attrib_k[2000];      /* There is a 255 character limit for         */
  static char attrib_v[2000];      /* key and value length in OSM.               */
  static char attrib_type[2000];   /* Therefore 2000 characters should be enough */
  static char attrib_role[2000];   /* to avoid a buffer overflow in strcpy().    */

  /* check all attributes of the element */
  while( attrs!=NULL && attrs[0]!=NULL ) {
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
  if( !xmlStrcmp(name, (const xmlChar *) "node") ) {
    element_active = NODE;
    sqlite3_bind_int64 (stmt_insert_nodes, 1, attrib_id);
    sqlite3_bind_double(stmt_insert_nodes, 2, attrib_lat);
    sqlite3_bind_double(stmt_insert_nodes, 3, attrib_lon);
    rc = sqlite3_step(stmt_insert_nodes);
    if( rc==SQLITE_DONE ) {
      sqlite3_reset(stmt_insert_nodes);
    } else {
      abort_db_error(rc);
    }
  } else if( !xmlStrcmp(name, (const xmlChar *) "way") ) {
    element_active = WAY;
    node_order = 0;
  } else if( !xmlStrcmp(name, (const xmlChar *) "relation") ) {
    element_active = RELATION;
    member_order = 0;
  } else if( !xmlStrcmp(name, (const xmlChar *) "tag") ) {
    if( element_active == NODE ) {
      sqlite3_bind_int64(stmt_insert_node_tags, 1, attrib_id);
      sqlite3_bind_text (stmt_insert_node_tags, 2, attrib_k, -1, NULL);
      sqlite3_bind_text (stmt_insert_node_tags, 3, attrib_v, -1, NULL);
      rc = sqlite3_step(stmt_insert_node_tags);
      if( rc==SQLITE_DONE ) {
        sqlite3_reset(stmt_insert_node_tags);
      } else {
        abort_db_error(rc);
      }
    }
    if( element_active == WAY ) {
      sqlite3_bind_int64(stmt_insert_way_tags, 1, attrib_id);
      sqlite3_bind_text (stmt_insert_way_tags, 2, attrib_k, -1, NULL);
      sqlite3_bind_text (stmt_insert_way_tags, 3, attrib_v, -1, NULL);
      rc = sqlite3_step(stmt_insert_way_tags);
      if( rc==SQLITE_DONE ) {
        sqlite3_reset(stmt_insert_way_tags);
      } else {
        abort_db_error(rc);
      }
    }
    if( element_active == RELATION ) {
      sqlite3_bind_int64(stmt_insert_relation_tags, 1, attrib_id);
      sqlite3_bind_text (stmt_insert_relation_tags, 2, attrib_k, -1, NULL);
      sqlite3_bind_text (stmt_insert_relation_tags, 3, attrib_v, -1, NULL);
      rc = sqlite3_step(stmt_insert_relation_tags);
      if( rc==SQLITE_DONE ) {
        sqlite3_reset(stmt_insert_relation_tags);
      } else {
        abort_db_error(rc);
      }
    }
  } else if( !xmlStrcmp(name, (const xmlChar *) "nd") ) {
    if( element_active == WAY ) {
      node_order++;
      sqlite3_bind_int64(stmt_insert_way_nodes, 1, attrib_id);
      sqlite3_bind_int64(stmt_insert_way_nodes, 2, attrib_ref);
      sqlite3_bind_int  (stmt_insert_way_nodes, 3, node_order);
      rc = sqlite3_step(stmt_insert_way_nodes);
      if( rc==SQLITE_DONE ) {
        sqlite3_reset(stmt_insert_way_nodes);
      } else {
        abort_db_error(rc);
      }
    }
  } else if( !xmlStrcmp(name, (const xmlChar *) "member") ) {
    if( element_active == RELATION ) {
      member_order++;
      sqlite3_bind_int64(stmt_insert_relation_members, 1, attrib_id);
      sqlite3_bind_text (stmt_insert_relation_members, 2, attrib_type, -1, NULL);
      sqlite3_bind_int64(stmt_insert_relation_members, 3, attrib_ref);
      sqlite3_bind_text (stmt_insert_relation_members, 4, attrib_role, -1, NULL);
      sqlite3_bind_int  (stmt_insert_relation_members, 5, member_order);
      rc = sqlite3_step(stmt_insert_relation_members);
      if( rc==SQLITE_DONE ) {
        sqlite3_reset(stmt_insert_relation_members);
      } else {
        abort_db_error(rc);
      }
    }
  }
}

/*
** create tables, indexes and prepared insert statements
*/
void add_tables() {
  rc = sqlite3_exec(
         db,
         " CREATE TABLE nodes (\n"
         "  node_id      INTEGER PRIMARY KEY,  -- node ID\n"
         "  lon          REAL,                 -- longitude\n"
         "  lat          REAL                  -- latitude\n"
         " );\n"

         " CREATE TABLE node_tags (\n"
         "  node_id      INTEGER,              -- node ID\n"
         "  key          TEXT,                 -- tag key\n"
         "  value        TEXT                  -- tag value\n"
         " );\n"

         " CREATE TABLE way_nodes (\n"
         "  way_id       INTEGER,              -- way ID\n"
         "  node_id      INTEGER,              -- node ID\n"
         "  node_order   INTEGER               -- node order\n"
         " );\n"

         " CREATE TABLE way_tags (\n"
         "  way_id       INTEGER,              -- way ID\n"
         "  key          TEXT,                 -- tag key\n"
         "  value        TEXT                  -- tag value\n"
         " );\n"

         " CREATE TABLE relation_members (\n"
         "  relation_id  INTEGER,              -- relation ID\n"
         "  ref          TEXT,                 -- reference ('node','way','relation')\n"
         "  ref_id       INTEGER,              -- node, way or relation ID\n"
         "  role         TEXT,                 -- describes a particular feature\n"
         "  member_order INTEGER               -- member order\n"
         " );\n"

         " CREATE TABLE relation_tags (\n"
         "  relation_id  INTEGER,              -- relation ID\n"
         "  key          TEXT,                 -- tag key\n"
         "  value        TEXT                  -- tag value\n"
         " );\n",
         NULL, NULL, NULL);
  if( rc!=SQLITE_OK ) abort_db_error(rc);
}

void create_prep_stmt() {
  rc = sqlite3_prepare_v2(
         db,
         "INSERT INTO nodes (node_id,lat,lon) VALUES (?1,?2,?3)",
         -1, &stmt_insert_nodes, NULL);
  if( rc!=SQLITE_OK ) abort_db_error(rc);
  rc = sqlite3_prepare_v2(
         db,
         "INSERT INTO node_tags (node_id,key,value) VALUES (?1,?2,?3)",
         -1, &stmt_insert_node_tags, NULL);
  if( rc!=SQLITE_OK ) abort_db_error(rc);
  rc = sqlite3_prepare_v2(
         db,
         "INSERT INTO way_nodes (way_id,node_id,node_order) VALUES (?1,?2,?3)",
         -1, &stmt_insert_way_nodes, NULL);
  if( rc!=SQLITE_OK ) abort_db_error(rc);
  rc = sqlite3_prepare_v2(
         db,
         "INSERT INTO way_tags (way_id,key,value) VALUES (?1,?2,?3)",
         -1, &stmt_insert_way_tags, NULL);
  if( rc!=SQLITE_OK ) abort_db_error(rc);
  rc = sqlite3_prepare_v2(
         db,
         "INSERT INTO relation_members (relation_id,ref,ref_id,role,member_order) VALUES (?1,?2,?3,?4,?5)",
         -1, &stmt_insert_relation_members, NULL);
  if( rc!=SQLITE_OK ) abort_db_error(rc);
  rc = sqlite3_prepare_v2(
         db,
         "INSERT INTO relation_tags (relation_id,key,value) VALUES (?1,?2,?3)",
         -1, &stmt_insert_relation_tags, NULL);
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

void add_index() {
  rc = sqlite3_exec(
         db,
         " CREATE INDEX node_tags__node_id            ON node_tags (node_id);"
         " CREATE INDEX node_tags__key                ON node_tags (key);"
         " CREATE INDEX way_tags__way_id              ON way_tags (way_id);"
         " CREATE INDEX way_tags__key                 ON way_tags (key);"
         " CREATE INDEX way_nodes__way_id             ON way_nodes (way_id, node_order);"
         " CREATE INDEX way_nodes__node_id            ON way_nodes (node_id);"
         " CREATE INDEX relation_members__relation_id ON relation_members (relation_id, member_order);"
         " CREATE INDEX relation_members__ref_id      ON relation_members (ref_id);"
         " CREATE INDEX relation_tags__relation_id    ON relation_tags (relation_id);"
         " CREATE INDEX relation_tags__key            ON relation_tags (key);",
         NULL, NULL, NULL);
  if( rc!=SQLITE_OK ) abort_db_error(rc);
}

void add_rtree() {
  rc = sqlite3_exec(
         db,
         /*
         ** Create R*Tree index 'rtree_way'
         */
         " CREATE VIRTUAL TABLE rtree_way USING rtree(way_id, min_lat, max_lat, min_lon, max_lon);"
         " INSERT INTO rtree_way (way_id, min_lat, max_lat, min_lon, max_lon)"
         " SELECT way_nodes.way_id,min(nodes.lat),max(nodes.lat),min(nodes.lon),max(nodes.lon)"
         " FROM way_nodes"
         " LEFT JOIN nodes ON way_nodes.node_id=nodes.node_id"
         " GROUP BY way_nodes.way_id;"
         " CREATE VIRTUAL TABLE rtree_node USING rtree(node_id, min_lat, max_lat, min_lon, max_lon);"
         " INSERT INTO rtree_node (node_id, min_lat, max_lat, min_lon, max_lon)"
         " SELECT DISTINCT nodes.node_id,nodes.lat,nodes.lat,nodes.lon,nodes.lon"
         " FROM nodes"
         " LEFT JOIN node_tags ON nodes.node_id=node_tags.node_id"
         " WHERE node_tags.node_id IS NOT NULL;",
         NULL, NULL, NULL);
  if( rc!=SQLITE_OK ) abort_db_error(rc);
}

void add_addr() {
  rc = sqlite3_exec(
    db,
    " BEGIN TRANSACTION;"
    " /*"
    " ** Create address tables"
    " */"
    " CREATE TABLE addr_street (\n"
    "  street_id   INTEGER PRIMARY KEY, -- street ID\n"
    "  postcode    TEXT,                -- postcode\n"
    "  city        TEXT,                -- city name\n"
    "  street      TEXT,                -- street name\n"
    "  min_lon     REAL,                -- boundingbox street min longitude\n"
    "  min_lat     REAL,                -- boundingbox street min latitude\n"
    "  max_lon     REAL,                -- boundingbox street max longitude\n"
    "  max_lat     REAL                 -- boundingbox street max latitude\n"
    " );\n"
    " CREATE TABLE addr_housenumber (\n"
    "  housenumber_id INTEGER PRIMARY KEY, -- housenumber ID\n"
    "  street_id      INTEGER,             -- street ID\n"
    "  housenumber    TEXT,                -- housenumber\n"
    "  lon            REAL,                -- longitude\n"
    "  lat            REAL,                -- latitude\n"
    "  way_id         INTEGER,             -- way ID\n"
    "  node_id        INTEGER              -- node ID\n"
    " );\n"
    " CREATE VIEW addr_view AS"
    " SELECT s.street_id,s.postcode,s.city,s.street,h.housenumber,h.lon,h.lat,h.way_id,h.node_id"
    " FROM addr_street AS s"
    " LEFT JOIN addr_housenumber AS h ON s.street_id=h.street_id;"
    " /*"
    " ** 1. Determine address data from way tags"
    " */"
    " CREATE TEMP TABLE tmp_addr_way (\n"
    "  way_id      INTEGER PRIMARY KEY,"
    "  postcode    TEXT,"
    "  city        TEXT,"
    "  street      TEXT,"
    "  housenumber TEXT"
    " );\n"
    " INSERT INTO tmp_addr_way"
    "  SELECT way_id,value AS postcode,'','',''"
    "  FROM way_tags WHERE key='addr:postcode'"
    "  ON CONFLICT(way_id) DO UPDATE SET postcode=excluded.postcode;"
    " INSERT INTO tmp_addr_way"
    "  SELECT way_id,'',value AS city,'',''"
    "  FROM way_tags WHERE key='addr:city'"
    "  ON CONFLICT(way_id) DO UPDATE SET city=excluded.city;"
    " INSERT INTO tmp_addr_way"
    "  SELECT way_id,'','',value AS street,''"
    "  FROM way_tags WHERE key='addr:street'"
    "  ON CONFLICT(way_id) DO UPDATE SET street=excluded.street;"
    " INSERT INTO tmp_addr_way"
    "  SELECT way_id,'','','',value AS housenumber"
    "  FROM way_tags WHERE key='addr:housenumber'"
    "  ON CONFLICT(way_id) DO UPDATE SET housenumber=excluded.housenumber;"
    " /*"
    " ** 2. Calculate coordinates of address data from way tags"
    " */"
    " CREATE TEMP TABLE tmp_addr_way_coordinates AS"
    " SELECT way.way_id AS way_id,round(avg(n.lon),7) AS lon,round(avg(n.lat),7) AS lat"
    " FROM tmp_addr_way AS way"
    " LEFT JOIN way_nodes AS wn ON way.way_id=wn.way_id"
    " LEFT JOIN nodes     AS n  ON wn.node_id=n.node_id"
    " GROUP BY way.way_id;"
    " CREATE INDEX tmp_addr_way_coordinates_way_id ON tmp_addr_way_coordinates (way_id);\n"
    " /*"
    " ** 3. Determine address data from node tags"
    " */"
    " CREATE TEMP TABLE tmp_addr_node (\n"
    "  node_id     INTEGER PRIMARY KEY,"
    "  postcode    TEXT,"
    "  city        TEXT,"
    "  street      TEXT,"
    "  housenumber TEXT"
    " );\n"
    " INSERT INTO tmp_addr_node"
    "  SELECT node_id,value AS postcode,'','',''"
    "  FROM node_tags WHERE key='addr:postcode'"
    "  ON CONFLICT(node_id) DO UPDATE SET postcode=excluded.postcode;"
    " INSERT INTO tmp_addr_node"
    "  SELECT node_id,'',value AS city,'',''"
    "  FROM node_tags WHERE key='addr:city'"
    "  ON CONFLICT(node_id) DO UPDATE SET city=excluded.city;"
    " INSERT INTO tmp_addr_node"
    "  SELECT node_id,'','',value AS street,''"
    "  FROM node_tags WHERE key='addr:street'"
    "  ON CONFLICT(node_id) DO UPDATE SET street=excluded.street;"
    " INSERT INTO tmp_addr_node"
    "  SELECT node_id,'','','',value AS housenumber"
    "  FROM node_tags WHERE key='addr:housenumber'"
    "  ON CONFLICT(node_id) DO UPDATE SET housenumber=excluded.housenumber;"
    " /*"
    " ** 4. Create temporary overall table with all addresses"
    " */"
    " CREATE TEMP TABLE tmp_addr (\n"
    "  addr_id     INTEGER PRIMARY KEY,"
    "  way_id      INTEGER,"
    "  node_id     INTEGER,"
    "  postcode    TEXT,"
    "  city        TEXT,"
    "  street      TEXT,"
    "  housenumber TEXT,"
    "  lon         REAL,"
    "  lat         REAL"
    " );\n"
    " INSERT INTO tmp_addr (way_id,node_id,postcode,city,street,housenumber,lon,lat)"
    "  SELECT w.way_id,-1 AS node_id,w.postcode,w.city,w.street,w.housenumber,c.lon,c.lat"
    "  FROM tmp_addr_way AS w"
    "  LEFT JOIN tmp_addr_way_coordinates AS c ON w.way_id=c.way_id"
    " UNION ALL"
    "  SELECT -1 AS way_id,n.node_id,n.postcode,n.city,n.street,n.housenumber,c.lon,c.lat"
    "  FROM tmp_addr_node AS n"
    "  LEFT JOIN nodes AS c ON n.node_id=c.node_id"
    " ORDER BY postcode,city,street,housenumber;"
    " /*"
    " ** 5. Fill tables 'addr_street' and 'addr_housenumber'"
    " */"
    " INSERT INTO addr_street (postcode,city,street,min_lon,min_lat,max_lon,max_lat)"
    "  SELECT postcode,city,street,min(lon),min(lat),max(lon),max(lat)"
    "  FROM tmp_addr"
    "  GROUP BY postcode,city,street;"
    " CREATE INDEX addr_street__postcode_city_street ON addr_street (postcode,city,street);\n"
    " INSERT INTO addr_housenumber (street_id,housenumber,lon,lat,way_id,node_id)"
    "  SELECT s.street_id,a.housenumber,a.lon,a.lat,a.way_id,a.node_id"
    "  FROM tmp_addr AS a"
    "  LEFT JOIN addr_street AS s ON a.postcode=s.postcode AND a.city=s.city AND a.street=s.street;"
    " CREATE INDEX addr_housenumber__street_id ON addr_housenumber (street_id);\n"
    " /*"
    " ** 6. Delete temporary tables"
    " */"
    " DROP TABLE tmp_addr_way;"
    " DROP TABLE tmp_addr_way_coordinates;"
    " DROP TABLE tmp_addr_node;"
    " DROP TABLE tmp_addr;"
    " COMMIT TRANSACTION;",
    NULL, NULL, NULL);
  if( rc!=SQLITE_OK ) abort_db_error(rc);
}

/* Calculates great circle distance between two coordinates in degrees */
double distance(double lon1, double lat1, double lon2, double lat2) {
  /* Avoid a acos error if the two points are identical */
  if( lon1 == lon2 && lat1 == lat2 ) return 0;
  lon1 = lon1 * (M_PI / 180.0);   /* Conversion degree to radians */
  lat1 = lat1 * (M_PI / 180.0);
  lon2 = lon2 * (M_PI / 180.0);
  lat2 = lat2 * (M_PI / 180.0);
  /* Use earth radius Europe 6371 km (alternatively radius equator 6378 km) */
  double dist = acos(sin(lat1) * sin(lat2) + cos(lat1) * cos(lat2) * cos(lon2 - lon1)) * 6371000;
  return dist;    /* distance in meters */
}

void add_graph() {
  sqlite3_exec(db, "BEGIN TRANSACTION", NULL, NULL, NULL);
  rc = sqlite3_exec(
         db,
         " CREATE TABLE graph (\n"
         "  edge_id       INTEGER PRIMARY KEY,  -- edge ID\n"
         "  start_node_id INTEGER,              -- edge start node ID\n"
         "  end_node_id   INTEGER,              -- edge end node ID\n"
         "  dist          INTEGER,              -- distance in meters\n"
         "  way_id        INTEGER,              -- way ID\n"
         "  permit        INTEGER DEFAULT 15    -- bit field access\n"
         " )\n",
         NULL, NULL, NULL);
  if( rc!=SQLITE_OK ) abort_db_error(rc);
  /* Create a table with all nodes that are crossing points */
  rc = sqlite3_exec(
         db,
         " CREATE TEMP TABLE highway_nodes_crossing"
         " ("
         "  node_id INTEGER PRIMARY KEY"
         " )",
         NULL, NULL, NULL);
  if( rc!=SQLITE_OK ) abort_db_error(rc);
  rc = sqlite3_exec(
         db,
         " INSERT INTO highway_nodes_crossing"
         " SELECT node_id FROM"
         " ("
         "  SELECT wn.node_id"
         "  FROM way_tags AS wt"
         "  LEFT JOIN way_nodes AS wn ON wt.way_id=wn.way_id"
         "  WHERE wt.key='highway'"
         " )"
         " GROUP BY node_id HAVING count(*)>1",
         NULL, NULL, NULL);
  if( rc!=SQLITE_OK ) abort_db_error(rc);
  /* */
  double prev_lon = 0;
  double prev_lat = 0;
  int64_t prev_way_id = -1;
  int64_t prev_node_id = -1;
  int edge_active = 0;
  int64_t start_node_id = -1;
  double dist = 0;

  sqlite3_stmt *stmt_insert_graph;
  rc = sqlite3_prepare_v2(
         db,
         "INSERT INTO graph (start_node_id,end_node_id,dist,way_id) VALUES (?1,?2,?3,?4)",
         -1, &stmt_insert_graph, NULL);
  if( rc!=SQLITE_OK ) abort_db_error(rc);

  sqlite3_stmt *stmt = NULL;
  rc = sqlite3_prepare_v2(
         db,
         " SELECT"
         "  wn.way_id,wn.node_id,"
         "  ifnull(hnc.node_id,-1) AS node_id_crossing,"
         "  n.lon,n.lat"
         " FROM way_tags AS wt"
         " LEFT JOIN way_nodes AS wn ON wt.way_id=wn.way_id"
         " LEFT JOIN highway_nodes_crossing AS hnc ON wn.node_id=hnc.node_id"
         " LEFT JOIN nodes AS n ON wn.node_id=n.node_id"
         " WHERE wt.key='highway'"
         " ORDER BY wn.way_id,wn.node_order",
         -1, &stmt, NULL);
  if( rc!=SQLITE_OK ) abort_db_error(rc);

  int64_t way_id;
  int64_t node_id;
  int64_t node_id_crossing;
  double lon;
  double lat;
  rc = sqlite3_step(stmt);
  while( rc!=SQLITE_DONE && rc!=SQLITE_OK ) {
    way_id = sqlite3_column_int64(stmt, 0);
    node_id = sqlite3_column_int64(stmt, 1);
    node_id_crossing = sqlite3_column_int64(stmt, 2);
    lon = sqlite3_column_double(stmt, 3);
    lat = sqlite3_column_double(stmt, 4);
    /* If a new way is active but there are still remnants of the previous way, create a new edge. */
    if( way_id != prev_way_id && edge_active ) {
      sqlite3_bind_int64(stmt_insert_graph, 1, start_node_id);
      sqlite3_bind_int64(stmt_insert_graph, 2, prev_node_id);
      sqlite3_bind_int  (stmt_insert_graph, 3, lroundf(dist));
      sqlite3_bind_int64(stmt_insert_graph, 4, prev_way_id);
      rc = sqlite3_step(stmt_insert_graph);
      if( rc==SQLITE_DONE ) {
        sqlite3_reset(stmt_insert_graph);
      } else {
        abort_db_error(rc);
      }
      edge_active = 0;
    }
    dist = dist + distance(prev_lon, prev_lat, lon, lat);
    edge_active = 1;
    /* If way_id changes or crossing node is present then an edge begins or ends. */
    if( way_id != prev_way_id ) {
      start_node_id = node_id;
      dist = 0;
    }
    if( node_id_crossing > -1 && way_id == prev_way_id ) {
      if( start_node_id != -1 ) {
        sqlite3_bind_int64(stmt_insert_graph, 1, start_node_id);
        sqlite3_bind_int64(stmt_insert_graph, 2, node_id);
        sqlite3_bind_int  (stmt_insert_graph, 3, lroundf(dist));
        sqlite3_bind_int64(stmt_insert_graph, 4, way_id);
        rc = sqlite3_step(stmt_insert_graph);
        if( rc==SQLITE_DONE ) {
          sqlite3_reset(stmt_insert_graph);
        } else {
          abort_db_error(rc);
        }
        edge_active = 0;
      }
      start_node_id = node_id;
      dist = 0;
    }
    prev_lon = lon;
    prev_lat = lat;
    prev_way_id = way_id;
    prev_node_id = node_id;

    rc = sqlite3_step(stmt);
  }
  if( edge_active ) {
    sqlite3_bind_int64(stmt_insert_graph, 1, start_node_id);
    sqlite3_bind_int64(stmt_insert_graph, 2, node_id);
    sqlite3_bind_int  (stmt_insert_graph, 3, lroundf(dist));
    sqlite3_bind_int64(stmt_insert_graph, 4, way_id);
    rc = sqlite3_step(stmt_insert_graph);
    if( rc==SQLITE_DONE ) {
      sqlite3_reset(stmt_insert_graph);
    } else {
      abort_db_error(rc);
    }
  }
  rc = sqlite3_exec(db, "CREATE INDEX graph__way_id ON graph (way_id)", NULL, NULL, NULL);
  if( rc!=SQLITE_OK ) abort_db_error(rc);
  sqlite3_exec(db, "COMMIT", NULL, NULL, NULL);
}

/*
** Main
*/
int main(int argc, char **argv) {
  if( argc<3 ) {
    show_help();
    return EXIT_FAILURE;
  }

  /* check options */
  int opt_index = 1;
  int opt_rtree = 0;
  int opt_addr = 0;
  int opt_graph = 0;
  int i;
  if( argc>3 ) {
    for(i=3; i < argc; i++) {
      if( strcmp("noindex", argv[i])==0 ) {
        opt_index = 0;
      } else if( strcmp("rtree", argv[i])==0 ) {
        opt_rtree = 1;
      } else if( strcmp("addr", argv[i])==0 ) {
        opt_addr = 1;
      } else if( strcmp("graph", argv[i])==0 ) {
        opt_graph = 1;
      } else {
        fprintf(stderr, "abort - option '%s' unknown\n", argv[i]);
        return EXIT_FAILURE;
      }
    }
  }

  /* Open database connection and create the tables */
  rc = sqlite3_open(argv[1], &db);
  if( rc!=SQLITE_OK ) abort_db_error(rc);
  rc = sqlite3_exec(db, " PRAGMA journal_mode = OFF;"
                        " PRAGMA page_size = 65536;"
                        " BEGIN TRANSACTION;", NULL, NULL, NULL);
  if( rc!=SQLITE_OK ) abort_db_error(rc);
  add_tables();
  create_prep_stmt();

  /* Read XML data with SAX parser */
  xmlSAXHandler sh = { 0 };                 /* initialize all fields to zero   */
  sh.startElement = start_element_callback; /* register callback functions     */
  xmlParserCtxtPtr ctxt;                    /* create context                  */
  if( (ctxt = xmlCreateFileParserCtxt(argv[2]))==NULL ) {
    fprintf(stderr, "SAX Error : creating context failed\n");
    return EXIT_FAILURE;
  }
  xmlCtxtUseOptions(ctxt, XML_PARSE_NOENT); /* substitute entities, e.g. &amp; */
  ctxt->sax = &sh;                          /* register sax handler in context */
  xmlParseDocument(ctxt);                   /* read and parse the XML document */
  if( !ctxt->wellFormed ) fprintf(stderr, "XML document isn't well formed\n");

  /* Add additional data */
  if( opt_index ) add_index();
  if( opt_rtree ) add_rtree();
  sqlite3_exec(db, "COMMIT", NULL, NULL, NULL);
  if( opt_addr ) add_addr();
  if( opt_graph ) add_graph();

  /* Close database connection */
  destroy_prep_stmt();
  sqlite3_close(db);

  return EXIT_SUCCESS;
}
