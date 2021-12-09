FROM bitnami/minideb:latest

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -q; \
    apt-get install -y git \
                        wget \
                        libfontconfig1 \
                        python3 \
                        make \
                        ghostscript \
                        python3-pip; \
    pip3 install --no-cache panflute \
                        pandoc-fignos \
                        pandoc-secnos; \
    apt-get purge -y --auto-remove python3-pip; \
    rm -rf /var/lib/apt/lists/*
    
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 100

# Install TexLive with scheme-basic
RUN wget https://mirror.clientvps.com/CTAN/systems/texlive/tlnet/install-tl-unx.tar.gz; \
    mkdir /install-tl-unx; \
    tar -xvf install-tl-unx.tar.gz -C /install-tl-unx --strip-components=1; \
    echo "selected_scheme scheme-basic" >> /install-tl-unx/texlive.profile; \
    echo "tlpdbopt_autobackup 0" >> /install-tl-unx/texlive.profile; \
    echo "tlpdbopt_install_docfiles 0" >> /install-tl-unx/texlive.profile; \
    echo "tlpdbopt_install_srcfiles 0" >> /install-tl-unx/texlive.profile; \
    /install-tl-unx/install-tl -profile /install-tl-unx/texlive.profile; \
    rm -r /install-tl-unx; \
    rm install-tl-unx.tar.gz

ENV PATH="/usr/local/texlive/2021/bin/x86_64-linux:${PATH}"

# install pandoc
RUN wget https://github.com/jgm/pandoc/releases/download/2.16.1/pandoc-2.16.1-1-amd64.deb; \
    dpkg -i pandoc-2.16.1-1-amd64.deb; \
    rm pandoc-2.16.1-1-amd64.deb
    
WORKDIR /wrk

# Install latex packages
RUN tlmgr update --self && \
    tlmgr install \
        appendix \
        beamer \
        booktabs \
        caption \
        cm-super \
        collection-fontsrecommended \
        csquotes \
        makeshape \
        epstopdf \
        float \
        flowchart \
        latexdiff \
        latexmk \
        listings \
        preprint \
        sfmath \
        setspace \
        tabulary \
        textpos \
        todonotes \
        ulem
        
ENTRYPOINT ["docker/entrypoint.sh"]
