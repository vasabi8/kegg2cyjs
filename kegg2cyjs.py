import json
import requests
from bs4 import BeautifulSoup

import pandas as pd

__author__ = 'Kozo Nishida'
__email__ = 'knishida@riken.jp'
__version__ = '0.0.1'
__license__ = 'MIT'

API_BASE = 'http://rest.kegg.jp/'

GLOBAL_PATHWAY_IDS = ("01100", "01110", "01120", "01130")

KEGG_STYLE = [ {
  "format_version" : "1.0",
  "generated_by" : "cytoscape-3.7.1",
  "target_cytoscapejs_version" : "~2.1",
  "title" : "keggstyle",
  "style" : [ {
    "selector" : "node",
    "css" : {
      "font-family" : "Dialog.plain",
      "font-weight" : "normal",
      "border-width" : 3.0,
      "shape" : "roundrectangle",
      "font-size" : 12,
      "color" : "rgb(51,51,51)",
      "border-opacity" : 1.0,
      "text-valign" : "center",
      "text-halign" : "center",
      "background-opacity" : 1.0,
      "text-opacity" : 1.0,
      "border-color" : "data(fgcolor)",
      "width" : "data(width)",
      "content" : "data(name)",
      "background-color" : "data(bgcolor)",
      "height" : "data(height)"
    }
  }, {
    "selector" : "node[type = 'rectangle']",
    "css" : {
      "shape" : "rectangle"
    }
  }, {
    "selector" : "node[type = 'circle']",
    "css" : {
      "shape" : "ellipse"
    }
  }, {
    "selector" : "node[type = 'roundrectangle']",
    "css" : {
      "shape" : "roundrectangle"
    }
  }, {
    "selector" : "node:selected",
    "css" : {
      "background-color" : "rgb(255,255,0)"
    }
  }, {
    "selector" : "edge",
    "css" : {
      "source-arrow-shape" : "none",
      "font-size" : 10,
      "width" : 3.0,
      "font-family" : "Dialog.plain",
      "font-weight" : "normal",
      "target-arrow-color" : "rgb(0,0,0)",
      "color" : "rgb(0,0,0)",
      "content" : "",
      "text-opacity" : 1.0,
      "line-color" : "rgb(102,102,102)",
      "source-arrow-color" : "rgb(0,0,0)",
      "opacity" : 1.0,
      "line-style" : "solid",
      "target-arrow-shape" : "none"
    }
  }, {
    "selector" : "edge:selected",
    "css" : {
      "line-color" : "rgb(255,0,0)"
    }
  } ]
} ]

KEGG_GLOBAL_STYLE = [ {
  "format_version" : "1.0",
  "generated_by" : "cytoscape-3.7.1",
  "target_cytoscapejs_version" : "~2.1",
  "title" : "KEGG global style",
  "style" : [ {
    "selector" : "node",
    "css" : {
      "font-size" : 12,
      "shape" : "ellipse",
      "content" : "",
      "border-color" : "rgb(0,0,0)",
      "background-opacity" : 1.0,
      "text-opacity" : 1.0,
      "color" : "rgb(0,0,0)",
      "border-opacity" : 1.0,
      "text-valign" : "center",
      "text-halign" : "center",
      "border-width" : 2.0,
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "width" : "data(width)",
      "background-color" : "data(bgcolor)",
      "height" : "data(height)"
    }
  }, {
    "selector" : "node[type = 'circle']",
    "css" : {
      "shape" : "ellipse"
    }
  }, {
    "selector" : "node:selected",
    "css" : {
      "background-color" : "rgb(255,255,0)"
    }
  }, {
    "selector" : "edge",
    "css" : {
      "opacity" : 1.0,
      "line-style" : "solid",
      "source-arrow-shape" : "none",
      "font-size" : 10,
      "width" : 1.0,
      "text-opacity" : 1.0,
      "target-arrow-shape" : "none",
      "line-color" : "rgb(64,64,64)",
      "content" : "",
      "source-arrow-color" : "rgb(0,0,0)",
      "font-family" : "SansSerif.plain",
      "font-weight" : "normal",
      "color" : "rgb(0,0,0)",
      "target-arrow-color" : "rgb(0,0,0)"
    }
  }, {
    "selector" : "edge:selected",
    "css" : {
      "line-color" : "rgb(255,0,0)"
    }
  } ]
} ]

