--
-- List of all cell phone antennas
--
-- https://wiki.openstreetmap.org/wiki/DE:Key:communication:mobile_phone
--
.header on
.mode tabs

SELECT t.node_id,t.key,t.value,n.lon,n.lat
FROM node_tags AS t
LEFT JOIN nodes AS n ON t.node_id=n.node_id
WHERE t.key='communication:mobile_phone' AND t.value='yes'
ORDER BY t.node_id
;

