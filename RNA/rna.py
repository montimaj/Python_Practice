import random
from collections import defaultdict

def num_nucleotides(rna_string):
    nucleotide_list=('A','G','C','U')
    for n in nucleotide_list:
        print('Count('+n+')=', rna_string.count(n))
    return len(rna_string)

def specific_codon_count(rna_string, specific_codon):
    codon_count=defaultdict(lambda:0)
    codons=get_all_codons(rna_string)
    for codon in codons:
        codon_count[codon]+=1
    return codon_count[specific_codon]

def num_codons(rna_string):
    return int(len(rna_string)/3)

def get_all_codons(rna_string):
    codons=[]
    for i in range(num_codons(rna_string)):
        offset=3*i
        codons.append(rna_string[offset:offset+3])
    return codons

def get_codon(rna_string, n):
    offset=3*(n-1)
    return rna_string[offset:offset+3]

def first_start_codon(rna_string):
    codons = get_all_codons(rna_string)
    starts=get_all_start_codons(codons)
    if starts:
        return starts[0]
    return 'Not found'

def first_stop_codon(rna_string):
    codons=get_all_codons(rna_string)
    stops=get_all_stop_codons(codons)
    if stops:
        return (codons[stops[0]], stops[0])
    return 'Not found'

def first_stop_after_start(rna_string):
    codons=get_all_codons(rna_string)
    starts=get_all_start_codons(codons)
    stops = get_all_stop_codons(codons)
    if starts and stops:
        for stop in stops:
            if stop > starts[0]:
                return (codons[stop],stop)
    return 'Not found'

def is_valid_start(start,stop):
    return start<stop
        
def random_seq(n):
    result = ''
    while n > 0:
        result = result + random.choice(NUCLEOTIDE_LIST)
        n = n - 1
    return result

def get_all_start_codons(codons):
    starts=[]
    for index,codon in enumerate(codons):
        if codon=='AUG':
            starts.append(index)
    return starts

def get_all_stop_codons(codons):
    stops=[]
    for index, codon in enumerate(codons):
        if codon in AMINO_ACIDS['STOP']:
            stops.append(index)
    return stops

def rna_split(rna_string):
    codons=get_all_codons(rna_string)
    start=get_all_start_codons(codons)
    stop=get_all_stop_codons(codons)
    start.sort()
    stop.sort()
    #print('Start/Stop=', start, stop)
    rna_slices = []
    for start_idx in start:
        for stop_idx in stop:
            if is_valid_start(start_idx,stop_idx):
                slice = ''.join(codons[start_idx:stop_idx+1])
                rna_slices.append(slice)
                break
    return rna_slices

def codon_to_amino_acid(rna_slices):
    amino_dict={}
    for rna_slice in rna_slices:
        codons=get_all_codons(rna_slice)
        amino_acids=[]
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
    while True:
        n = random.randint(lower, upper)
        if n%3==0:
            return n

