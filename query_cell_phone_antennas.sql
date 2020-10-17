--
-- List cell phone antennas
-- (all nodes with tag key='communication:mobile_phone')
--
.header on
.mode box

SELECT t.node_id,t.key,t.value,n.lon,n.lat
FROM node_tags AS t
LEFT JOIN nodes AS n ON t.node_id=n.node_id
WHERE t.key='communication:mobile_phone'
ORDER BY t.node_id
;

