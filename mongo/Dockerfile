FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get -y install python3 python3-pip wget
RUN pip3 install pymongo
#RUN apt -y install screen curl
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add -
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list
RUN apt-get update
RUN apt-get install -y mongodb-org
WORKDIR /root
#RUN mkdir /var/run/sshd
RUN mkdir /root/project
RUN mkdir -p /root/data/db
#RUN echo 'root:abcd' | chpasswd
#RUN sed -i 's/#*PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config

#RUN sed -i 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' /etc/pam.d/sshd

ENV NOTVISIBLE="in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

#EXPOSE 22
#EXPOSE 80
#EXPOSE 27017
#COPY *.py /root/
#COPY *.json /root/
#COPY requirements.txt /root
#CMD ["/usr/sbin/sshd", "-D"]
#CMD mongod --dbpath /data/db --bind_ip 0.0.0.0
