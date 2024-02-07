.print "----------------------------------------------"
.print "Test4: Show floating point difference"
.print "----------------------------------------------"
.mode table
.parameter set $limit 6

ATTACH DATABASE './osm_c.db'  AS db_c;
ATTACH DATABASE './osm_py.db' AS db_py;

--
-- Diff lon
--
CREATE TEMP TABLE diff_lon AS
SELECT DISTINCT node_id FROM
(
  SELECT node_id,lon FROM db_c.nodes
  EXCEPT
  SELECT node_id,lon FROM db_py.nodes
  UNION ALL
  SELECT node_id,lon FROM db_py.nodes
  EXCEPT
  SELECT node_id,lon FROM db_c.nodes
);

SELECT node_id,'db_c' AS db,
 format('%!.50f',lon),
 lower(quote(ieee754_to_blob(lon))) AS binary64_lon
FROM db_c.nodes
WHERE node_id IN (SELECT node_id FROM diff_lon)
UNION ALL
SELECT node_id,'db_py' AS db,
 format('%!.50f',lon),
 lower(quote(ieee754_to_blob(lon))) AS binary64_lon
FROM db_py.nodes
WHERE node_id IN (SELECT node_id FROM diff_lon)
ORDER BY node_id
LIMIT $limit
;

--
-- Diff lat
--
CREATE TEMP TABLE diff_lat AS
SELECT DISTINCT node_id FROM
(
  SELECT node_id,lat FROM db_c.nodes
  EXCEPT
  SELECT node_id,lat FROM db_py.nodes
  UNION ALL
  SELECT node_id,lat FROM db_py.nodes
  EXCEPT
  SELECT node_id,lat FROM db_c.nodes
);

SELECT node_id,'db_c' AS db,
 format('%!.50f',lat),
 lower(quote(ieee754_to_blob(lat))) AS binary64_lat
FROM db_c.nodes
WHERE node_id IN (SELECT node_id FROM diff_lat)
UNION ALL
SELECT node_id,'db_py' AS db,
 format('%!.50f',lat),
 lower(quote(ieee754_to_blob(lat))) AS binary64_lat
FROM db_py.nodes
WHERE node_id IN (SELECT node_id FROM diff_lat)
ORDER BY node_id
LIMIT $limit
;
