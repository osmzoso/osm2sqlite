# Appendix


## Table size

Output from `sqlite3_analyzer freiburg-regbez-latest.db`:

```
/** Disk-Space Utilization Report For freiburg-regbez-latest.db

Page size in bytes................................ 65536     
...

*** Page counts for all tables and indices separately *************************

WAY_NODES......................................... 5940        17.8% 
NODES............................................. 5727        17.1% 
WAY_NODES__WAY_ID................................. 4339        13.0% 
WAY_NODES__NODE_ID................................ 4181        12.5% 
WAY_TAGS.......................................... 3313         9.9% 
WAY_TAGS__KEY..................................... 1894         5.7% 
WAY_TAGS__WAY_ID.................................. 1340         4.0% 
RTREE_WAY_NODE.................................... 1156         3.5% 
NODE_TAGS......................................... 1103         3.3% 
NODE_TAGS__KEY.................................... 604          1.8% 
RELATION_MEMBERS.................................. 480          1.4% 
RTREE_WAY_ROWID................................... 472          1.4% 
NODE_TAGS__NODE_ID................................ 469          1.4% 
GRAPH............................................. 374          1.1% 
ADDR_HOUSENUMBER.................................. 356          1.1% 
RELATION_MEMBERS__TYPE............................ 320          0.96% 
RTREE_HIGHWAY_NODE................................ 287          0.86% 
RELATION_MEMBERS__RELATION_ID..................... 279          0.84% 
GRAPH__WAY_ID..................................... 180          0.54% 
RELATION_TAGS..................................... 152          0.46% 
RTREE_HIGHWAY_ROWID............................... 111          0.33% 
ADDR_HOUSENUMBER__STREET_ID....................... 102          0.31% 
RELATION_TAGS__KEY................................ 70           0.21% 
RELATION_TAGS__RELATION_ID........................ 51           0.15% 
ADDR_STREET....................................... 50           0.15% 
ADDR_STREET__POSTCODE_CITY_STREET................. 27           0.081% 
RTREE_WAY_PARENT.................................. 14           0.042% 
RTREE_HIGHWAY_PARENT.............................. 4            0.012% 
SQLITE_SCHEMA..................................... 1            0.003% 
```


## SpatiaLite

Test lib SpatiaLite

    sudo dnf install libspatialite.x86_64

