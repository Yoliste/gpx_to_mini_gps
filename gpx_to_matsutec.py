#!/usr/bin/env python3

import argparse
import xmltodict
import json


def dd_to_dmm(coord):
    # TODO
    return True


def write_last_line(file):
    file.write("$PFEC,GPxfr,CTL,E*59")


def parse_gpx_waypoints(source_file):
    f = open(source_file, "r")
    gpx_dict = xmltodict.parse(f)
    waypoint_list = gpx_dict["gpx"]["wpt"]
    return waypoint_list


class Waypoint:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = dd_to_dmm(abs(lat))
        self.lon = dd_to_dmm(abs(lon))
        if lat >= 0:
            self.north_south = "N"
        else:
            self.north_south = "S"
        if lon >= 0:
            self.east_west = "E"
        else:
            self.east_west = "W"
        self._set_color_shape()

    # cardinals : end with N, S, W or E (depending on directions), blue sideways square
    # lateral buoys : end with either B or T, green or red flag
    # lighthouses : end with P, brown disc
    # special marks : end with SP, yellow flag
    # isolated danger : endd with DG, red square
    # coastal marks (used to "draw" the coast line) : start with TC
    def _set_color_shape(self):
        # coastal line
        if self.name.startswith("TC"):
            self.color = "1"
            self.shape = "@y"
        else:
            # cardinals
            if self.name.endswith(("N", "S", "E", "W")):
                self.color = "6"
                self.shape = "@s"
            elif self.name.endswith("B"):
                self.color = "1"
                self.shape = "@z"
            elif self.name.endswith("T"):
                self.color = "3"
                self.shape = "@z"
            elif self.name.endswith("SP"):
                self.color = "2"
                self.shape = "@z"
            elif self.name.endswith("P"):
                self.color = "4"
                self.shape = "@g"
            elif self.name.endswith("DG"):
                self.color = "1"
                self.shape = "@r"
            else:
                print("unknown waypoint format : {}".format(self.name))
                self.color = None
                self.shape = None

    def write(self, file):
        line = "$PFEC,GPwpl,{lat},{ns},{lon},{ew},{name},{color},{shape},A,,,,".format(lat=self.lat,
                                                                                       ns=self.north_south, lon=self.lon, ew=self.east_west, name=self.name, color=self.color, shape=self.shape)
        file.write(line)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", help="Path to the source GPX file containing the waypoints to import", required=True)
    parser.add_argument("--output", "-o", help="Path to the output text file formatted for Matsutec import", required=True)

    args = parser.parse_args()

    wpt_list = parse_gpx_waypoints(args.input)

    output_file = open(args.output, "w")

    for w in wpt_list:
        if 'name' in w and '@lat' in w and '@lon' in w:
            wpt = Waypoint(w['name'], w['@lat'], w['@lon'])
            wpt.write(output_file)
        else:
            print("gpx format not supported :")
            print(json.dumps(w))

    write_last_line(output_file)


if __name__ == "__main__":
    main()
