FROM ubuntu:20.04

RUN apt-get update
RUN apt-get -y install python3 python3-pip
RUN pip3 install fastapi uvicorn pymongo
RUN apt -y install screen curl
WORKDIR /root
#RUN mkdir /var/run/sshd
RUN mkdir /root/project
#RUN mkdir -p /root/data/db
#RUN echo 'root:abcd' | chpasswd
#RUN sed -i 's/#*PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config

#RUN sed -i 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' /etc/pam.d/sshd

ENV NOTVISIBLE="in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

#EXPOSE 22
EXPOSE 80
#EXPOSE 27017
COPY *.py /root/
COPY *.json /root/
COPY requirements.txt /root
RUN pip3 install -r requirements.txt
#CMD ["/usr/sbin/sshd", "-D"]
#CMD uvicorn main:app --reload --port 80 --host 0.0.0.0
