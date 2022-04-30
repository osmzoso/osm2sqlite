.print "----------------------------------------------"
.print "Test3: Show floating point difference"
.print "----------------------------------------------"
.mode table

--
-- The coordinates are slightly different in the C and the Python version
--

ATTACH DATABASE './osm_c.db'  AS db_c;
ATTACH DATABASE './osm_py.db' AS db_py;

CREATE TEMP TABLE list_node_id AS
SELECT DISTINCT node_id FROM
(
  SELECT node_id,lon,lat FROM db_c.nodes
  EXCEPT
  SELECT node_id,lon,lat FROM db_py.nodes
  UNION ALL
  SELECT node_id,lon,lat FROM db_py.nodes
  EXCEPT
  SELECT node_id,lon,lat FROM db_c.nodes
)
;

SELECT node_id,'db_c' AS db,
 format("%!.50f",lon),format("%!.50f",lat),
 lower(quote(ieee754_to_blob(lon))) AS binary64_lon,
 lower(quote(ieee754_to_blob(lat))) AS binary64_lat
FROM db_c.nodes
WHERE node_id IN (SELECT node_id FROM list_node_id)

UNION ALL

SELECT node_id,'db_py' AS db,
 format("%!.50f",lon),format("%!.50f",lat),
 lower(quote(ieee754_to_blob(lon))) AS binary64_lon,
 lower(quote(ieee754_to_blob(lat))) AS binary64_lat
FROM db_py.nodes
WHERE node_id IN (SELECT node_id FROM list_node_id)

ORDER BY node_id
;

