#!/usr/bin/env python
"""
Convert GPX to CSV
"""
import sys
import xml.etree.ElementTree as ET


def gpx2csv(gpx_filename, csv_filename):
    """Convert GPX file to CSV file"""
    with open(csv_filename, 'w', encoding='utf-8') as csv_file:
        # Parse the GPX file
        tree = ET.parse(gpx_filename)
        root = tree.getroot()
        # Namespace dictionary
        ns = {'gpx': 'http://www.topografix.com/GPX/1/1'}
        # Find all track points
        track_points = root.findall('.//gpx:trkpt', namespaces=ns)
        # Extract information from each track point
        for track_point in track_points:
            # Extract latitude and longitude
            lat = track_point.get('lat')
            lon = track_point.get('lon')
            # Extract ele and time information if available
            ele_element = track_point.find('gpx:ele', namespaces=ns)
            ele = ele_element.text if ele_element is not None else -1
            time_element = track_point.find('gpx:time', namespaces=ns)
            time = time_element.text if time_element is not None else -1
            # Write information
            csv_file.write(f'{lon},{lat},{ele},{time}\n')


def main():
    """entry point"""
    if len(sys.argv) != 3:
        print('Converts a gpx file into a csv file.\n\n'
              'Usage:\n'
              f'{sys.argv[0]} GPX_FILE CSV_FILE')
        sys.exit(1)
    gpx2csv(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
