from pyvis.network import Network
import airtable_utils
import networkx as nx

G = nx.Graph()

net = Network(height='750px', width='100%', bgcolor='#222222', font_color='white')

net.show_buttons(filter_=['physics'])

data = airtable_utils.get_airtable_records("Clinical Relationships")
data_fields = []
for datum in data:
    data_fields.append(datum["fields"])


seen = set()
new_l = []
for d in data_fields:
    dstring = ""
    for item in d.items():
        dstring = dstring + str(item)
    
    t = dstring
    if t not in seen:
        seen.add(t)
        new_l.append(d)

deduped_data = new_l
record_weighted = []
for record in deduped_data:
    count = data_fields.count(record)
    for dic in deduped_data:
        if dic == record:
            dic["WEIGHT"] = count * count
            record_weighted.append(dic)

targets = []
sources = []
weights = []
for rec in record_weighted:
    print(rec)
    targets.append(rec["TARGET"])
    sources.append(rec["NAME"])
    weights.append(rec["WEIGHT"])

edge_data = zip(sources, targets, weights)


for e in edge_data:
    src = e[0]
    dst = e[1]
    w = e[2]

    net.add_node(src, src, title=src)
    net.add_node(dst, dst, title=dst, size = 5)
    net.add_edge(src, dst, value=w)

neighbor_map = net.get_adj_list()


net.show('clinical_network.html')
