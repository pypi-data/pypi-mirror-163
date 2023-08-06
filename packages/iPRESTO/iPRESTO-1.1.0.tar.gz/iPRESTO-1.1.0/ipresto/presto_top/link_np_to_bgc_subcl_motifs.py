#!usr/bin/env python3
'''
Author: Joris Louwen

Part of iPRESTO, Bioinformatics group Wageningen University.
PI: Marnix Medema

Script to link NPs known to be produced by certain organism to BGCs through
sub-cluster analysis with iPRESTO.

Required:
-output file of NPatlas for a substructure search
    (https://www.npatlas.org/joomla/index.php/search/advanced-search)
-iPRESTO output (PRESTO-TOP output), sub-cluster motifs. Sub-cluster motifs
    should be grouped by motif. This is for example the 
    matches_per_topic_filtered.txt

Usage:
python3 link_np_to_bgc.py -h
'''

import argparse
from collections import defaultdict
from glob import glob, iglob
import os
import time

def get_commands():
    parser = argparse.ArgumentParser(description="Script to link NPs known \
    to be produced by certain organism to BGCs through sub-cluster analysis \
    with iPRESTO. Needed are NPatlas output (tsv) and PRESTO-TOP output.")
    parser.add_argument("-i", "--in_file", help="Input substructure search \
        file downloaded from NPatlas output. Can be multiple files.",
        required=True, nargs='+')
    parser.add_argument("-o", "--out_file", dest="out_file", 
        required=True, help="Output file")
    parser.add_argument("-m", "--motifs_file", help="File containing\
        sub-cluster motifs, such as matches_per_topic_filtered.txt")
    parser.add_argument("-s", "--subcluster_selection", help="The one or more\
        sub-cluster motif(s) (numbers) that you are interested in that is \
        annotated with the substructure from the NPatlas search",nargs='+')
    parser.add_argument("-t", "--taxonomy_file", help="File linking BGCs\
        to organism names, tsv of bgc\torganism")
    parser.add_argument("--min_genes", default=0, type=int, help="Minimum \
        amount of genes that need to match the sub-cluster motif, \
        default = 0")
    return parser.parse_args()

def extract_subcl_motif(infile, motif, min_genes = 0):
    '''Extract all BGCs with motif_num as {bgc: [info_motif_match]}

    infile: str, filepath to motif file
    motif: list of str, name(s) of motif(s)
    min_genes: int, minimum amount of genes needed to match the subcluster
        motif
    '''
    right_motif = False
    bgc_dict = {}
    with open(infile, 'r') as inf:
        for line in inf:
            line = line.strip()
            if line.startswith('#'):
                right_motif = False
                #header of motif matches
                motif_in_file = line.split(', ')[0].split(' ')[-1]
                if motif_in_file in motif:
                    right_motif = True
            else:
                if right_motif:
                    line = line.split('\t')
                    bgc = line.pop(3)
                    genes = [gene.split(':')[0] for gene in line[2].split(',')]
                    if len(genes) >= min_genes:
                        bgc_dict[bgc] = line
    return bgc_dict

def parse_npatlas(infiles):
    '''Parse the NPatlas output to {NPatlas_id:[genus,species]}
    
    infiles: list of str, filepath to NPatlas file
    '''
    id_dict = {}
    for infile in infiles:
        with open(infile,'r') as inf:
            #header
            header = inf.readline().strip().split('\t')
            genus_ind = [i for i,genus in enumerate(header) if genus ==\
                'GENUS'][0]
            spec_ind = [i for i,species in enumerate(header) if species ==\
                'SPECIES'][0]
            has_mibig_i = [i for i,mibig in enumerate(header) if mibig ==\
                'COMPOUND_HAS_MIBIG'][0]

            for line in inf:
                line = line.strip().split('\t')
                np_id = line[0]
                other_info = line[1:4]
                genus = line[genus_ind]
                spec = line[spec_ind]
                has_mibig = [line[has_mibig_i]]
                id_dict[np_id] = [genus, spec] + other_info + has_mibig
        return id_dict

def read_tax(infile):
    '''Parse the taxonomy information into {bgc: [taxonomy info]}
    
    infile: str, filepath to taxonomy file
    '''
    tax_dict = {}
    with open(infile,'r') as inf:
        for line in inf:
            line = line.strip().split('\t')
            tax_dict[line[0]] = line[1]
    return tax_dict

