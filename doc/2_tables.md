# 2. Tables

The following tables and indexes are created in the database:

Table **nodes**:
```
column       | type                | description
-------------|---------------------|-------------------------------------
node_id      | INTEGER PRIMARY KEY | node ID
lon          | REAL                | longitude
lat          | REAL                | latitude
```

Table **node_tags**:
```
column       | type                | description
-------------|---------------------|-------------------------------------
node_id      | INTEGER             | node ID
key          | TEXT                | tag key
value        | TEXT                | tag value

- INDEX node_tags__node_id ON node_tags (node_id)
- INDEX node_tags__key     ON node_tags (key)
```

Table **way_nodes**:
```
column       | type                | description
-------------|---------------------|-------------------------------------
way_id       | INTEGER             | way ID
node_id      | INTEGER             | node ID
node_order   | INTEGER             | node order

- INDEX way_nodes__way_id  ON way_nodes (way_id, node_order)
- INDEX way_nodes__node_id ON way_nodes (node_id)
```

Table **way_tags**:
```
column       | type                | description
-------------|---------------------|-------------------------------------
way_id       | INTEGER             | way ID
key          | TEXT                | tag key
value        | TEXT                | tag value

- INDEX way_tags__way_id   ON way_tags (way_id)
- INDEX way_tags__key      ON way_tags (key)
```

Table **relation_members**:
```
column       | type                | description
-------------|---------------------|-------------------------------------
relation_id  | INTEGER             | relation ID
type         | TEXT                | type ('node','way','relation')
ref          | INTEGER             | node, way or relation ID
role         | TEXT                | describes a particular feature
member_order | INTEGER             | member order

- INDEX relation_members__relation_id ON relation_members (relation_id, member_order)
- INDEX relation_members__type        ON relation_members (type, ref)
```

Table **relation_tags**:
```
column       | type                | description
-------------|---------------------|-------------------------------------
relation_id  | INTEGER             | relation ID
key          | TEXT                | tag key
value        | TEXT                | tag value

- INDEX relation_tags__relation_id    ON relation_tags (relation_id)
- INDEX relation_tags__key            ON relation_tags (key)
```

