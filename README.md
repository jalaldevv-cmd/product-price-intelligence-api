# Product Price Intelligence API

A Python application that monitors prices of products over time.

It uses Playwright to scrape a JavaScript-rendered website, Pandas to clean the data, PostgreSQL to store the price history, and FastAPI to provide the data through a REST API.

## Live Demo

https://product-price-intelligence-api.onrender.com/docs

## How It Works

```text
Website
   ↓
Playwright
   ↓
Pandas
   ↓
PostgreSQL
   ↑
FastAPI
   ↑
Client
```

A scheduled GitHub Actions workflow fetches the current prices on a daily basis.

## API

`GET /products` — get a list of products

`GET /products/{product_id}/prices` — get price history

`GET /products/{product_id}/change` — get latest price change and percentage change

## Database

Prices are stored separately from the product information so each product is only stored once while also keeping multiple historical price records.

## Testing

Unit and API tests run using pytest with a separate PostgreSQL test database. The tests run automatically through GitHub Actions when new changes are pushed.

```bash
python -m pytest -v
```

## Built With

Python · FastAPI · PostgreSQL · Playwright · Pandas · Pydantic · pytest · Docker · GitHub Actions · Render

## What I Learned

This project combined scraping, data processing, databases, APIs, testing, Docker, CI, automation, and deployment in one solution.