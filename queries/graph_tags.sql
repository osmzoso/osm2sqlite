/*
** Show way tags for edge evaluation
*/
.mode table

.print
.print '*************************************************************'
.print ' Highway'
.print '*************************************************************'
.print 'https://wiki.openstreetmap.org/wiki/Category:Highways'
SELECT key,value,count(*)
FROM way_tags
WHERE key LIKE 'highway%'
GROUP BY key,value
ORDER BY key,value
;
.print
.print '*************************************************************'
.print ' Bicycle'
.print '*************************************************************'
.print 'https://wiki.openstreetmap.org/wiki/Key:cycleway'
.print 'https://wiki.openstreetmap.org/wiki/Key:cycleway:both'
.print 'https://wiki.openstreetmap.org/wiki/Key:cycleway:left'
.print 'https://wiki.openstreetmap.org/wiki/Key:cycleway:right'
.print 'https://wiki.openstreetmap.org/wiki/Key:bicycle'
SELECT key,value,count(*) AS number
FROM way_tags
WHERE key LIKE 'cycleway%' OR key LIKE 'bicycle%'
GROUP BY key,value
ORDER BY number DESC
;
.print
.print '*************************************************************'
.print ' Foot'
.print '*************************************************************'
.print 'https://wiki.openstreetmap.org/wiki/Key:sidewalk'
.print 'https://wiki.openstreetmap.org/wiki/Key:sidewalk:both'
.print 'https://wiki.openstreetmap.org/wiki/Key:sidewalk:left'
.print 'https://wiki.openstreetmap.org/wiki/Key:sidewalk:right'
.print 'https://wiki.openstreetmap.org/wiki/Key:footway'
SELECT key,value,count(*) AS number
FROM way_tags
WHERE key LIKE 'sidewalk%' OR key LIKE 'footway%' OR key LIKE 'foot%'
GROUP BY key,value
ORDER BY number DESC
;
.print
.print '*************************************************************'
.print ' Oneway'
.print '*************************************************************'
.print 'https://wiki.openstreetmap.org/wiki/Key:oneway'
SELECT key,value,count(*) AS number
FROM way_tags
WHERE key LIKE 'oneway%'
GROUP BY key,value
ORDER BY key,value
;
.print
.print '*************************************************************'
.print ' Road surface'
.print '*************************************************************'
SELECT key,value,count(*) AS number
FROM way_tags
WHERE key='surface' OR key='tracktype'
GROUP BY key,value
ORDER BY number DESC
;
