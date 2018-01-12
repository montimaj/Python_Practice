import random

def num_nucleotides(rna_string):
    nucleotide_list=('A','G','C','U')
    for n in nucleotide_list:
        print('Count('+n+')=', rna_string.count(n))
    return len(rna_string)

def num_codons(rna_string):
    return int(len(rna_string)/3)

def get_all_codons(rna_string):
    codons=[]
    for i in range(num_codons(rna_string)):
        offset=3*i
        codons.append(rna_string[offset:offset+3])
        #print('Codon #'+str(i+1), codons[i])
    return codons

def get_codon(rna_string, n):
    offset=3*(n-1)
    print('Codon #'+str(n), rna_string[offset:offset+3])

def first_start_codon(rna_string):
    return rna_string.find('AUG')

def start_codons(rna_string):
    start_list = []
    offset = 0
    while True:
        pos = rna_string.find('AUG')
        if pos == -1:
            return start_list
        start_list.append(pos+offset)
        rna_string=rna_string[pos+3:]
        offset+=pos+3

def stop_codons(rna_string, start):
    stop_codons = AMINO_ACIDS['STOP']
    stop_list = []
    for codon in stop_codons:
        rna_copy=rna_string[:]
        offset=0
        while rna_copy:
            pos = rna_copy.find(codon)
            if pos==-1:
                break
            if is_proper_stop_codon(pos, start):
                stop_list.append(pos + offset)
            rna_copy=rna_copy[pos+3:]
            offset+=pos+3
    return stop_list

def first_stop_codon(rna_string):
    stop_codons=AMINO_ACIDS['STOP']
    stop_idx=[]
    for codon in stop_codons:
        stop=rna_string.find(codon)
        if stop!=-1:
            stop_idx.append(stop)
    if stop_idx:
        return min(stop_idx)
    return -2

def is_proper_stop_codon(stop, start):
    for codon in start:
        if (stop-codon) > 2 and (stop+3-codon)%3==0:
            return True
    return False

def is_valid_start(start,stop):
    return start<stop and (stop+3-start)%3==0

def remove_invalid_starts(start, stop):
    invalid_starts={}
    for codon1 in start:
        invalid_starts[codon1]=0
        for codon2 in stop:
            if not(is_valid_start(codon1,codon2)):
                invalid_starts[codon1]+=1                
            else:                
                invalid_starts[codon1]-=1   
    for (codon,invalid) in invalid_starts.items():
        if invalid>0:
            start.remove(codon)

def stop_codon_after_start(rna_string, start_idx):
    rna_copy=rna_string[:]
    l=0
    while rna_copy:
        stop_idx = first_stop_codon(rna_copy)
        if  is_proper_stop_codon(stop_idx,start_idx):
            print(rna_copy[stop_idx:stop_idx+3])
            print(rna_string[stop_idx+l+start_idx:stop_idx+l+start_idx+3])
            return stop_idx
        rna_copy=rna_copy[start_idx+3:]
        l+=3
    return -2
        
def random_seq(n):
    result = ''
    while n > 0:
        result = result + random.choice(NUCLEOTIDE_LIST)
        n = n - 1
    return result

def rna_split(rna_string):
    start = start_codons(rna_string[:])
    stop = stop_codons(rna_string[:], start)
    #print('Inital start, stop=',start, stop)
    if start and stop:
        start.sort()
        stop.sort()
        remove_invalid_starts(start,stop)
        #print('Corrected start, stop=',start, stop)
        rna_slices=[]
        for start_idx in start:
            for stop_idx in stop:
                if is_valid_start(start_idx,stop_idx):
                    rna_slices.append(rna_string[start_idx:stop_idx+3])
        return rna_slices
    
def codon_to_amino_acid(rna_slices):    
    amino_dict={}
    for rna_slice in rna_slices:
        codons=get_all_codons(rna_slice)
        amino_acids=[]
        #print(codons, len(codons))
        for codon in codons:
            for amino_acid, codon_tuple in AMINO_ACIDS.items():
                if codon in codon_tuple:
                    amino_acids.append(amino_acid)
                    break
        amino_dict[rna_slice]=amino_acids
    return amino_dict

def show_amino_acids(amino_dict):
    num_slice=1
    for rna_slice, amino_acid in amino_dict.items():
        print('\nRNA Slice #'+str(num_slice)+'[Len='+str(len(rna_slice))+']:', rna_slice)
        print('Amino Acid Form:', amino_acid)
        num_slice+=1
       
