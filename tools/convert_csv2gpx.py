#!/usr/bin/env python
"""
Convert CSV to GPX
"""
import sys


def csv2gpx(csv_filename, gpx_filename):
    """Convert CSV file to GPX file"""
    path_coordinates = []
    with open(csv_filename, 'r', encoding='utf-8') as csv_file:
        for line in csv_file:
            columns = line.split(',')
            try:
                lon = float(columns[0])
                lat = float(columns[1])
                ele = float(columns[2])
            except ValueError:
                continue
            path_coordinates.append((lon, lat, ele))
    with open(gpx_filename, 'w', encoding='utf-8') as gpx_file:
        gpx_file.write(
          '<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n'
          '<gpx version="1.1" xmlns="http://www.topografix.com/GPX/1/1"'
                 f' creator="{sys.argv[0]}">\n'
          '  <metadata></metadata>\n'
          '  <trk>\n'
          '    <name>Track 1</name>\n'
          '    <extensions>\n'
          '    </extensions>\n'
          '    <trkseg>\n')
        for (lon, lat, ele) in path_coordinates:
            gpx_file.write(
             f'      <trkpt lat="{lat}" lon="{lon}">\n'
             f'        <ele>{ele}</ele>\n'
              '      </trkpt>\n')
        gpx_file.write(
          '    </trkseg>\n'
          '  </trk>\n'
          '</gpx>')


def main():
    """entry point"""
    if len(sys.argv) != 3:
        print('Converts a csv file into a gpx file.\n'
              'Usage:\n'
              f'{sys.argv[0]} CSV_FILE GPX_FILE')
        sys.exit(1)
    csv2gpx(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
