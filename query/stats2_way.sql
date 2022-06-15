--
-- Values for important way keys
--
.mode table

.print
.print 'way key=highway:'
.print
SELECT key,value,count(*) AS number
FROM way_tags
WHERE key='highway'
GROUP BY key,value
ORDER BY number DESC
;

.print
.print 'way key=landuse:'
.print
SELECT key,value,count(*) AS number
FROM way_tags
WHERE key='landuse'
GROUP BY key,value
ORDER BY number DESC
;

.print
.print 'way key=leisure:'
.print
SELECT key,value,count(*) AS number
FROM way_tags
WHERE key='leisure'
GROUP BY key,value
ORDER BY number DESC
;

.print
.print 'way key=natural:'
.print
SELECT key,value,count(*) AS number
FROM way_tags
WHERE key='natural'
GROUP BY key,value
ORDER BY number DESC
;

.print
.print 'way key=building:'
.print
SELECT key,value,count(*) AS number
FROM way_tags
WHERE key='building'
GROUP BY key,value
ORDER BY number DESC
;

