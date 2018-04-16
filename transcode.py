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
    not formatted correctly or entry has no hours or minutes in record."""
    hours, minutes, seconds = [int(x) for x in record[DURATION].split(':')]

    if not hours | minutes:
        raise Exception('No entry to add.')

    return ", ".join([record[DESCRIPTION], "%dh %dm" % (hours, minutes)])


def transcode(filename):
    """Returns ordered dictionary of entries grouped by date, with associated entries formatted as with time string
    entry of '<description>, <number>h <number>m' format. No CSV file will return empty bucket."""
    buckets = collections.OrderedDict()
    try:
        with open(filename, 'r') as csvfile:
            entries = list(csv.reader(csvfile, delimiter=',', quotechar='|'))
            for record in entries:
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