# ByeByePii

[![PyPI Latest Release](https://img.shields.io/pypi/v/ByeByePii.svg)](https://pypi.org/project/ByeByePii/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## What is it?

**ByeByePii** is a Python package that is meant for hashing personal identifiable information (PII). It was built focused on making Data Lakes storing JSON files GDPR compliant.

## Main Features
  - Analyzing Python Dictionaries in order to identify PII
  - Hashing PII in a given Python Dictionary

## Where to get it
The source code is currently hosted on GitHub at:
https://github.com/falkzeh/ByeByePii

Binary installers for the latest released version are available at the [Python
Package Index (PyPI)](https://pypi.org/project/ByeByePii).

```sh
pip install ByeByePii
```

## Documentation

#### Analyzing a Python Dictionary and creating a list of keys to hash
In order to not having to manually look for all the keys in a Python Dictionary, we can use the `analyzeDict` function.

```python
import byebyepii
import json

if __name__ == '__main__':

    # Loading local JSON file
    with open('data.json') as json_file:
        data = json.load(json_file)

    # Analyzing the dictionary and creating our hash list
    key_list, subkey_list = byebyepii.analyzeDict(data)
```

```sh
$ python3 analyzeDict.py

Add BuyerInfo - BuyerEmail to hash list? (y/n) y
Add SalesChannel to hash list? (y/n) n
Add OrderStatus to hash list? (y/n) n
Add PurchaseDate to hash list? (y/n) n
Add ShippingAddress - StateOrRegion to hash list? (y/n) y
Add ShippingAddress - PostalCode to hash list? (y/n) y
Add ShippingAddress - City to hash list? (y/n) n
Add ShippingAddress - CountryCode to hash list? (y/n) n
Add LastUpdateDate to hash list? (y/n) n

Keys to hash: ['BuyerInfo', 'ShippingAddress', 'ShippingAddress', 'ShippingAddress', 'ShippingAddress']
Subkeys to hash: ['BuyerEmail', 'StateOrRegion', 'PostalCode']
```

#### Hashing PII in a given Python Dictionary
Using the key lists we just created we can proceed to hash the PII in the dictionary.

```python
import byebyepii
import json

if __name__ == '__main__':

    # Loading local JSON file
    with open('data.json') as json_file:
        data = json.load(json_file)

    # Hasing the PII
    keys_to_hash = ['BuyerInfo', 'ShippingAddress', 'ShippingAddress', 'ShippingAddress', 'ShippingAddress']
    subkeys_to_hash = ['BuyerEmail', 'StateOrRegion', 'PostalCode']
    hashed_pii = byebyepii.hashPii(data, keys_to_hash, subkeys_to_hash)

    # Writing the updated JSON file
    with open('hashed_data.json', 'w') as outfile:
        json.dump(hashed_pii, outfile)
```

Before:
```json
{
  "BuyerInfo": {
    "BuyerEmail": "test@test.com"
  },
  "EarliestShipDate": "2022-01-01T23:59:59Z",
  "SalesChannel": "Website",
  "OrderStatus": "Shipped",
  "PurchaseDate": "2022-01-01T23:59:59Z",
  "ShippingAddress": {
    "StateOrRegion": "West Midlands",
    "PostalCode": "DY9 0TH",
    "City": "STOURBRIDGE",
    "CountryCode": "GB"
  },
  "LastUpdateDate": "2022-01-01T23:59:59Z",
}
```

After:
```json
{
  "BuyerInfo": {
    "BuyerEmail": "037a51cb9162f51772eaf6b0fb02e1b5d0bf8219deacf723eeedc162209bfd33"
  },
  "EarliestShipDate": "2022-01-01T23:59:59Z",
  "SalesChannel": "Website",
  "OrderStatus": "Shipped",
  "PurchaseDate": "2022-01-01T23:59:59Z",
  "ShippingAddress": {
    "StateOrRegion": "08fa57d00de1936ebea7aeaf8e36d04510a5d885cfaa4f169c2b010d36ccaca4",
    "PostalCode": "714f02c01e20988ee273776dc218f44326c2f5839618b0c117413b0cc7d91701",
    "City": "STOURBRIDGE",
    "CountryCode": "GB"
  },
  "LastUpdateDate": "2022-01-01T23:59:59Z",
}
```
