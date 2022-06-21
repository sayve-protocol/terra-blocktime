# terra-send
Repo for sending coins to multiple addresses

Edit send.py, paste your seed phrase in the SEED=, where it says paste your seed phrase
We currently used test wallet 1 seed from
```
https://docs.google.com/spreadsheets/d/1o-8J4P37blmzyCKaBT4SK19fNbuNHOlVl57SmyeOxr8/edit?usp=sharing
```
Update NETWORK = 'TESTNET' or NETWORK = 'MAINNET' in send.py
If you are using testnet, then you can get some coins for your account at 
```
https://faucet.terra.money/
```
Run the docker
```
docker build -t terra_send .
docker run -it --volume "$(pwd)/send.py:/app/send.py" terra_send:latest
```
For details read
```
https://terra-money.github.io/terra.py/
```

Read input.csv at one time and generate output.csv, add new volum to make output.csv to be generated locally.
```
docker run -it  -v $(pwd):/app  terra_send:latest python multisend.py
```

Read input.csv line by line and generate output.csv, add new volum to make output.csv to be generated locally.
```
docker run -it  -v $(pwd):/app  terra_send:latest python multisend_v2.py
```

output.csv structure is made of terra_address,sayve_amount,ust_amount,txhash

Calculate Part
```
docker run -it  -v $(pwd):/app  terra_send:latest python new_calculate.py
```
it will generate calculate.csv and output.json


The following command is to check the allocation number plus refund ust equal total deposit

```
docker run -it  -v $(pwd):/app  terra_send:latest python test.py
```