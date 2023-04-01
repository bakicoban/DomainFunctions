#!/usr/bin/env python3

# created by Baki Coban
# Newick tree file to cds of nodes - only for ensembl proteins


import argparse
import sys
import requests
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


#returns list of tree leaves
def newickfile2leafnames(newickfilepath):
    from Bio import Phylo
    tree = Phylo.read(newickfilepath, "newick")
    l = []
    for leaf in tree.get_terminals():
        s = str(leaf.name)
        l.append(s[s.find("_")+1:-2])
    return l


#ensembl id list to cds
def cds(ensembl_id, f_out):
    f = open(f_out, "w")
    ls = []
    server = "https://rest.ensembl.org"
    for i in ensembl_id:
        ext = "/sequence/id/" + i + "?type=cds"
        r = requests.get(server + ext, headers={"Content-Type": "text/plain"})
        if not r.ok:
            pass
        ls.append(r.text)
    newls = []
    for i in range(len(ensembl_id)):
        if "error" in ls[i]:
            pass
        else:

            fasta = SeqRecord(
                Seq(ls[i]),
                id=ensembl_id[i],
                description= ""
            )
            SeqIO.write(fasta, f, 'fasta')
    return newls

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f','--file', help='Newick tree file', metavar='FILE')
    parser.add_argument('-o', '--out', help='CDS output file', metavar='FILE')
    args = parser.parse_args()

    if args.file is None:
        print("Error! You need to provide an exonerate file with -f option!", file=sys.stderr)

    try:
        l = newickfile2leafnames(args.file)
        cds(l, args.out)
    except Exception as e:
        sys.exit("failed to open file: %s" % (str(e)))

if __name__ == "__main__":
    main()






