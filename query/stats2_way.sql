/*
** Way keys and values
*/
.mode table

.print
.print "Values for ways with key='highway':"
.print
SELECT key,value,count(*) AS number
FROM way_tags
WHERE key='highway'
GROUP BY key,value
ORDER BY number DESC
;

.print
.print 'The most common key/value pairs for ways:'
.print
SELECT key,value,count(*) AS number
FROM way_tags
-- except some keys with individual values:
WHERE key NOT IN (
'name','name:source',
'addr:country','addr:postcode','addr:city','addr:street','addr:housenumber','addr:suburb','addr:housename','addr:place','addr:source',
'source','source:outline','source:geometry','source:addr','source:address',
'FIXME','fixme',
'note','note:name','note:de',
'website','website:de','url','contact:website','phone','contact:phone','operator','opening_hours','description','ref','email','fax',
'wikipedia','wikidata',
'destination',
'is_in'
)
GROUP BY key,value
ORDER BY number DESC
;

