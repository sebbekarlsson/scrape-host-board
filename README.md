# scrape.host
> Scraper hosting service

# Development server
> How to start the development server

> First make sure you have the following installed:

* [Ruby gem sass](http://sass-lang.com/install)
* [Python 2.7](https://www.python.org/download/releases/2.7/)
* [python-virtualenv](https://virtualenv.pypa.io/en/stable/installation/)
* [MongoDB](https://docs.mongodb.com/manual/installation/)

## Follow these steps to get started:

### Create the config file

    cp config.example.json config.json

> Edit `config.json` to match your settings.

### Create a virtualenv

    virtualenv -p /usr/bin/python2.7 ./venv

> This will create a virtualenv inside a `venv` directory.

### Source the virtualenv

    source ./venv/bin/activate

> You are now using the virtualenv.

### Install scrape.host

    python setup.py develop

> Depending on your operating system, you might have to execute the command
> above multiple times.

### Start MongoDB

    mongod

> Make sure MongoDB is running

### Start the web server

    python web.py

> The web application should now be available at `http://localhost:5000`

### Start the scraping service

    python scrapehost/scraping

> The scraping service should now be running.

# Unit tests
> First make sure you have sourced the `venv` (python-virtualenv) and executed
> `setup.py`

> Then run:

    pytest .

> This will run all tests
