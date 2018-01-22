### Cassandra setup

This setup assumes you have a local instance of cassandra running. In case you are connecting to a remote node(s), you can change the hosts in `store.py`.

#### Note: You can spin a cassandra container via `docker-compose up -d cassandra`.

### Getting Started

#### Required Dependencies

* [cassandra driver](https://github.com/datastax/python-driver)

#### Setup

Copy all the computed `.dmp` files in this directory. All pre-snapshots dbs can be found [here](http://store.alon-e.com/IOTA_DBs).


```
python store.py
```
