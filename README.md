# terra-send
Repo for calculating block time given a time

Run the docker
```
docker build -t terra_calculate .
docker run -it  -v $(pwd):/app  terra_calculate:latest python calculate.py
```
For details read
```
https://terra-money.github.io/terra.py/
```
You can adjust the time in calculate.py to calculate a new time
