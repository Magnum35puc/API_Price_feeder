
# Asset Vision API Price Feeder

This project aims to regularly update asset price data in the AssetVIsion MongoDB Atlas through the dedicated RESTful FastAPI.

## Requirements

-   schedule
-   requests


## How to run the API

1.  Clone this repository to your local machine.
2.  Install the required packages by running `pip install -r requirements.txt`.
3. Setup your API Adress in `feed_crypto_prices.py` 
4.  Launch the Price feeder using the command `python feed_crypto_prices.py`.
    

## Price Data

The data comes from :

-  `For Cryptocurrencies`: The price data comes from CryptoCompare.

- `For others`: WIP.

## Security

The API uses JSON Web Tokens (JWT) for authentication.

## Database

The API uses MongoDB Atlas for storing its data.