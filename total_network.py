
from posixpath import split
import rapidfuzz
from rapidfuzz import fuzz
from itertools import combinations
from pyvis.network import Network

net = Network(height='750px', width='100%', bgcolor='#222222', font_color='white')
net.show_buttons(filter_=['physics'])

records = []
with open("records.txt") as readfile:
    lines = readfile.read().split("\n")
    for line in lines[1:]:
        record = {}
        split_line = line.split(",,,")
        record["TICKER"] = split_line[0]
        record["SOURCE"] = split_line[1]
        record["TARGET"] = split_line[2]
        records.append(record)


sources = []
targets = []
for record in records:
    source = record["SOURCE"].lower()
    if source.find(" ") != -1:
        ssource = source.split(" ")
        capitalized_source = ""
        for item in ssource:
            capitalized_source = capitalized_source + item.capitalize() + " "
        sources.append(capitalized_source.strip())
    else:
        sources.append(source.capitalize().strip())

for record in records:
    target = record["TARGET"].lower()
    if target.find(" ") != -1:
        starget = target.split(" ")
        capitalized_target = ""
        for item in starget:
            capitalized_target = capitalized_target + item.capitalize() + " "
        targets.append(capitalized_target.strip())
    else:
        targets.append(target.capitalize().strip())

        

keywords = ["Pharmaceuticals","Pharmaceutical","Pharma","Biopharmaceuticals","Biopharmaceutical","Biopharma","Therapeutics", "American Depositary Shares","Biosciences","Biologics","Holdings","Oncology","Bioscience","Is Now A Wholly Owned Subsidiary Of Pfizer","Is Now A Wholly Owned Subsidiary","Clinical Oncology Group","Development","Biotechnology","Corporation","Corp.","Corp","Incorporated","Inc.","Inc","Limited","Ltd.","Ltd", "Group","A/s","Biotherapeutics","Medicines","Medicine"," Bio"]
clean_sources = []
clean_targets = []

for source in sources:
    new_source = source
    for kw in keywords:
        if new_source.find(kw) != -1:
            new_source = new_source.replace(kw, "")
            new_source = new_source.replace(",", "")
            new_source = new_source.replace(" ,", "")
            new_source = new_source.replace("'", "")
            new_source = new_source.replace("  ", "")
            new_source = new_source.replace("  ", "")

        if new_source.lower().find("a wholly") != -1:
            new_source = new_source.split("A Wholly")[0]
    
    clean_sources.append(new_source.strip())

for target in targets:
    new_target = target
    for kw in keywords:
        if new_target.find(kw) != -1:
            new_target = new_target.replace(kw, "")
            new_target = new_target.replace(",", "")
            new_target = new_target.replace(" ,", "")
            new_target = new_target.replace("'", "")
            new_target = new_target.replace("  ", "")
            new_target = new_target.replace("  ", "")
            
        if new_target.lower().find("a wholly") != -1:
            new_target = new_target.split("A Wholly")[0]


        if new_target.find("(") != -1:
            new_target_split = new_target.split("(")
            starget_split = ""
            for starget in new_target_split:
                if starget.find(")") != -1:
                    new_target_split.remove(starget)
                    new_target_split.append(starget.split(")")[1])
            deparenthasized = ""
            for dptarget in new_target_split:
                deparenthasized = deparenthasized + dptarget + " "
            
            new_target = deparenthasized
            

    
    clean_targets.append(new_target.strip())



sources = list(set(clean_sources))
targets = list(set(clean_targets))

entities = sources + targets
print(str(len(entities)))

entities = list(set(entities))
print(str(len(entities)))


new_entities = []

treshold = 97
minGroupSize = 1
entities = { c:{c} for c in sources }
for a,b in combinations(sources,2):
    if fuzz.WRatio(a,b) < treshold: continue
    entities[a].add(b)
    entities[b].add(a)
groups = []
ungrouped = set(sources)
while ungrouped:
    bestGroup = {}
    for city in ungrouped:
        g = entities[city] & ungrouped
        for c in g.copy():
            g &= entities[c] 
        if len(g) > len(bestGroup):
            bestGroup = g
    if len(bestGroup) < minGroupSize : break  # to terminate grouping early change minGroupSize to 3
    ungrouped -= bestGroup
    new_entities.append((list(bestGroup)[0], list(bestGroup)))





new_records = []
for record in records:
    new_record = {}
    new_record["TICKER"] = record["TICKER"]
    record_target = record["TARGET"]
    record_source = record["SOURCE"]
    for kw in keywords:
        if record_target.find(kw) != -1:
            record_target = record_target.replace(kw, "")
            record_target = record_target.replace(",", "")
            record_target = record_target.replace(" ,", "")
            record_target = record_target.replace("'", "")
            record_target = record_target.strip()

    for kw in keywords:
        if record_source.find(kw) != -1:
            record_source = record_source.replace(kw, "")
            record_source = record_source.replace(",", "")
            record_source = record_source.replace(" ,", "")
            record_source = record_source.replace("'", "")
            record_source = record_source.strip()



    for target in new_entities:
        for new_target in target[1]:
            if rapidfuzz.fuzz.WRatio(record_target.lower(), new_target.lower()) > 94:
                new_record["TARGET"] = target[0]

    for source in new_entities:
        for new_source in source[1]:
            if rapidfuzz.fuzz.WRatio(record_source.lower(), new_source.lower()) > 94:
                new_record["SOURCE"] = source[0]
    
    new_records.append(new_record)



targets = []
sources = []
for rec in records:
    try:
        targets.append(rec["TARGET"])
        sources.append(rec["SOURCE"])
    except:
        pass

edge_data = zip(sources, targets)

for e in edge_data:
    src = e[0]
    dst = e[1]

    net.add_node(src, src, title=src)
    net.add_node(dst, dst, title=dst, size = 5)
    net.add_edge(src, dst)

neighbor_map = net.get_adj_list()


net.show('clinical_network_total.html')