def link_np_to_bgc(np_dict, tax_dict, motif_dict):
    '''Link NPatlas entry to bgc through string matching of taxonomy strings

    np_dict: dict, {NPatlas_id:[genus,species]}
    tax_dict: dict, {bgc: [taxonomy info]}
    motif_dict: dict, {bgc: [info_motif_match]} bgcs in the motif of interest
    result_dict: {np: {'genus': ['bgc\ttaxonomy info'],
        'species: ['bgc\ttaxonomy info'] } } Meaning a match only to the genus
        or also a match to the species name, strain matching is not included
        for now
    '''
    result_dict = defaultdict(dict)
    #get tax from bgcs in motif
    motif_tax = {bgc:tax_dict[bgc] for bgc in motif_dict if bgc in tax_dict}
    for np, info in np_dict.items():
        genus, spec = info[:2]
        #there might be spaces ea 'sp. CNQ-418', 'aeruginosa T 359'
        spec_l = spec.split()
        spec_name = spec_l.pop(0) #only the species name
        for bgc, tax in motif_tax.items():
            taxl = tax.lower()
            if genus.lower() in taxl:
                if spec_name.lower() in taxl:
                    if all(spec_i.lower() in taxl for spec_i in spec_l):
                        #exact match
                        try:
                            result_dict[np]['exact'].append(\
                                ' '.join([bgc,tax]))
                        except KeyError:
                            result_dict[np]['exact'] = [' '.join([bgc,tax])]
                    else:
                        #genus and species match
                        try:
                            result_dict[np]['species'].append(\
                                ' '.join([bgc,tax]))
                        except KeyError:
                            result_dict[np]['species'] = [' '.join([bgc,tax])]
                else:
                    #genus match but not species
                    try:
                        result_dict[np]['genus'].append(' '.join([bgc,tax]))
                    except KeyError:
                        result_dict[np]['genus'] = ['\t'.join([bgc,tax])]
    return result_dict

def write_results(result_dict, np_dict, tax_dict, motif_dict, outfile):
    '''Write the output to a file

    result_dict: {np: {'genus': ['bgc\ttaxonomy info'],
        'species: ['bgc\ttaxonomy info'] } } Meaning a match only to the genus
        or also a match to the species name, strain matching is not included
        for now
    np_dict: dict, {NPatlas_id:[genus,species]}
    tax_dict: dict, {bgc: [taxonomy info]}
    motif_dict: dict, {bgc: [info_motif_match]} bgcs in the motif of interest
    '''
    with open(outfile, 'w') as outf:
        outf.write('###Each compound starts with >. Compound header is: '+
            'NPA ID, Genus, Species, Cluster ID, Node ID, Name(s), '+
            'Has Mibig. Exact, species or genus matches start start at #.\n')
        for np, info in result_dict.items():
            outf.write('>{}\t{}\n'.format(np, '\t'.join(np_dict[np])))
            if 'exact' in info:
                outf.write('#Exact_matches:\n')
                for result in info['exact']:
                    outf.write('{}\n'.format(result))
            if 'species' in info:
                outf.write('#Species_matches:\n')
                for result in info['species']:
                    outf.write('{}\n'.format(result))
            if 'genus' in info:
                outf.write('#Genus_matches:\n')
                for result in info['genus']:
                    outf.write('{}\n'.format(result))

if __name__ == "__main__":
    start = time.time()
    print("\nStart")
    cmd = get_commands()

    bgcs_in_motif = extract_subcl_motif(cmd.motifs_file,
        cmd.subcluster_selection, cmd.min_genes)

    # print(bgcs_in_motif, len(bgcs_in_motif))

    np_ids = parse_npatlas(cmd.in_file)

    # print(np_ids)

    bgc_tax = read_tax(cmd.taxonomy_file)
    # print(bgc_tax)

    linked_np_bgc = link_np_to_bgc(np_ids, bgc_tax, bgcs_in_motif)
    # print(linked_np_bgc.keys())

    write_results(linked_np_bgc, np_ids, bgc_tax, bgcs_in_motif, cmd.out_file)

    end = time.time()
    t = end-start
    t_str = '{}h{}m{}s'.format(int(t/3600),int(t%3600/60),int(t%3600%60))
    print('\nScript completed in {}'.format(t_str))