NUCLEOTIDE_LIST=('U','C', 'A', 'G')
AMINO_ACIDS={   'Phenylalanine': ('UUU', 'UUC'),
                'Leucine':('UUA', 'UUG', 'CUU', 'CUC', 'CUA', 'CUG'),
                'Isoleucine': ('AUU', 'AUC', 'AUA'),
                'Methionine/START': ('AUG'),
                'Valine': ('GUU', 'GUC', 'GUA', 'GUG'),
                'Serine': ('UCU', 'UCC', 'UCA', 'UCG', 'AGU', 'AGC'),
                'Proline': ('CCU', 'CCC', 'CCA', 'CCG'),
                'Threonine': ('ACU', 'ACC', 'ACA', 'ACG'),
                'Alanine': ('GCU', 'GCC', 'GCA', 'GCG'),
                'Tyrosine': ('UAU', 'UAC'),
                'STOP': ('UAA', 'UGA', 'UAG'),
                'Histidine': ('CAU', 'CAC'),
                'Glutamine': ('GAA', 'GAG'),
                'Asparagine': ('AAU', 'AAC'),
                'Lysine': ('AAA', 'AAG'),
                'Aspartic acid': ('GAU', 'GAC'),
                'Glutamic acid': ('GAA', 'GAG'),
                'Cysteine': ('UGU', 'UGC'),
                'Tryptophan': ('UGG'),
                'Arginine': ('CGU', 'CGC', 'CGA', 'CGG', 'AGA', 'AGG'),
                'Glycine': ('GGU', 'GGC', 'GGA', 'GGG')
            }

def rna_seq_length(lower, upper):
    n=random.randint(lower, upper)
    if n%3==0:
        return n
    return rna_seq_length(lower, upper)

#rna='AUGGCUACGGCAGCGAAACUGCCCGAGCCGGAGAGAAGACCUAUUCCGUGCCCCCUGAAAACAGUGACACAUGAGCCUGGGUAUUAAACCAGUCAAGGG'
#rna='GGUAAUGAGGCCUAAGGAUCCGCCGAGGAAGUCUUCGGGACAGCGGAGUUCGUCAGCCCGUCCAAAGGAGAAGCCCAGCCUACUCCGCUCUUCGGGUUU'
#rna='CGUUCGCGAAGUAUGGUGAUUUACAUACUAAGGUUUGUGGUUACGUAUCGCGUAUCAAUAAUGAUGCAUCGUCACUACGGACACAAUGUGGAGUAACCC'
#rna='UUUUUCACAGUAUAAUGCGGAAUUGCCGGGUGACUGGGACCGAUGUGUAUGUAUCAUGGGGGCGACUCCUGUGCUAUGUAUCUAAGUAUCUUGCUGCUC'
#rna='ACGAACCUAAUGGCAUAUUUACCAUCUAAAUGUUCUGGGUUACAAACUCUAAUGUCCCGUUAUGGCCACUAAUUUGGCGGCGCGAAUGAGAUACGGGCA'
#rna='UCAAUGCCAAGCAGAGAGGCUGCAAAGCCUGGAAAGUCAUGAUUGAAUAUAAAGAUAGGAGAUAGCCUACAGAAAACCCCUUGAGUUGCACGUCGUAGU'
#rna='GCAUGGAGUUACCGGAUUUUAAGGAGAUCUCUCAUUAGCCUCCGCAUCCCCAACCGGUGCCGCCGAUGCCAACCUGUAGUGAUUUACACCCCGCCUAGU'
#rna='AAUGGGGUUAUAGUAAUUUUUCCCUGAUGAAUCCGAUGCAGAUCCCGCGCCUAAACGUCGGAGAUUGUACGUCUAACACCUAGAAGGAAGUAUGGUGUG'
#rna='GUCAGUCGGCCUUUUUGGUAUGCGCCGCGUUACCGCGCAGCGAACUUUCGAUCAGCGAGGCUAGCCUACGAAGUUUAAACCCCGUACGCCUCAAAGCGU'
rna_length=rna_seq_length(99,1e+5)
rna=random_seq(rna_length)
print('RNA[Len='+str(rna_length)+']=',rna)
rna_slices=rna_split(rna)
if rna_slices:
    amino_dict=codon_to_amino_acid(rna_slices)
    show_amino_acids(amino_dict)
else:
    print('Cant\'t slice')
