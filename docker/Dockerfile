FROM ubuntu:hirsute
MAINTAINER Lukas Erhard <luerhard@googlemail.com>
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -q; \
    apt-get install -qy build-essential wget libfontconfig1 git latexdiff python3 python3-pip python-is-python3; \
    rm -rf /var/lib/apt/lists/*

# Install TexLive with scheme-basic
RUN wget http://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz; \
	mkdir /install-tl-unx; \
	tar -xvf install-tl-unx.tar.gz -C /install-tl-unx --strip-components=1; \
    echo "selected_scheme scheme-basic" >> /install-tl-unx/texlive.profile; \
	/install-tl-unx/install-tl -profile /install-tl-unx/texlive.profile; \
    rm -r /install-tl-unx; \
	rm install-tl-unx.tar.gz

ENV PATH="/usr/local/texlive/2021/bin/x86_64-linux:${PATH}"

RUN pip install --no-cache panflute \
        pandoc-fignos \
        pandoc-secnos

RUN wget https://github.com/jgm/pandoc/releases/download/2.16/pandoc-2.16-1-amd64.deb; \
    dpkg -i pandoc-2.16-1-amd64.deb; \
    rm pandoc-2.16-1-amd64.deb
    

# Install latex packages
RUN tlmgr update --self && \
    tlmgr install \
        appendix \
        booktabs \
        caption \
        cm-super \
        csquotes \
        float \
        latexmk \
        preprint \
        setspace \
        tabulary \
        todonotes \
        ulem    


ENTRYPOINT ["docker/entrypoint.sh"]
