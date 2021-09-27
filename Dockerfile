FROM debian:latest

WORKDIR /root

COPY setup.sh /root

# package install
RUN apt-get update
RUN apt-get install -y wget \
                       tar \
                       gcc \
                       make \
                       bzip2 \
                       python3 \
                       python3-pip \
                       fonts-migmix \
                       fontconfig \
                       unzip \
                       graphviz \
                       vim \
                       curl \
                       git

# CRF install
RUN wget -O CRF++-0.58.tar.gz 'https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7QVR6VXJ5dWExSTQ' && \
    tar xvzf CRF++-0.58.tar.gz && \
    cd CRF++-0.58 && \
    ./configure --with-charset=utf-8 --enable-utf8-only && \
    make && \
    make install

# mecab install
RUN wget -O mecab-0.996.tar.gz 'https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7cENtOXlicTFaRUE' && \
    tar xvzf mecab-0.996.tar.gz && \
    cd mecab-0.996 && \
    ./configure && \
    make && \
    make check && \
    make install && \
    cd ../ && \
    ldconfig && \
    wget -O mecab-ipadic-2.7.0-20070801.tar.gz 'https://drive.google.com/uc?export=download&id=0B4y35FiV1wh7MWVlSDBCSXZMTXM' && \
    tar xvzf mecab-ipadic-2.7.0-20070801.tar.gz && \
    cd mecab-ipadic-2.7.0-20070801 && \
    ./configure --with-charset=utf-8 --enable-utf8-only && \
    make && \
    make install

# word2vec install
RUN curl -O http://www.cl.ecei.tohoku.ac.jp/~m-suzuki/jawiki_vector/data/20170201.tar.bz2 && \
    tar -jxvf 20170201.tar.bz2

RUN mkdir -p /root/chatBot

COPY . /root/chatBot

RUN mkdir -p /root/chatBot/word2vec_model && \
    cp entity_vector/entity_vector.model.bin chatBot/word2vec_model

# python lib
RUN pip install requests \
                matplotlib \
                graphviz \
                pandas \
                gensim \
                mecab-python3 \
                beautifulsoup4 \
                pycodestyle

CMD /bin/bash setup.sh
