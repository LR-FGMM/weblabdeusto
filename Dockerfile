FROM debian
WORKDIR /weblabdeusto
RUN apt-get update && \
    apt-get install -y git && \
    apt-get install -y python &&\
    apt-get install -y python-pip &&\
    apt-get install -y virtualenv
RUN virtualenv weblab_env
RUN . weblab_env/bin/activate
COPY . .
RUN python -m pip install .
#RUN weblab-admin httpd-config-generate sample
CMD ["weblab-admin", "start" ,"sample"]