def global2cyjs(soup):
    #entries = soup.find_all('entry')
    nodes = []
    edges = []
    elements = {}
    compounds = soup.find_all('entry', attrs={"type": "compound"})
    reactions = soup.find_all('reaction')
    
    edgeid2gene = {}
    genes = soup.find_all('entry', attrs={'type': 'gene'})
    for gene in genes:
        edgeid2gene[gene['id']] = gene['name']

    for c in compounds:
        g = c.find("graphics")
        data = {}
        data['id'] = c['id']
        data['label'] = g['name']
        data['fgcolor'] = g['fgcolor']
        data['bgcolor'] = g['bgcolor']
        data['type'] = g['type']
        data['width'] = g['width']
        data['height'] = g['height']
        data['x'] = g['x']
        data['y'] = g['y']
        node = {'data':data, 'position':{'x':int(g['x']), 'y':int(g['y'])}, 'selected': 'false'}
        nodes.append(node)
    elements['nodes'] = nodes

    for r in reactions:
        substrates = r.find_all('substrate')
        products = r.find_all('product')
        edgeid = r['id']
        for s in substrates:
            for p in products:
                ed = {}
                ed['source'] = s['id']
                ed['target'] = p['id']
                ed['id'] = edgeid
                ed['genes'] = edgeid2gene[edgeid]
                edge = {'data':ed}
                edges.append(edge)
    # s2t_id = []
    # for r in reactions:
    #     substrates = r.find_all('substrate')
    #     products = r.find_all('product')
    #     rids = r["name"].replace("rn:", "")
    #     edgeid = r['id']
    #     # data = {}
    #     for s in substrates:
    #         for p in products:
    #             s2t_id.append([s['id'], p['id'], edgeid])
    #             # data['source'] = s['id']
    #             # data['target'] = p['id']
    #             # edge = {'data':data}
    #             # edges.append(edge)
    
    # for stid in set(frozenset(i) for i in s2t_id):
    #     data = {}
    #     data['source'] = list(stid)[0]
    #     data['target'] = list(stid)[1]
    #     data['genes'] = edgeid2gene[list(stid)[2]]
    #     edge = {'data':data}
    #     edges.append(edge)
    elements['edges'] = edges

    return elements
    # print(len(entries))
    # print(len(reactions))

def kegg2cyjs(identifier):
    kgml = requests.get(API_BASE + 'get/' + identifier + '/kgml').content
    soup = BeautifulSoup(kgml, "xml")
    if identifier[3:] in GLOBAL_PATHWAY_IDS:
        return global2cyjs(soup)
    
    entries = soup.find_all('entry')

    elements = {}
    nodes = []
    edges = []

    for e in entries:
        g = e.find("graphics")
        data = {}
        data["id"] = e["id"]
        data['keggids'] = e['name']
        data['keggtype'] = e['type']
        if e["type"] != "group":
            data["label"] = g["name"].split(", ")[0]
            data["name"] = g["name"]
        data["x"] = int(g["x"])
        data["y"] = int(g["y"])
        data["fgcolor"] = g["fgcolor"]
        data["bgcolor"] = g["bgcolor"]
        data["type"] = g["type"]
        data["width"] = g["width"]
        data["height"] = g["height"]
        node = {"data":data, "position":{"x":int(g["x"]), "y":int(g["y"])}, "selected":"false"}
        nodes.append(node)

    relations = soup.find_all('relation')
    s2t = []
    for rel in relations:
        stype = rel.find("subtype")
        # data1 = {}        
        # data1["source"] = stype["value"]
        # data1["target"] = rel["entry1"]
        s2t.append([stype["value"], rel["entry1"]])
        # data1["type"] = rel["type"]
        # edge = {"data":data1}
        # edges.append(edge)
        # data2 = {}
        # data2["source"] = stype["value"]
        # data2["target"] = rel["entry2"]
        s2t.append([stype["value"], rel["entry2"]])
        # edge = {"data":data2}
        # edges.append(edge)

    reactions = soup.find_all('reaction')
    for rea in reactions:
        substrates = rea.find_all('substrate')
        products = rea.find_all('product')
        for s in substrates:
            s2t.append([s['id'], rea['id']])
            for p in products:
                s2t.append([rea['id'], p['id']])
                # data = {}
                # data['source'] = s['id']
                # data['target'] = p['id']
                # edge = {'data': data}
                # edges.append(edge)

    for st in set(frozenset(i) for i in s2t):
        data = {}
        data['source'] = list(st)[0]
        data['target'] = list(st)[1]
        edge = {'data':data}
        edges.append(edge)

    elements["nodes"] = nodes
    elements["edges"] = edges
    return elements

def nodes2df(nodes):
    rows = []
    for n in nodes:
        rows.append(pd.Series(n['data']))
    return pd.DataFrame(rows)

def cyjs2file(cyjs, filename):
    d = {}
    d["elements"] = cyjs
    print(json.dumps(d, indent=4), file=open(filename,'w'))
    print("wrote " + filename)
    # return json.dumps(d, indent=4)