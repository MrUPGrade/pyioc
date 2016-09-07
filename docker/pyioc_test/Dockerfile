FROM mrupgrade/docker-deadsnakes-bundle-dev

MAINTAINER MrUPGrade itsupgradetime@gmail.com

COPY requirements.txt /

RUN pip2.6 install --upgrade -r requirements.txt && \
    pip2.7 install --upgrade -r requirements.txt && \
    pip3.3 install --upgrade -r requirements.txt && \
    pip3.4 install --upgrade -r requirements.txt && \
    pip3.5 install --upgrade -r requirements.txt && \
    rm -Rf requirements.txt

COPY docker/pyioc_test/docker-entrypoint.sh /

ENTRYPOINT ["/docker-entrypoint.sh"]

VOLUME /code
WORKDIR /code
