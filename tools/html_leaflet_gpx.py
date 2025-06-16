#!/usr/bin/env python
"""
Create map from GPX files
"""
import sys
import xml.etree.ElementTree as ET
import html_leaflet


def map_gpx_html(gpx_filename, html_filename):
    """Create map from GPX files"""
    color_scheme = ['#ff0000', '#0000ff', '#ff00ff', '#ff8000', '#00bfff']
    color_number = 0
    m = html_leaflet.Leaflet(html_filename)
    m.write_html_header('Map GPX Files')
    m.write_html_code('''
    <h1>Map GPX Files</h1>
    <p><div id="mapid" style="width: 100%; height: 700px;"></div></p>
    ''')
    m.write_script_start()
    infotext = '<tr><th>file</th><th>tracks</th><th>trackpoints</th></tr>\n'
    for filename in gpx_filename:
        # read GPX file
        namespace = '{http://www.topografix.com/GPX/1/1}'
        path_coordinates = []
        num_tracks = 0
        tree = ET.parse(filename)
        for trk in tree.findall(namespace + 'trk'):
            num_tracks += 1
            for trkpt in trk.iter(namespace + 'trkpt'):
                lon = float(trkpt.attrib['lon'])
                lat = float(trkpt.attrib['lat'])
                path_coordinates.append((lon, lat))
        #
        num_trackpoints = len(path_coordinates)
        color = color_scheme[color_number]
        color_number = color_number + 1
        if color_number == len(color_scheme):
            color_number = 0
        m.set_property({'color': color})
        m.set_property({'opacity': 0.7})
        m.add_polyline(path_coordinates)
        infotext = infotext + f'<tr><td>{filename}</td><td bgcolor="{color}">{num_tracks}</td><td>{num_trackpoints}</td></tr>\n'
    m.write_script_end()
    m.write_html_code('<table>\n' + infotext + '</table>\n')
    m.write_html_footer()


def main():
    """entry point"""
    if len(sys.argv) < 3:
        print('Creates an HTML file with a map of all paths from the specified GPX files.\n\n'
              'Usage:\n'
              f'{sys.argv[0]} GPX_FILES ... HTML_FILE')
        sys.exit(1)
    gpx_filename = []
    html_filename = ''
    for filename in sys.argv:
        if filename.endswith(('.gpx', '.GPX')):
            gpx_filename.append(filename)
        if filename.endswith(('.html', '.HTML')):
            html_filename = filename
    if gpx_filename == []:
        print('Abort: No GPX file(s) specified')
        sys.exit(1)
    if html_filename == '':
        print('Abort: No HTML file specified')
        sys.exit(1)
    map_gpx_html(gpx_filename, html_filename)


if __name__ == '__main__':
    main()
