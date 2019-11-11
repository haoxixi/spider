from city import CITY_CODE, CAR_CODE_LIST
from redis import Redis
# import sys
# sys.path.append("..")
class Redis_url():
    def __init__(self):
        self.re = Redis("localhost",6379)

    def add(self,url):
        self.re.lpush("taoche:start_urls",url)

rd = Redis_url()
for city in CITY_CODE:
    for car_code in CAR_CODE_LIST:
        rd.add( "https://{}.taoche.com/{}/".format(city, car_code))

