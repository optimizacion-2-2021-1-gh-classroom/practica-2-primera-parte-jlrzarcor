#dummy line
FROM ubuntu:bionic

ENV JUPYTERLAB_VERSION 3.0.0
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

ENV DEB_PACKAGES="sudo nano less git python3-dev python3-pip python3-setuptools"
ENV KALE_VERSION="kubeflow-kale==0.6.1"

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive && echo "America/Mexico_City" > /etc/timezone && apt-get install -y tzdata

RUN apt-get update && apt-get install -y $DEB_PACKAGES && pip3 install --upgrade pip

RUN apt-get install -y curl
#RUN apt-get install nodejs
#RUN apt-get install -y npm
RUN curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash - && apt-get install -y nodejs
RUN groupadd miuser
RUN useradd miuser -g miuser -m -s /bin/bash
RUN echo 'miuser ALL=(ALL:ALL) NOPASSWD:ALL' | (EDITOR='tee -a' visudo)
RUN echo 'miuser:qwerty' | chpasswd
#RUN pip3 install absl-py
#RUN pip3 install nbformat
RUN pip3 install jupyter "jupyterlab>=2.0.0,<3.0.0" --upgrade
RUN pip3 install $KALE_VERSION --upgrade
#RUN pip3 install --upgrade kubeflow-kale 
RUN jupyter labextension install kubeflow-kale-labextension



USER miuser
#Github proyect
#RUN git clone https://github.com/optimizacion-2-2021-1-gh-classroom/practica-1-segunda-parte-jlrzarcor.git
#COPY OA_logreg/requirements.txt requirements.txt


#COPY requirements.txt .

RUN pip3 install numpy pandas
COPY requirements.txt .
RUN pip3 install -r requirements.txt

#Nuestro paquete
RUN pip3 install oae5

#COPY . /tmp/
#COPY --from=intermediate ./practica-1-segunda-parte-jlrzarcor/requirements.txt requirements.txt
#RUN pip3 install -r requirements.txt  
#RUN cat requirements.txt  
#RUN pip3 install numpy==1.19.5 pandas==1.2.0 scipy==1.6.0 cvxpy==1.1.7 sklearn pytest==6.2.1 


RUN jupyter notebook --generate-config && sed -i "s/#c.NotebookApp.password = .*/c.NotebookApp.password = u'sha1:115e429a919f:21911277af52f3e7a8b59380804140d9ef3e2380'/" /home/miuser/.jupyter/jupyter_notebook_config.py

#ENTRYPOINT ["/usr/local/bin/jupyter", "lab", "--ip=0.0.0.0", "--no-browser"]

#https://docs.docker.com/engine/reference/builder/ 

VOLUME ["/shared_volume"]
WORKDIR /
ENV NB_PREFIX  Opt_HC_CG

ENTRYPOINT ["/usr/local/bin/jupyter", "lab", "--ip=0.0.0.0", "--no-browser", "--allow-root", "--LabApp.allow_origin='*'", "--LabApp.base_url="Opt_HC_CG"]


