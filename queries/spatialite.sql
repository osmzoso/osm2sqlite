/*
** Test SpatiaLite
*/
.mode table

SELECT load_extension('/usr/lib64/mod_spatialite.so');

SELECT spatialite_version();

-- Create table "spatial_ref_sys"
SELECT InitSpatialMetadata(1);

-- WGS84 EPSG:4326 -> Web Mercator EPSG:3857
SELECT AsText( Transform( MakePoint(7.8112387, 48.0160627, 4326), 3857) );

-- Distance Freiburg-Konstanz (ellipsoid, slower but precise)
SELECT Distance( MakePoint(7.8118613,48.015983), MakePoint(9.1808754,47.6716953), 1 );

-- Distance Freiburg-Konstanz (great circle, faster but less precise)
SELECT Distance( MakePoint(7.8118613,48.015983), MakePoint(9.1808754,47.6716953), 0 );

-- Calculate the nearest point on a polyline (linestring) using SpatiaLite
/*
http://www.gaia-gis.it/gaia-sins/spatialite-sql-5.0.1.html
--------------------------------------------------------------------
ShortestLine( geom1 Geometry , geom2 Geometry ) : Curve
ST_ShortestLine( geom1 Geometry , geom2 Geometry ) : Curve
    Returns the shortest line between two geometries.
    NULL is returned for invalid arguments (or if distance is ZERO)
--------------------------------------------------------------------
ClosestPoint( geom1 Geometry , geom2 Geometry ) : Point
ST_ClosestPoint( geom1 Geometry , geom2 Geometry ) : Point
    Returns the Point on geom1 that is closest to geom2.
    NULL is returned for invalid arguments (or if distance is ZERO)
--------------------------------------------------------------------
*/
SELECT
 ST_AsText(
   ST_ShortestLine(
     ST_GeomFromText('LINESTRING(1 1, 2 2, 3 3, 4 4, 5 5)'),
     ST_GeomFromText('POINT(2 3)')
   )
 ) AS shortest_line,
 ST_AsText(
   ST_ClosestPoint(
     ST_GeomFromText('LINESTRING(1 1, 2 2, 3 3, 4 4, 5 5)'),
     ST_GeomFromText('POINT(2 3)')
   )
 ) AS closest_point
;
