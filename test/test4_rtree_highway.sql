--
-- Test R*Tree 'highway'
--
.mode table

--
-- Boundingbox (Reiskirchen im Saarland, Sportplatz)
--
-- min_lon (x1):  7.3280550
-- min_lat (y1): 49.3540703
-- max_lon (x2):  7.3316550
-- max_lat (y2): 49.3576703
--

-- Find all elements of the index (ways) that are contained within the boundingbox:
SELECT way_id
FROM highway
WHERE min_lon>= 7.3280550 AND max_lon<= 7.3316550
 AND  min_lat>=49.3540703 AND max_lat<=49.3576703
;

-- Find all elements of the index (ways) that overlap the boundingbox:
SELECT way_id
FROM highway
WHERE max_lon>= 7.3280550 AND min_lon<= 7.3316550
 AND  max_lat>=49.3540703 AND min_lat<=49.3576703
;

-- Limits of an element of the index:
SELECT min_lon,max_lon,min_lat,max_lat
FROM highway
WHERE way_id=79235038
;

