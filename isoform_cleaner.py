#!/usr/bin/env python3

# created by Baki Coban
# An isoform cleaner for NCBI proteomes

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import argparse
import sys

def isoform_cleaner(file, outfile):
    d = {}
    fasta_sequences = SeqIO.parse(open(file), "fasta")
    for fasta in fasta_sequences:
        if "isoform" in fasta.description:
            line = fasta.description.strip().split()[:-2]
            if "isoform" in line:
                if " ".join(line[1:line.index("isoform")]) not in d:
                    d[" ".join(line[1:line.index("isoform")])] = [fasta]
                else:
                    d[" ".join(line[1:line.index("isoform")])].append(fasta)
    with open(outfile, "w") as f:
        for i in d:
            c = 0
            my_seq = SeqRecord(
                Seq(""),
                id="",
                name="",
                description="")
            for j in d[i]:
                if len(j.seq) > c:
                    c = len(j.seq)
                    my_seq = j
            SeqIO.write(my_seq, f, "fasta")

        fasta_sequences = SeqIO.parse(open(file), 'fasta')
        for fasta in fasta_sequences:
            if "isoform" not in fasta.description:
                SeqIO.write(fasta, f, "fasta")



def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f','--file', help='Proteome file', metavar='FILE')
    parser.add_argument('-o', '--out', help='Output file', metavar='FILE')
    args = parser.parse_args()

    if args.file is None:
        print("Error! You need to provide an exonerate file with -f option!", file=sys.stderr)

    try:
        isoform_cleaner(args.file, args.out)
    except Exception as e:
        sys.exit("failed to open file: %s" % (str(e)))

if __name__ == "__main__":
    main()