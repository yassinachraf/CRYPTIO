import requests

url = "https://app-api.cryptio.co/api/movement?transaction_hashes=0xfdf027f88de3290e8493086abdf24b2b1316c3159be2b5ef06109784c81cbbc7&transaction_hashes=0x2f67ba2394dca3287a30c35caa7a70f42c1aea570bc8bbb86308ced0534c0f49"

headers = {
    "accept": "application/json",
    "cryptio-api-key": "2e737658-575d-4b42-8625-616c5f115cb5"
}

response = requests.get(url, headers=headers)

print(response.text)