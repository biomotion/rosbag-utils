#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# Copyright 2016 Massachusetts Institute of Technology

"""Extract images from a rosbag.
"""

import os
import sys
import argparse
import rosbag
from tqdm import tqdm

def print_progress_bar(i, n, bar_length=20, first_call=True):
    if n <= 0:
        return
    f = float(i) / n
    num_ticks = int(round(bar_length * f))
    num_ticks = min(bar_length, max(0, num_ticks))
    percent = min(100, max(0, int(round(100 * f))))
    s = '[' + '=' * num_ticks + '-' * (bar_length - num_ticks) + '] ' + '{: >3d}%'.format(percent)
    if not first_call:
        sys.stdout.write('\033[2K\r')
    sys.stdout.write(s)
    sys.stdout.flush()

if __name__ == '__main__':
    """Extract a folder of images from a rosbag.
    """
    parser = argparse.ArgumentParser(description="Split a bag with constant size.")
    parser.add_argument("bag_file", help="Input ROS bag.")
    parser.add_argument("output_dir", help="Output directory.")
    parser.add_argument("--bag_prefix", default="seg", help="Output bag file prefix.")
    parser.add_argument("--split_size", default="2048", help="Size of split bag in MB.")
    parser.add_argument('-t', '--topics', default="*", nargs="+",
                        help='string interpreted as a list of topics (wildcards \'*\' and \'?\' allowed) to include in the merged bag file')

    args = parser.parse_args()

    if args.topics == "*":
        topics = None
    else:
        topics = args.topics

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    split_size = int(args.split_size) * 1024 * 1024
    print "Splitting rosbag %s into bags with size = %s MB." % (args.bag_file, args.split_size)

    with rosbag.Bag(args.bag_file, "r") as bag:
        print "Total size = %.2f MB" %(float(bag.size)/1024/1024)
        i = 0
        current_bag = rosbag.Bag(os.path.join(args.output_dir, "%s-%i.bag"%(args.bag_prefix, i)), "w")
        print "new bag: ", os.path.join(args.output_dir, "%s-%i.bag"%(args.bag_prefix, i))
        print_progress_bar(0, split_size, first_call=True)
        for topic, msg, stamp in bag.read_messages(topics=topics, raw=True):
            # print "read topic:", topic
            if current_bag.size >= split_size:
                current_bag.close()
                i += 1
                current_bag = rosbag.Bag(os.path.join(args.output_dir, "%s-%04i.bag"%(args.bag_prefix, i)), "w")
                print "\nnew bag:", os.path.join(args.output_dir, "%s-%04i.bag"%(args.bag_prefix, i))
                print_progress_bar(0, split_size, first_call=True)
                
            current_bag.write(topic, msg, stamp, raw=True)
            print_progress_bar(current_bag.size, split_size, first_call=False)

        print_progress_bar(100, 100, first_call=False)
        sys.stdout.write("\n")
        sys.stdout.flush()
        current_bag.close()


