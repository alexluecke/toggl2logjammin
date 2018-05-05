#!/usr/bin/env python3

import csv
import argparse
import collections

"""Indices for toggl csv entries."""
DESCRIPTION = 5
DURATION = 11
START_DATE = 7


def create_entry(record):
    """Returns string for time record in '<description>, <number>h <number>m' format for record. Raises exception when
    entry is not formatted correctly or has no hours or minutes."""
    hours, minutes, seconds = [int(x) for x in record[DURATION].split(':')]

    if not hours | minutes:
        raise Exception('No entry to add.')

    return ", ".join([record[DESCRIPTION], "%dh %dm" % (hours, minutes)])


def transcode(filename):
    """Returns ordered dictionary of entries grouped by date, withe each entry formatted as:
    '<description>, <number>h <number>m'."""
    buckets = collections.OrderedDict()
    try:
        with open(filename, 'r') as csvfile:
            for record in list(csv.reader(csvfile, delimiter=',', quotechar='|')):
                try:
                    entry = create_entry(record)
                    if record[START_DATE] in buckets:
                        buckets[record[START_DATE]] = buckets[record[START_DATE]] + [entry]
                    else:
                        buckets[record[START_DATE]] = [entry]
                except:
                    pass
    except:
        pass

    return buckets


def print_bucket(bucket):
    for key in bucket.keys():
        print(key)
        print("\n".join(bucket[key]))
        print("")


parser = argparse.ArgumentParser()
parser.add_argument('file', type=str, help='file to load')
args = parser.parse_args()

print_bucket(transcode(filename=args.file))
