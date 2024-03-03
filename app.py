# app.py
from flask import Flask, request
from datetime import datetime
import redis
import time
import os  # Import os module for environment variable

app = Flask(__name__)
cache = redis.StrictRedis(host='redis', port=6379, decode_responses=True)
environment = os.environ.get('V_ENV', 'default')

def get_hit_count():
    for _ in range(5):
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError:
            time.sleep(0.5)
    raise redis.exceptions.ConnectionError("Exhausted retries for incrementing hits")

@app.route('/')
def greeting():
    current_date = datetime.now()
    day_of_week = current_date.strftime("%A")
    count = get_hit_count()

    greeting_message = 'Dzień dobry, Pani Doktor. Przepraszam za niedogodności. Życzę udanej reszty weekendu!\n'
    cache.set('greeting', f'{greeting_message}Licznik odwiedzin: {count}')

    return cache.get('greeting')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)