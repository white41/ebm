# Email Based Middleware (EBM)

**EBM** is a middleware to abstract a client application from communication. Given an email server, a client email address on this server and an **EBM** server email address the client can forget the way its application communicates with the world and focus on coding its logic.

## Getting Started

Our middleware has a client library and a server script, fully written in python. We provide a [Flask](flask link) client application as proof of correctness.

### Prerequisites

* [Python 3.6](https://www.python.org) - The specific version used for this project
* [imbox>=0.9.6](https://github.com/martinrusev/imbox) - IMAP client for humans.

### Installation

First clone the project from [github](https://github.com/white41/ebm):

```bash
$ git clone https://github.com/white41/ebm
```

Now install from source:

```bash
$ cd ebm/ebmc && python3 setup.py install
```

## Usage

You can install our middleware client **ebmc** or start a server of our middleware **ebms**.

### Server

Our server application is fully [dockerized](https://www.docker.com), but you can run it from source.

On a side note, our server uses [python-fire](https://github.com/google/python-fire) for ease of use. The possible uses can be seen in the arguments of the `main` function inside `server.py` file.

#### Source

First, we must install our server requirements:

  * [Python 3.6](https://www.python.org) - The specific version used for this project
  * [imbox>=0.9.6](https://github.com/martinrusev/imbox) - IMAP client for humans.
  * [rpyc=4.0.2](https://rpyc.readthedocs.io/en/latest) - Remote Python Call
  * [python-fire](https://github.com/google/python-fire) - Python Fire is a library for automatically generating command line interfaces (CLIs) from absolutely any Python object.

Then, enter our source directory **src** and run our `server.py` script with the appropriate arguments.

```bash
$ cd ebm/src
$ ./server.py --server-email-addr="ebms@estudiantes.matcom.uh.cu" \
            --pwd="password" \
            --email-server="correo.estudiantes.matcom.uh.cu" \
            --ip-addr="('10.6.98.203', 18861)" \
            --join-addr="('10.6.98.3', 18861)"
```

This will start a new server joining our distributed [chord](https://en.wikipedia.org/wiki/Chord_(peer-to-peer)) system in the address `--join-addr="('10.6.98.3', 18861)"`, in case of not setting the `--join-addr` argument the server assumes it itself is the first **chord** node.

`--ip-addr` is this server's transport layer address, which is needed in case of running the [docker](https://www.docker.com) image, if not you can omit this argument, the server will set its address correctly, further explained in our [article](https://github.com/white41/ebm/blob/master/article/article.pdf).

`--server-email-addr` and `--pwd` refer to the client account our server will use to connect to `--email-server`.

#### Docker

With a shell prompt in our project's root path, we simply run:

```bash
$ sudo docker build -t ebms:latest .
```

Thus, building our image requirements as shown inside our [Dockerfile](https://github.com/white41/ebm/blob/master/Dockerfile). Afterwards, let's start our container with any given port binding (which we'll have to remember).

```bash
$ sudo docker run -d -p PORT:PORT --name ebms ebms:latest python3.6 \
                  /usr/ebm/server.py
                  --server-email-addr="ebms@estudiantes.matcom.uh.cu" \
                  --pwd="password" \
                  --email-server="correo.estudiantes.matcom.uh.cu" \
                  --ip-addr="('10.6.98.203', PORT)" \
                  --join-addr="('10.6.98.3', PORT)"
```

Starting our server instance which is equivalent to the *Source* section instance.

If we want to see what our server logs, we can run:

```bash
$ sudo docker logs -f ebms
```

This shows that putting our server in development is really straight-forward and that we can have potentially infinite ;) instances in the same host, in the same docker daemon or in as many hosts as we want, scaling horizontally with ease.

### Client

After installation our client can be imported as any other python library. Using an `EBMC` as transport layer.

```python
import ebmc
ebm = ebmc.EBMC('user_client','s@g.com','server.com','pwd')
ebm.register('user','pwd')
ebm.login('user','pwd')
ebm.send('another_user', 'data to send', 'name of the package')
```

### Sender-app

We provide a flask application for testing purposes which basically just send files between clients. It is also fully dockerized, just need to run from the `sender-app` folder:

```bash
$ sudo cd sender-app
$ sudo docker build -t sender-app:latest .
```

And then, just run the new container with:

```bash
$ docker run -d -p 5000:5000 sender-app:latest
```

## Authors

* Alexander Gonzalez - **a.fertel@estudiantes.matcom.uh.cu**
* Sandor Martin - **s.martin@estudiantes.matcom.uh.cu**
