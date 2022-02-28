def domainExt(dom_f_in, fasta_file_in, fasta_file_out, dom_name):
    d = {}
    for i in dom_f_in.readlines():
        if i.startswith("#") or i == "" or i == "\n":
            continue
        else:
            line = i.strip().split()
            if line[6] == dom_name:
                if line[0] not in d:
                    d[line[0]] = [[int(line[1]), int(line[2])]]
                else:
                    d[line[0]].append([int(line[1]), int(line[2])])

    from Bio import SeqIO
    from Bio.SeqRecord import SeqRecord
    from Bio.Seq import Seq
    with open(fasta_file_out, 'w') as f_out:
        for seq_record in SeqIO.parse(open(fasta_file_in, mode='r'), 'fasta'):
            if seq_record.id in d:
                x = d[seq_record.id]
                for i in range(len(x)):
                    new_seq_record = SeqRecord(
                        seq_record.seq[int(x[i][0])-1:int(x[i][1])],
                        id = str(seq_record.id) + str(dom_name) + str(i + 1),
                        description=""
                    )
                    SeqIO.write(new_seq_record, f_out, 'fasta')