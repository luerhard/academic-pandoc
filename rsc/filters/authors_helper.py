from collections import OrderedDict

import panflute as pf

def extract_institutions(author):
    name = next(iter(author.keys()))
    d = author[name]
    if not isinstance(d["institute"], list):
        return [d["institute"]]
    return d["institute"]


def prepare(doc):
    authors = doc.get_metadata("authors")
    if not authors:
        return
    institutes = doc.get_metadata("institutes")
    insts = []
    for author in authors:
        author_inst = extract_institutions(author)
        for inst in author_inst:
            if inst not in insts:
                insts.append(inst)

    short2ix = dict(zip(insts, range(1, len(insts) + 1)))
    if institutes:
        ix2name = {ix: institutes.get(ix) for ix in short2ix}

    new = []
    for author in authors:
        name = next(iter(author.keys()))
        old = author[name]
        a = {
            "name": name,
            "institute": [short2ix[i] for i in extract_institutions(author)],
            "email": old.get("email"),
            "correspondence": True if (old.get("correspondence") == "yes") else False,
        }
        new.append(a)
    if any(a["correspondence"] for a in new):
        doc.metadata["correspondence"] = True
    doc.metadata["authors"] = new

    new = []
    for short, ix in short2ix.items():
        i = {
            "index": ix,
            "name": ix2name[short] if institutes else short
        }
        new.append(i)

    doc.metadata["institute"] = new


def action(elem, doc):
    pass


def main(doc=None):
    return pf.run_filter(action, prepare=prepare, doc=doc)


if __name__ == "__main__":
    main()
