import requests
import logging
import datetime
now = datetime.datetime.now()
nowstr = now.strftime("%Y%m%d%H%M%S")
timestr = "{}".format(nowstr)
logpath = "logs/{}.log".format(timestr)


def fetch():
	return ""

def parse(raw):
	return ['1','2','3','4','5']

def export(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for line in data:
                file.write(line + '\n')
    except Exception as e:
        logger.Error(f"An error occurred while writing to {filename}: {e}")


if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG,
	                    filename=logpath,
	                    datefmt='%Y/%m/%d %H:%M:%S',
	                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')

	logger = logging.getLogger(__name__)
	logger.info("Crawler start to run")

	raw_data = fetch()
	
	parsed = parse(raw_data)
	export(parsed, "data/{}.csv".format(timestr))