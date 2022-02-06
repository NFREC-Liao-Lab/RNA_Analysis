#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author:young
# E-mail:yangzs_chi@yeah.net
# Created on 2021/10/25 10:23
# The latest version was edited on :  2021/10/25 22:23  By:young


import sys
import os
import re
from argparse import ArgumentParser
from goatools import obo_parser, base
import pandas as pd


help_info = 'This script is convert the GO annotation with GO annotation with wego format, ' \
            'TSV format (interproscan.sh and eggNOG)  to GENE2TERM format, and '
def make_options():
    parser = ArgumentParser(description=help_info)
    parser.add_argument("-i", '--in', action='store', dest='inputfile',
                        help='path of input file',
                        default=False)

    avg = parser.parse_args()
    in_file = avg.inputfile
    # in_format = avg.format
    # return (in_file, in_format)
    return (in_file)



# in_file = r"G:\genebang\GO\TEST\test.go"
# main
def gene_go_query(goterm_list):
    '''
    :param goterm_list: eg. goterm_list = ['GO:0042026', 'GO:0006457', 'GO:0016887', 'GO:0005524']
    :return:
    '''
    all_goterm_list = goterm_list
    for goterm in goterm_list:
        goterm_obj = obofile.query_term(goterm)
        if goterm_obj != None:
            parents_list = list(goterm_obj.get_all_parents())
            all_goterm_list = list(set(all_goterm_list + parents_list))
        else:
            all_goterm_list.remove(goterm)
            continue
    # remove top level
    # GO:0003674 molecular_function
    # GO:0005575 cellular_component
    # GO:0008150 biological_process
    all_goterm_obj_list = [obofile.query_term(go_term) for go_term in all_goterm_list if go_term != "GO:0003674" and go_term != "GO:0005575" and go_term != "GO:0008150" ]
    all_goterm_detail_list = ['\t'.join([go_term.id, "level_" + str(go_term.level), go_term.namespace, go_term.name]) for go_term in all_goterm_obj_list if go_term is not None]
    return all_goterm_detail_list
    #

def  go_annotation_parser(in_file):
    '''
    :param in_anno:   Result of GO annotation with wego format,  TSV format of interproscan.sh and eggNOG.
    :return:
    '''
    in_anno_text = open(in_file, "r").readlines()
    in_anno_text = [term.rstrip("\n") for term in in_anno_text if term.startswith("#") == False]
    in_anno_GO = [[term.split("\t")[0], re.findall(r'GO:\d{7}', term)] for term in in_anno_text if len(re.findall(r'GO:\d{7}', term)) > 0]
    # in_anno_GO :
    # [['GENE1', ['GO:0003824']], ['GENE2', ['GO:0003824']], ['GENE3', ['GO:0005524', 'GO:0006457', 'GO:0016887'], ...]
    gene_GO_dict = {}
    for term in in_anno_GO:
        gene_id = term[0]
        GO_list = term[1]
        if gene_id  not in gene_GO_dict.keys():
            gene_GO_dict[gene_id] = GO_list
        else:
            gene_GO_dict[gene_id] = list(set(gene_GO_dict[gene_id] + GO_list))
    # gene_GO_dict :
    # {'GENE1': ['GO:0003824'], 'GENE2': ['GO:0008080'],'GENE3': ['GO:0042026', 'GO:0006457', 'GO:0005524'], ... }
    out_file.write('Gene_ID\tGO_term\tLevel\tFunction_class\tFunction\n')
    for gene_id in gene_GO_dict.keys():
        goterm_detail_list = gene_go_query(gene_GO_dict[gene_id])
        for GO_term in goterm_detail_list:
            out_file.write(gene_id + "\t" + GO_term + "\n")

    #To  DataFrame too slow
    # df_go = pd.DataFrame(columns=['Gene_ID', 'GO_term', 'Level', 'Function_class', 'Function'])
    # for gene_id in gene_GO_dict.keys():
    #     goterm_detail_list = gene_go_query(gene_GO_dict[gene_id])
    #     for GO_term in goterm_detail_list:
    #         df_go.loc[len(df_go)] = pd.Series({'Gene_ID': gene_id , 'GO_term': GO_term[0], 'Level': GO_term[1],
    #                                               'Function_class': GO_term[2], 'Function': GO_term[3]})
    # df_go.to_csv(out_file_path, sep='\t', index=False)


# main over

if len(sys.argv) == 1:
    print(help_info)
    sys.exit()
else:
    in_file = make_options()

    # Download GO DAG file, go-basic.obo if not exist
    base.download_go_basic_obo("go-basic.obo")
    obofile = obo_parser.GODag('go-basic.obo', load_obsolete=False)

    path_list = os.path.split(in_file)
    out_file_name = path_list[-1].rsplit(".", 1)[0] + '_GO_anno.xls'
    out_file_path = os.path.join(path_list[0], out_file_name)
    stat_file_name = path_list[-1].rsplit(".", 1)[0] + '_GO_anno_stats.xls'
    stat_file_path = os.path.join(path_list[0], stat_file_name)

    out_file = open(out_file_path, "w+")
    # annotation
    go_annotation_parser(in_file)
    # stat and drawing
    os.remove("go-basic.obo")
    out_file.close()
