FROM bitnami/minideb:latest
MAINTAINER Lukas Erhard <luerhard@googlemail.com>

RUN apt-get update -q; \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -qq git \
                        wget \
                        libfontconfig1 \
                        python3-pip; \
    rm -rf /var/lib/apt/lists/*
    
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 100; \
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 100

RUN pip install --no-cache panflute \
                        pandoc-fignos \
                        pandoc-secnos
                            
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
        booktabs \
        caption \
        cm-super \
        csquotes \
        float \
        latexdiff \
        latexmk \
        listings \
        preprint \
        setspace \
        tabulary \
        todonotes \
        ulem
        
ENTRYPOINT ["docker/entrypoint.sh"]
