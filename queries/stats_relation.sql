/*
** Relation keys and values
*/
.mode table

.print
.print 'The most common keys for relations:'
.print
SELECT substr(key,1,50),count(*) AS number
FROM relation_tags
GROUP BY key
ORDER BY number DESC
;

/*
.print
.print 'The most common key/value pairs for relations:'
.print
SELECT key,value,count(*) AS number
FROM relation_tags
-- except some keys with individual values:
WHERE key NOT IN (
'name','name:source',
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
*/

SELECT ref,count(*) FROM relation_members GROUP BY ref;

SELECT role,count(*)
FROM relation_members
GROUP BY role
ORDER BY count(*) DESC
LIMIT 20
;

SELECT key,value,count(*)
FROM relation_tags
WHERE key='type'
GROUP BY key,value
ORDER BY count(*) DESC
;
