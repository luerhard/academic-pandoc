import panflute as pf


def extract_institutions(author):
    if not isinstance(author, dict):
        return []
    name = next(iter(author.keys()))
    d = author[name]
    if not isinstance(d, dict):
        return []

    institutes = d.get("institute")
    if not institutes:
        return []
    elif isinstance(institutes, list):
        return institutes
    return [institutes]


def prepare(doc):
    authors = doc.get_metadata("authors")

    if not authors:
        author = doc.get_metadata("author")
        if author:
            authors = [author]
        else:
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

        # Happens if there is no colon after Author Name:
        if not isinstance(author, dict):
            a = {
                "name": author,
                "institute": False,
                "email": False,
                "correspondence": False,
            }
            new.append(a)
            continue

        name = next(iter(author.keys()))
        old = author[name]

        # get institutions
        if isinstance(author, dict):
            institutions = [short2ix[i] for i in extract_institutions(author)]
        else:
            institutions = False

        # get email address and correspondence if exists
        if isinstance(old, dict):
            email = old.get("email", False)
            correspondence = (
                True if (old.get("correspondence") in ["yes", "y", True]) else False
            )
        else:
            email = "None"
            correspondence = False

        # pack information together
        a = {
            "name": name,
            "institute": institutions,
            "email": email,
            "correspondence": correspondence,
        }
        new.append(a)

    # check for correspondences and how many
    if any(a["correspondence"] for a in new):
        correspondence = [
            {"name": author["name"], "email": author["email"]}
            for author in new
            if author["correspondence"] is True
        ]
        doc.metadata["correspondence"] = correspondence
        doc.metadata["multi_correspondence"] = (
            True if len(correspondence) > 1 else False
        )
    doc.metadata["authors"] = new

    new = []
    for short, ix in short2ix.items():
        i = {"index": ix, "name": ix2name[short] if institutes else short}
        new.append(i)

    doc.metadata["institutes"] = new


def action(elem, doc):
    pass


def main(doc=None):
    return pf.run_filter(action, prepare=prepare, doc=doc)


if __name__ == "__main__":
    main()
