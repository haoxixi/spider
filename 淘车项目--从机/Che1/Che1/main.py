from scrapy import cmdline
from scrapy.cmdline import execute
import os,sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy","crawl","Che"])
# cmdline.execute("scrapy crawl Che --nolog".split())
# cmdline.execute("scrapy crawl Che".split())
