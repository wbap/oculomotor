# oculomotor
WBAI 2018 Hackathon Oculomotor Project Repository.

## Usage

### 1. Install Docker
[How to install](https://docs.docker.com/install/)

After successfull install, you should be able to run `docker ps` and get something like this:

```
$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

### 2. Clone this repository.
```
$ git clone --recursive https://github.com/wbap/oculomotor
```

### 3. Build the docker image.
```
$ cd oculomotor
$ docker build -t wbap/oculomotor .
```

### 4. Edit the files under `appliation/functions`.

### 5. Run the docker image.
```
$ ./helpers/run_app.sh
```

### 6. Open web page in a browser

[http://0.0.0.0:5000/](http://0.0.0.0:5000/) : Simple environment run

[http://0.0.0.0:5000/inspector](http://0.0.0.0:5000/inspector) : Inspector mode

![screenshot](./doc/images/screenshot0.png)
