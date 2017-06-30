import os, sys, argparse
import simplejson as json
from tabulate import tabulate
import ezbpg
from ezbpg.utils   import save_edges
from ezbpg.matcher import partition_forest, refine_partition, describe_partition

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--infile", help="csv file to parse", required=True)
    return parser.parse_args()

def mkdir_soft(dirpath):
    if not os.path.exists(dirpath):
        os.mkdir(dirpath)

# edgeseq = purify(csviter(args.infile))
# g = Matcher(edgeseq)
def refine(g):
    p = partition_forest(g)
    r = refine_partition(p)
    rows,total = describe_partition(r)
    print(tabulate(rows,headers="firstrow"))

    print("Making for %d components total." % total['component'])
    for tag in sorted(r.keys()):
        print("class[%s] = %s" % (tag,{x:len(r[tag][x]) for x in r[tag]}))
    return r

def extract(outdir,tag,r):
    mkdir_soft(outdir)
    subdir = "comp/%s" % tag
    mkdir_soft(subdir)
    print("tag '%s' has %d component class(es)." % (tag,len(r[tag])))
    for t in sorted(r[tag].keys()):
        nj,nk = t
        components = r[tag][t]
        print ("class[%s] = has %d component(s):" % (t,len(components)))
        for i,edgelist in enumerate(components):
            basefile = "%d,%d-%d.txt" % (nj,nk,i)
            outpath = "%s/%s" % (subdir,basefile)
            print("%s .." % outpath)
            with open(outpath,"wt") as f:
                save_edges(f,edgelist)

def main():
    args = parse_args()

    g = ezbpg.slurp(args.infile)
    print("Consumed %d edge observations, of which %d were distinct." % (g.observed,g.distinct))
    print("stats = ",json.dumps(g.stats(),sort_keys=True))
    r = refine(g)

    tag = 'm-n'
    outdir = 'comp'
    extract(outdir,tag,r)

if __name__ == '__main__':
    main()



