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
                        pantable \
                        click==7.1.2 \
                        pandoc-acronyms; \
    apt-get purge -y --auto-remove python3-pip; \
    apt-get clean; \
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

ENV PATH="/usr/local/texlive/2023/bin/x86_64-linux:${PATH}"
WORKDIR /wrk

# Install latex packages
RUN tlmgr update --self && \
    tlmgr install \
        appendix \
        babel-german \
        beamer \
        booktabs \
        cantarell \
        caption \
        changebar \
        cm-super \
        collection-fontsrecommended \
        collection-xetex \
        csquotes \
        makeshape \
        multirow \
        environ \
        epstopdf \
        fancyvrb \
        float \
        flowchart \
        footmisc \
        fontaxes \
        fontspec \
        framed \
        latexdiff \
        latexmk \
        listings \
        preprint \
        sfmath \
        setspace \
        tabulary \
        tabu \
        tcolorbox \
        textpos \
        titlesec \
        todonotes \
        ulem \
        unicode-math \
        xltxtra

RUN tlmgr install fontspec

# install pandoc
RUN wget https://github.com/jgm/pandoc/releases/download/3.1.2/pandoc-3.1.2-1-amd64.deb; \
    dpkg -i pandoc-3.1.2-1-amd64.deb; \
    rm pandoc-3.1.2-1-amd64.deb

RUN git config --global safe.directory "/wrk"