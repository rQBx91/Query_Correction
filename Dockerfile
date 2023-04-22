FROM python:3.10
WORKDIR /app
ADD requirements.txt ./
ADD *.py ./
ADD /resources ./resources
EXPOSE 80
ENV PIP_ROOT_USER_ACTION=ignore
RUN pip3 install -r requirements.txt
CMD ["python", "server.py"] 
