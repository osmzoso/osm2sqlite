#!/usr/bin/env python
"""
Create map from CSV files
"""
import sys
import html_leaflet


def map_csv_html(csv_filename, html_filename):
    """Create map from CSV files"""
    path_coordinates = []
    infotext = csv_filename + '\n'
    #
    f = open(csv_filename, 'r', encoding='utf-8')
    for line in f:
        if line.startswith("# subgraph_boundingbox:"):
            bbox = line.split()
        if line.startswith("#"):
            infotext = infotext + line
            continue
        lonlat = line.split(',')
        try:
            lon = float(lonlat[0])
            lat = float(lonlat[1])
        except ValueError:
            continue
        path_coordinates.append((lon, lat))
    f.close()
    #
    m = html_leaflet.Leaflet(html_filename)
    m.write_html_header('Map Routing')
    m.write_html_code(f'''
    <h1>Map Routing Path</h1>
    <pre>{infotext}</pre>
    <p><div id="mapid" style="width: 100%; height: 700px;"></div></p>
    ''')
    m.write_script_start()
    m.set_property(
      {'color': '#ff0000', 'opacity': 0.6, 'weight': 6, 'dasharray': '',
       'fillcolor': '#00ffff', 'fillopacity': 0.7}
    )
    m.add_polyline(path_coordinates)
    if 'bbox' in locals():
        m.set_property(
          {'color': '#005588', 'opacity': 1.0, 'weight': 2, 'dasharray': '5 5',
           'fillcolor': 'none', 'fillopacity': 1.0}
        )
        m.add_rectangle(float(bbox[2]), float(bbox[3]), float(bbox[4]), float(bbox[5]), '')
    m.write_script_end()
    m.write_html_footer()


def main():
    """entry point"""
    if len(sys.argv) != 3:
        print('Creates an HTML file with a map from a CSV file containing waypoints (lon,lat).\n\n'
              'Usage:\n'
              f'{sys.argv[0]} CSV_FILE HTML_FILE')
        sys.exit(1)
    csv_filename = sys.argv[1]
    html_filename = sys.argv[2]
    map_csv_html(csv_filename, html_filename)


if __name__ == '__main__':
    main()
