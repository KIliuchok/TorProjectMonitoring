# TorProjectMonitoring

## Requirements

The named system requires additional software to be installed, and this section describes how to install it bit by bit.

The named software was developed and tested using the Ubuntu 21.10 and following instructions should work for any Debian System. For other Linux Distros, such as Arch, please refer to the specific installation guides directly from each software developer.

#### Grafana

Grafana is the backbone for the visualization of the data. Follow the following commands to install it to your system (Debian) from official grafana repository:

```
sudo apt update

sudo apt-get install -y gnupg2 curl software-properties-common
curl https://packages.grafana.com/gpg.key | sudo apt-key add -

sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"

sudo apt-get update
sudo apt-get -y install grafana
```

To start Grafana service:

```
sudo systemctl enable --now grafana-server
```

Note, you need to enable port 3000 on your firewall and router for the public access to this server from outside your network if necessary. Otherwise, the server will be hosted at http://localhost:3000.

Default credentials after installation are:
Username: admin
Password: admin.

You will be prompted to change your admin password with first time login.

#### PostgreSQL

PostgreSQL is the database for the data storage and quering.

To install:

```
sudo apt update

sudo apt install postgresql
```

To run:

```
sudo systemctl start postgresql.service
```

For easier management of your database you might want to install such utility as DBeaver (https://dbeaver.io/) for easier management of your postgresql db.

#### Tor, and other Tor Utilities

This repository contains fork of OnionPerf from [Onionperf Repository](https://github.com/torproject/onionperf), and it requires installed Tor and TGen.

Onionperf requires the path to Tor and TGen binaries, which you supply in command line.

To install Tor:

```
sudo apt install tor
```

To install TGen:

```
sudo apt install cmake libglib2.0-dev libigraph0-dev make
cd ~/
git clone https://github.com/shadow/tgen.git
cd tgen/
mkdir build
cd build/
cmake ..
make
```

To install OnionPerf:

```
cd onionperf/
source /venv/bin/activate
sudo python3 setup.py install
cd ~/
```

For any additional information, refer to [OnionPerf Repository](https://github.com/torproject/onionperf).


To install stem library for your system:

```
sudo pip install stem
```


Additional, Python3 Libraries:

```
sudo pip install psycopg2 
```


## Setup PostgreSQL

The following is the dump of the schema for the postgres DB, which is named postgres and is default database created after installation. To recreate such just run the following dump in the terminal, when connected to the db:

<details><summary>Click for whole DB schema dump</summary>
<p>

```
--
-- PostgreSQL database dump
--

-- Dumped from database version 14.2 (Ubuntu 14.2-1.pgdg21.10+1)
-- Dumped by pg_dump version 14.2 (Ubuntu 14.2-1.pgdg21.10+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: tor-statistics; Type: SCHEMA; Schema: -; Owner: kostia
--

CREATE SCHEMA "tor-statistics";


ALTER SCHEMA "tor-statistics" OWNER TO kostia;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: hourly_sensus; Type: TABLE; Schema: tor-statistics; Owner: kostia
--

CREATE TABLE "tor-statistics".hourly_sensus (
    date date,
    relay_fingerprint numeric,
    measured_bandwith numeric,
    measured_bandwidth_vote numeric,
    advertized_bandwidth numeric
);


ALTER TABLE "tor-statistics".hourly_sensus OWNER TO kostia;

--
-- Name: hourly_sensus_avg; Type: TABLE; Schema: tor-statistics; Owner: kostia
--

CREATE TABLE "tor-statistics".hourly_sensus_avg (
    date date,
    advertised_bandwidth_avg numeric,
    measured_bandwidth numeric,
    number_of_available_relays numeric,
    number_of_available_bridges numeric
);


ALTER TABLE "tor-statistics".hourly_sensus_avg OWNER TO kostia;

--
-- Name: onionperf_daily_additional; Type: TABLE; Schema: tor-statistics; Owner: kostia
--

CREATE TABLE "tor-statistics".onionperf_daily_additional (
    date date NOT NULL,
    circuit_build_time numeric,
    number_of_measurements numeric,
    number_of_failures numeric,
    server_origin character varying
);


ALTER TABLE "tor-statistics".onionperf_daily_additional OWNER TO kostia;

--
-- Name: onionperf_data; Type: TABLE; Schema: tor-statistics; Owner: kostia
--

CREATE TABLE "tor-statistics".onionperf_data (
    id character varying NOT NULL,
    label character varying,
    filesize_bytes numeric,
    error_code character varying,
    server character varying,
    time_to_first_byte numeric,
    time_to_last_byte numeric,
    mbps numeric,
    start timestamp without time zone NOT NULL,
    origin_server character varying
);


ALTER TABLE "tor-statistics".onionperf_data OWNER TO kostia;

--
-- Name: relays_and_bridges; Type: TABLE; Schema: tor-statistics; Owner: kostia
--

CREATE TABLE "tor-statistics".relays_and_bridges (
    date date NOT NULL,
    version character varying,
    relays_number_for_version numeric,
    bsd numeric,
    linux numeric,
    macos numeric,
    other numeric,
    windows numeric,
    announced_ipv6_relays numeric,
    exiting_ipv6_relays numeric,
    reachable_ipv6_relays numeric,
    avg_relays numeric,
    avg_bridges numeric,
    announced_ipv6_bridges numeric
);


ALTER TABLE "tor-statistics".relays_and_bridges OWNER TO kostia;

--
-- Name: user_statistics; Type: TABLE; Schema: tor-statistics; Owner: kostia
--

CREATE TABLE "tor-statistics".user_statistics (
    date date NOT NULL,
    country_id character varying(50) NOT NULL,
    user_estimate integer,
    lower_user_estimate character varying(50),
    upper_user_estimate character varying(50),
    fraction_of_relays_for_estimate integer
);


ALTER TABLE "tor-statistics".user_statistics OWNER TO kostia;

--
-- Name: onionperf_daily_additional onionperf_daily_additional_pk; Type: CONSTRAINT; Schema: tor-statistics; Owner: kostia
--

ALTER TABLE ONLY "tor-statistics".onionperf_daily_additional
    ADD CONSTRAINT onionperf_daily_additional_pk PRIMARY KEY (date);


--
-- Name: onionperf_data onionperf_data_pk; Type: CONSTRAINT; Schema: tor-statistics; Owner: kostia
--

ALTER TABLE ONLY "tor-statistics".onionperf_data
    ADD CONSTRAINT onionperf_data_pk PRIMARY KEY (start, id);


--
-- Name: relays_and_bridges relays_additional_information_pk; Type: CONSTRAINT; Schema: tor-statistics; Owner: kostia
--

ALTER TABLE ONLY "tor-statistics".relays_and_bridges
    ADD CONSTRAINT relays_additional_information_pk PRIMARY KEY (date);


--
-- Name: user_statistics user_statistics_pk; Type: CONSTRAINT; Schema: tor-statistics; Owner: kostia
--

ALTER TABLE ONLY "tor-statistics".user_statistics
    ADD CONSTRAINT user_statistics_pk PRIMARY KEY (date, country_id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON SCHEMA public TO kostia;


--
-- PostgreSQL database dump complete
--
```
</p>
</details>


## Import Grafana Dashboard

From your grafana dashboard after setting up postgresql, import the grafana dashboard from provided JSON project-1651137476215.json

## Run scheduler

The scheduler will update the data every day when the new data is published on the network. Additionally, db_operations script contains additional functions to import data standalone.



