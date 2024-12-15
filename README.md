# Callisto-project
Egyszerű, Docker-kompatibilis monitoring eszköz

## Előkövetelmények (ajánlott)
- CPU: Intel/AMD 2 GHz
- RAM: 8 GB
- Architecture: 64-bit

<small>*A memóriában futó adatbázis miatt célszerű a lehető legtöbb memóriát használni!*</small>

## Használat docker fájllal
Docker link: https://hub.docker.com/repository/docker/jusztuszxd/callisto-project/general

1. Le kell tölteni a docker képfájlt
   ```bash
   docker pull jusztuszxd/callisto-project
2. Docker run paranccsal való futtatáshoz
   ```bash
   docker run -d \
     -p 8001:80 \
     -p 8002:22 \
     -p 8003:6379 \
     jusztuszxd/callisto-project
