#!/usr/bin/env python3
#-*- coding: UTF-8 -*-


"""
module description
"""

from lib.queue import VlanQueue
from sys import exit
import argparse
import csv

parser = argparse.ArgumentParser(description="""Challenge for VLAN allocating""")
parser.add_argument("vlans", nargs=1, type=str)
parser.add_argument("requests", nargs=1, type=str)
parser.add_argument("output", nargs="?", type=str, default="output.csv")


def read_csv(filename):
    """
    Helper that returns generator where fields are converted to integer
    """
    reader = csv.reader(open(filename))
    next(reader) # skips first line
    int_reader = ([int(field)  for field in row]
        for row in reader)
    return int_reader

def main():
    """
    The main function.
    """
    OPTIONS = vars(parser.parse_args())

    vlans_filename     =  OPTIONS['vlans'][0]
    requests_filename  =  OPTIONS['requests'][0]
    output_filename    =  OPTIONS['output']

    vlans = read_csv(vlans_filename)
    vlan_queue = VlanQueue()
    for vlan in vlans:
        vlan_queue.push_vlan(*vlan)

    requests = read_csv(requests_filename)
    print("Writing to %s" % output_filename)
    with open(output_filename, "w") as file:
        writer = csv.writer(file)
        writer.writerow(("request_id", "device_id", "primary_port", "vlan_id"))
        for request in requests:
            request_id, redundant = request
            for vlan in vlan_queue.get_vlans(redundant):
                device_id, vlan_id, is_primary = vlan
                writer.writerow((request_id, device_id, is_primary, vlan_id))


if __name__ == "__main__":
    exit(main())