#rna='AUGGCUACGGCAGCGAAACUGCCCGAGCCGGAGAGAAGACCUAUUCCGUGCCCCCUGAAAACAGUGACACAUGAGCCUGGGUAUUAAACCAGUCAAGGG'
#rna='GGUAAUGAGGCCUAAGGAUCCGCCGAGGAAGUCUUCGGGACAGCGGAGUUCGUCAGCCCGUCCAAAGGAGAAGCCCAGCCUACUCCGCUCUUCGGGUUU'
#rna='CGUUCGCGAAGUAUGGUGAUUUACAUACUAAGGUUUGUGGUUACGUAUCGCGUAUCAAUAAUGAUGCAUCGUCACUACGGACACAAUGUGGAGUAACCC'
#rna='UUUUUCACAGUAUAAUGCGGAAUUGCCGGGUGACUGGGACCGAUGUGUAUGUAUCAUGGGGGCGACUCCUGUGCUAUGUAUCUAAGUAUCUUGCUGCUC'
#rna='ACGAACCUAAUGGCAUAUUUACCAUCUAAAUGUUCUGGGUUACAAACUCUAAUGUCCCGUUAUGGCCACUAAUUUGGCGGCGCGAAUGAGAUACGGGCA'
#rna='UCAAUGCCAAGCAGAGAGGCUGCAAAGCCUGGAAAGUCAUGAUUGAAUAUAAAGAUAGGAGAUAGCCUACAGAAAACCCCUUGAGUUGCACGUCGUAGU'
#rna='GCAUGGAGUUACCGGAUUUUAAGGAGAUCUCUCAUUAGCCUCCGCAUCCCCAACCGGUGCCGCCGAUGCCAACCUGUAGUGAUUUACACCCCGCCUAGU'
#rna='AAUGGGGUUAUAGUAAUUUUUCCCUGAUGAAUCCGAUGCAGAUCCCGCGCCUAAACGUCGGAGAUUGUACGUCUAACACCUAGAAGGAAGUAUGGUGUG'
#rna='GUCAGUCGGCCUUUUUGGUAUGCGCCGCGUUACCGCGCAGCGAACUUUCGAUCAGCGAGGCUAGCCUACGAAGUUUAAACCCCGUACGCCUCAAAGCGU'
#rna='GCUCUGUUUCCCUUACAAUUGAUUUUUUAUAGAAAUACCUGCAGUGUGACCCGCAGCUCACUGAAGAGCGGAUGAGGGUACCGAUGACACAAAUGCGCUACCGUCUCGUUCGCAGUAUAAAAGGUAUAAGAAUAUUGUCACCUCGGAUGCACCCCCAGAGUGUGACAGACUCGUAGC'
#rna='AUGGUCUCGUAGCGCCAAUGAAGAAAAGUAGCAAGGACCAGGUUUGGGUCGCCUUAUCACGGCUACGAACCGAUGGUGUUAGUUUAGUUGUACUCUCAACUGCCAAUUCCGUGUGUGCCUGCCGCAGUACCCCUGCAAUCACUAAUUUUCGGUUAGGGGAGGAGGCAGUGGUGGUGACAACGCGGUAUUGGGUUC'
#rna='GCAGUAAGCACAAUCUACACAAACUUGCUUGUAGUUGAGCCCAAUUACGGAAUCUCAUGAGGCUCCCAAAGUAAGAUAUUCACACCGGAAGGCUUCCGGGUG'
#rna='CUUCGGAUGAAGCUGUGGGCAAGUUGGGAUGAAUCGUGAUGGGUC'
#rna='GCGGAUCUUCUCACUCCGCACGGGUUAUUACCCUAGUAUGAUUAGCCCGGCCACAUGGAACUUUAUAUCGGUUGUACCACGGGCUAGUACACAUACGGGUUUUGCCGCGGAUUGUAAUGGAUCGAAGCUACUGCAACUCCUAUCCAAAGAUCUAUGUGGGGAGCCUGUGCGGAGGCCGAUCAUGCGUGGGUUCAC'
#rna='UCAUCACCCUAUAUGACAGCUGACAAAUAAUAUUCGGGCGACCGUAACGGCCUCCGUUUUUAGGUUGCGAGUAUAUUAUAUAAUACCUAAGGAAAGCGGUAUAGGCCGGGCCCCAUGCUCGAGCGAAUGCUCGGCUCUUAUAGAAUUCUACGAACCACUGGAAUCAUGUUCCAAGGUAUCCAGUGUUCUAUAGACUAG'
#rna='UUGUAGGACUCGUUACGCAGGGGCGAAUGGCCAUAGGGCAGUUGAGGGCGGGCGAGAUGCUCCGGACGUUGGCCGUACUUGAAUGAUGUAAAAGGAAACGGUUGAUAAAUAGUCCGGAGGGCCGCAUAGCUUUGCGUGCUGGAGGAGUGGCCGCGGGUCCAGCUUUCGGCUCAGUAAUUCGAAAAGUAAAGCCGUAACAGUAUCGCGCCCUCUGAAAGGUAGGCGUCGGUAGAACGACAAUCGCGGAGGCUGAUUCCACUAAUAUCCCUCCGGUGCUCCGUACCCAGCCAACCCUCCGAUGACCUUGGUCGUGACUACGUCGUCGUUACACCCGUUGUGACAAAACUUGUCAUGGUCCAACUUUAAUAUUCCUUGGGCGCUGGAAAAUCAACCCGUUCACAGCUACGGCAUUUCAUCUGAUAAGGUCCCCAAAGAGGAAACAGCUUGCGCCAACGGUCGUAAGAGCAAUAGGGUCGUCUCACUCCAACAGUUUAUAAGCCAAAGCAACGCGUAAGUUUUUUAUGUGACGACACCUUCCUCCCGCAGCUGUUGCUCCGCCGCGGACAUCGGGACGGACUUCGCUCGGGGAAAACAACUCGUUUAACAGGGCCUUAGCCCCUAUAACUGGAGCUGUUCGACAGGGUAUGGAUUAUUUUUCGAAAUACGUCCCUCUCAACGGGGCGACUUGAACGUCCAGCCUGUUCAUCGGGAAGAUUUACGGUGGAAGGUAUGACUCCACACGCGACGCAUCGUCGGCCAUAGUAAUAAACUACUCAGACUACAAAUAGAUAUGGUCUUGCGACCCAGUAUGCCACUUUUCUGAAUUUGAUUAGAUAACUUUAUCCUACGGCAGCGCGGCAAUUCGACAGCAUGGGUAUGGAAUCAUUCGUAAACAGAAGUACAUGGAUGGCUAAGACUCAGGGCCUGUGUAACUCCAAAACAUGGUGCUCGCUGUAAAUUAGCUUACUUACCACACUUUUGACUCCAUUACUCCACUUUUUUUUUUGUUCCUAUAGCUGUGUGGCGACUCGUGGCGCGCAAACGGUUACUGGCGUGACAGGAACGAAACCGGGCAUGCAUAGCCUUCAAUCACAACCAGCCCAGUCCCAGUUCUCUUUC'

rna_length=rna_seq_length(99,1e+5)
rna=random_seq(rna_length)
print('RNA[Len='+str(rna_length)+']=',rna,'\n')
print('Num nucleotides:', num_nucleotides(rna))
n=num_codons(rna)
print('\nNum codons=', n)
n=random.randint(0, n)
print('Codon #'+str(n)+'=', get_codon(rna, n))
print('\nFirst start codon index=', first_start_codon(rna))
print('First stop codon index=', first_stop_codon(rna))
print('First stop codon after first start=', first_stop_after_start(rna),'\n')
rna_slices=rna_split(rna)
if rna_slices:
    amino_dict=codon_to_amino_acid(rna_slices)
    show_amino_acids(amino_dict)
else:
    print('Cant\'t slice')