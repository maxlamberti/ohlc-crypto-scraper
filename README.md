# Serverless Crypto Data Scraper
![python version](https://img.shields.io/badge/python-3.6-blue.svg)

Create an event schedule to scrape OHLC cryptocurrency data from a public exchange API (here implemented with [Kraken API](https://www.kraken.com/help/api)) and insert it into your private database. The scraper is hosted serverless on AWS Lambda making it virtually free to run.

## Tech

- [Zappa](https://github.com/Miserlou/Zappa) - deploy Python Lambdas and schedule events
- [krakenex](https://github.com/veox/python3-krakenex) - API for Kraken exchange
- [AWS Lambda](https://aws.amazon.com/lambda/) - serverless compute service
- [AWS RDS](https://aws.amazon.com/rds/) - relational database service

## Installation and Setup

### Clone
Clone this repo to your local machine. 
```
$ git clone https://github.com/hexamax/ohlc-crypto-scraper.git
```

### Install Requirements
Zappa requires an active [virtual environment](https://virtualenv.pypa.io/en/latest/installation/) to deploy. Either install and activate your own virtual environment or execute the following steps.
```
$ cd ohlc-crypto-scraper
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### Configure Database
Get your database credentials and write them into the corresponding fields of the database configuration file located at `ohlc-crypto-scraper/db_config.py`

**WARNING**: The scraper was written, used and tested for a PostgreSQL database instance only. For compatability make sure to be running a Postgres instance as well. To set up a low cost RDS Postgres instance on AWS check out this [tutorial](https://aws.amazon.com/getting-started/tutorials/create-connect-postgresql-db/).

### (Optional) Zappa Settings
The `zappa_settings.json` file was initialized with some sensible defaults and will run fine without additional manipulation. However, here are some easy changes you can make to customize your deploy:
- Specify the rate at which the data scraping event is executed by changing the [rate expression](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html#RateExpressions) located in `zappa_settings.json > events > expression`.
- Specify the [aws region](https://docs.aws.amazon.com/general/latest/gr/rande.html) of your deploy in the `aws_region` field.
- Specif a custome name for your S3 bucket  using the `s3_bucket` field.

## Deploy and Schedule

### Initial Deploy
Use the following command for the initial deploy only.
```
$ zappa deploy scrape_event
```
Zappa will spit out the deployment information to your terminal and let you know if the deploy was succesfull. If the deploy was succesfull your data scraper should now be up and running.

### Schedule
If you decided to update the rate expression in the `zappa_settings.json` file you can easily reschedule your scraper.
```
$ zappa schedule scrape_event
```

### Undeploy
This will remove the scheduled Lambda function.
```
$ zappa undeploy scrape_event
```

## Logs
You can monitor your scraper's AWS CloudWatch logs directly from the console.
```
$ zappa tail scrape_event
```
