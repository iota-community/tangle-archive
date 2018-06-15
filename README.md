# Tangle-Archive

## Required Dependencies

- python >= 2.7
- [Docker](https://docs.docker.com/engine/installation/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

### Development setup

Clone the repository from the command line by entering:

```
git clone https://gitlab.com/iota-healthcare/permanode
```

Once you configure all of the required dependencies and clone the source code, you are ready to begin working with the API. Type the following command to start the API server on port `9080`.

```
docker-compose up -d
```

### Contribution guidelines

Make sure you run [flake8](http://flake8.pycqa.org/en/latest/) to check for linting errors before submitting a pull request.

### Troubleshooting

Make sure that *CASSANDRA_HOSTS* is set to the correct address in the `config.py` file.
