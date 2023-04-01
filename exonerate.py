#!/usr/bin/env python3

# created by Baki Coban
# A simple parser for exonerate output

import argparse
import sys


class Exonerate:
    pass
def readExonerate(filename):
    fh = open(filename, "r")
    ls = []
    i_fh = iter(fh)
    for i in i_fh:
        if "C4 Alignment:" in i:
            new = Exonerate()
            i = next(i_fh)
            i = next(i_fh)
            new.query = i.strip().split()[1]
            i = next(i_fh)
            new.target = i.strip().split()[1]
            i = next(i_fh)
            i = next(i_fh)
            new.score = int(i.strip().split()[2])
            i = next(i_fh)
            new.q_range = [i.strip().split()[2], i.strip().split()[4]]
            i = next(i_fh)
            new.t_range = [i.strip().split()[2], i.strip().split()[4]]

            ls.append(new)
    return ls




def insert_sorted(seq, elt):
    idx = 0
    if not seq or elt.score > seq[-1].score:
        seq.append(elt)
    else:
        while elt.score > seq[idx].score and idx < len(seq):
            idx += 1
        seq.insert(idx, elt)

def printer(filename):
    ls = readExonerate(filename)
    n = []
    for i in ls:
        insert_sorted(n, i)
    for i in n:
        print(i.query + "\t" + i.target + "\t" + str(i.score) + "\t" + " ".join(i.q_range) + "\t" + " ".join(i.t_range))

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f','--file', help='Exonerate output file', metavar='FILE')
    args = parser.parse_args()

    if args.file is None:
        print("Error! You need to provide an exonerate file with -f option!", file=sys.stderr)

    try:
        printer(args.file)
    except Exception as e:
        sys.exit("failed to open file: %s" % (str(e)))

if __name__ == "__main__":
    main()