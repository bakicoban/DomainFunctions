def pfam2xdom(file_in, f_out, dom_file):
    from Bio import SeqIO
    from Bio.SeqRecord import SeqRecord
    from Bio.Seq import Seq
    d = {}
    for seq_record in SeqIO.parse(open(file_in, mode='r'), 'fasta'):
        d[seq_record.id] = len(seq_record.seq)


    new_d = {}
    for i in dom_file.readlines():
        if i.startswith("#") or i == "" or i == "\n":
            continue
        else:
            line = i.strip().split()
            if line[0] not in new_d:
                f_out.write(">" + line[0] + " " +  str(d[line[0]]) + "\n")
                new_d[line[0]] = 1
            f_out.write(str(line[1]) + " " + str(line[2]) + " " +  line[6] + " "+ line[12] + "\n")