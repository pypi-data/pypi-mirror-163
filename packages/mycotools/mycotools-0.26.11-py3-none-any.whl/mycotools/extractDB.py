#! /usr/bin/env python3

import os
import sys
import copy
import random
import argparse
from collections import defaultdict
from mycotools.lib.kontools import file2list, intro, outro, format_path, eprint
from mycotools.lib.dbtools import mtdb, masterDB

def extract_unique(db, allowed = 1, sp = True):
    keys = copy.deepcopy(list(db.keys()))
    random.shuffle(keys)
    prep_db0 = {x: db[x] for x in keys}
    prep_db1 = mtdb().set_index('ome')
    if sp:
        found = defaultdict(int)
        for ome, row in prep_db0.items():
            name = row['taxonomy']['species']
            found[name] += 1
            if found[name] <= allowed:
                prep_db1[ome] = row
    else:
        found = set()
        for ome, row in prep_db0.items():
            name = row['taxonomy']['species'] + ' ' + row['strain']
            if name not in found:
                prep_db1[ome] = row
            found_prep = list(found)
            found_prep.append(name)
            found = set(found_prep)
    return prep_db1

def extract_tax(db, lineages, classification):
    if isinstance(lineages, str):
        lineages = [lineages]
    lineages = set(x.lower() for x in lineages)
    new_db = mtdb().set_index()
    for ome in db:
        try:
            if db[ome]['taxonomy'][classification].lower() in lineages:
                new_db[ome] = db[ome]
        except KeyError:
            pass

    return new_db

def extract_ome(db, omes):
    new_db = mtdb().set_index()
    for i in db:
        if i in omes:
            new_db[i] = db[i]
    return new_db

def extract_source(db, source):
    return mtdb({ome: row for ome, row in db.items() \
                   if row['source'].lower() == source.lower()}, 
                   index = 'ome')

def extract_pub(db):
    new_db = mtdb().set_index()
    for ome, row in db.items():
        if row['published']:
            new_db[ome] = row
    return new_db

def main( 
    db, unique_strains = False, unique_species = 0, 
    lineage_list = [], rank = None, omes_set = set(),
    source = None, nonpublished = False, inverse = False
    ):

    db = db.set_index('ome')
    if unique_strains:
        db = extract_unique(db, sp = False)
    if unique_species > 0:
        db = extract_unique(db, unique_species, sp = True)

    # extract each taxonomic entry based on the classification specified
    if lineage_list:
        new_db = extract_tax(db, lineage_list, rank)
    # if an ome list is specified then open it, store each entry in a list and pull each ome
    elif omes_set:
        extract_ome(db, omes)
    # if none of these are specified then create a `new_db` variable to work for later
    else:
        new_db = db

    # if there is a source specified, extract it or the opposite
    if source:
        new_db = extract_source(new_db, source)

    # if you want publisheds, then just pull those out 
    if not nonpublished:
        new_db = extract_pub(new_db)

    if inverse:
        new_omes = set(new_db.keys())
        inv_db = mtdb().set_index()
        for ome, row in db.items():
            if ome not in new_omes:
                inv_db[ome] = row
        return inv_db.reset_index()
    else:
        return new_db.reset_index()


if __name__ == '__main__':

    parser = argparse.ArgumentParser( description = \
       'Extracts a MycotoolsDB from arguments. E.g.\t`extractDB.py ' + \
       '-l Atheliaceae -r family`' )
    parser.add_argument('-l', '--lineage')
    parser.add_argument('-r', '--rank', help = "Taxonomy rank")
    parser.add_argument('-s', '--source')
    parser.add_argument('-n', '--nonpublished', action = 'store_true', 
        help = 'Include restricted')
    parser.add_argument('-u', '--unique_strain', action = 'store_true')
    parser.add_argument('-a', '--allowed_sp', default = 0, type = int, 
        help = 'Replicate species allowed' )
    parser.add_argument('-i', '--inverse', action = 'store_true', 
        help = 'Inverse [source|lineage(s)|nonpublished]')
    parser.add_argument('-ol', '--ome', help = "File w/list of omes" )
    parser.add_argument('-ll', '--lineages', help = 'File w/list of lineages (same rank)' )
    parser.add_argument('--headers', action = 'store_true')
    parser.add_argument('-', '--stdin', action = 'store_true')
    parser.add_argument('-d', '--database', default = masterDB())
    parser.add_argument('-o', '--output' )
    args = parser.parse_args()
    db_path = format_path( args.database )


    if (args.lineage or args.lineages) and not args.rank:
        eprint('\nERROR: need rank for lineage(s)', flush = True)
        sys.exit(5)
    elif args.lineage or args.lineages:
        eprint("\nWARNING: extracting taxonomy is subject to taxonomic error and errors in NCBI's hiearchy\n")

    output = 'stdout'
    if args.output:
        output = format_path( args.output )
        if not output.endswith( '/' ):
            tag = ''
                       
            if args.lineage:
                tag += '_' + args.lineage
            if args.lineages:
                tag += '_taxonomy'
            if args.source:
                tag += args.source.lower()
            if not args.nonpublished:
                tag += '_pub'
            output += '/' + os.path.basename( db_path ) + tag
        
    args_dict = {
        'database': db_path,
        'output': output,
        'lineage': args.lineage,
        'lineages list': args.lineages,
        'rank': args.rank,
        'ome_list': args.ome,
        'Source': args.source,
        'unique': args.allowed_sp,
        'nonpublished': args.nonpublished,
        'inverse': args.inverse,
        'headers': bool(args.headers)
    	}
#    start_time = intro( 'Abstract Database', args_dict, stdout = args.output )

    if args.stdin:
        data = ''
        for line in sys.stdin:
            data += line.rstrip() + '\n'
        data = data.rstrip()
        db = mtdb(data, stdin=True)
    else:
       db = mtdb( db_path )

    if args.ome:
        omes = set(file2list(format_path(args.ome)))
    else:
        omes = set()

    if args.lineages:
        lineage_list = file2list(format_path(lineage_list))
    elif args.lineage:
        lineage_list = [args.lineage]
    else:
        lineage_list = []

    new_db = main( 
        db, rank = args.rank, lineage_list = lineage_list,
        omes_set = omes, source = args.source, unique_species = args.allowed_sp, 
        nonpublished = args.nonpublished, inverse = args.inverse
        )
    if args.output:
        new_db.df2db( output )
    else:
        new_db.df2db( headers = bool(args.headers) )

 #   outro( start_time, stdout = args.output )
    sys.exit(0)
