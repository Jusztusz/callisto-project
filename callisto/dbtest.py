import redis

# Csatlakozás a Redis szerverhez (ha van jelszó, add meg a 'password' paramétert)
r = redis.StrictRedis(host='localhost', port=6379, db=0, password='callisto2024')

# Például néhány adat tárolása a Redis-ben
r.set('kulcs1', 'érték1')
r.set('kulcs2', 'érték2')
r.set('kulcs3', 'érték3')

# Adatok lekérése és megjelenítése
print(f"kulcs1: {r.get('kulcs1').decode('utf-8')}")
print(f"kulcs2: {r.get('kulcs2').decode('utf-8')}")
print(f"kulcs3: {r.get('kulcs3').decode('utf-8')}")

# Tömbök használata (listák)
r.lpush('lista', 'elem1')
r.lpush('lista', 'elem2')
r.lpush('lista', 'elem3')

# Lista kiolvasása
print(f"Lista elemei: {r.lrange('lista', 0, -1)}")
