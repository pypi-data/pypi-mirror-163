# REaccess

Execute commands on another machine remotely and get the response in real time.

Install `reaccess` using pip:

```
pip install reaccess
```

## How to use

Use the `reaccess` command to start the command line interface. You will have 2 arguments available, `server` to start a server and `client` to connect to a server.

You can also set the host and port using the `--host` and `--port` flags. If not specified, the host `localhost` and port `2808` will be the default. See a example to server:

```
reaccess server --host 127.0.0.1 --port 5000
```

## License

```
Apache License
Copyright 2022 Jaedson Silva
```

See and follow the **complete license** at [LICENSE](https://github.com/jaedsonpys/reaccess/blob/master/LICENSE).