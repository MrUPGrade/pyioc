FROM mrupgrade/docker-deadsnakes-bundle-dev

MAINTAINER MrUPGrade itsupgradetime@gmail.com


COPY . /code/

RUN cd /code && \
    pip2.6 install --upgrade -e .[test] && \
    pip2.7 install --upgrade -e .[test] && \
    pip3.3 install --upgrade -e .[test] && \
    pip3.4 install --upgrade -e .[test] && \
    pip3.5 install --upgrade -e .[test] && \
    rm -Rf /code/


COPY docker/pyioc_test/docker-entrypoint.sh /

ENTRYPOINT ["/docker-entrypoint.sh"]

VOLUME /code
WORKDIR /code

