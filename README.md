# Information Retrival Project: Query Correction

A simple and fairly accurate query correction system for persian language built using wikipedia farsi [data](https://dumps.wikimedia.org/fawiki/) writen in Python.

Project done as part of Information Retrival course at Urmia University.

Extract resource files:
```bash
tar xvf resources.tar.xz --directory=./resources
```

Run docker version:
```bash
sudo docker pull rqbx91/query-correction:latest
sudo docker run -d -p 80:80 rqbx91/query-correction:latest
```

Build docker image:
```bash
sudo docker build -t query-correction:latest .
sudo docker run -d -p 80:80 query-correction:latest
```

Server is now running on [localhost](http://localhost:80). (Building Index may take a few minutes)