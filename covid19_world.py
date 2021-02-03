from datetime import date, timedelta
import requests
from collections import Counter
from setup import logger_setup
logger = logger_setup(__name__)
from sheet_editor import SheetEditor

class Covid19_World:
    def __init__(self):
        logger.info('Initialization...')
        self.dir_download_path = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
        self.file_name_format = '%m-%d-%Y'
        self.file_extension = '.csv'

        self.interesting_regions = [
            # 'World'
            'Poland',
            'US',
            'Germany',
            'Czechia',
            'Slovakia',
            'Ukraine',
            'Belarus',
            'Lithuania',
            'Russia',
            'Italy',
            'Spain',
            'United Kingdom']
        self.keys = ['Confirmed', 'Deaths', 'Recovered', 'Active']

        self.starting_day = date(year=2020, month=3, day=4)

        logger.info('Initialized!')

    def download_data(self, day):
        logger.info(f'Downloading data for {day}...')
        path = self.dir_download_path + day.strftime(self.file_name_format) + self.file_extension
        logger.debug(f'Downloading from {path}')
        raw_chars = requests.get(path)
        raw_chars.raise_for_status()
        logger.debug('Data downloaded!')

        line = ''
        raw_lines = []
        commas_to_underscore = False
        for char in raw_chars.text:
            if char == '\n':
                raw_lines.append(line)
                line = ''
                commas_to_underscore = False
            else:
                if char == '"':
                    commas_to_underscore = not commas_to_underscore
                if commas_to_underscore and char == ',':
                    line += '_'
                else:
                    line += char
        return raw_lines

    def parse_raw_lines(self, raw_lines):
        logger.info(f'Parsing data...')
        split_lines = []
        for line in raw_lines:
            split_lines.append(line.split(','))

        reqions_dicts = dict()
        reqions_dicts['World'] = dict()
        for key in self.keys:
            reqions_dicts['World'][key] = 0

        for line in split_lines[1:]:
            if line[3] in self.interesting_regions:
                if not line[3] in reqions_dicts:
                    reqions_dicts[line[3]] = Counter()
                    logger.debug(f'Parsing region: {line[3]}')
            for i, key in enumerate(split_lines[0]):
                if key in self.keys:
                    try:
                        reqions_dicts['World'][key] += int(line[i])
                        if line[3] in self.interesting_regions:
                            reqions_dicts[line[3]][key] += int(line[i])
                    except ValueError:
                        pass

        return reqions_dicts

    def run(self, days):
        days_of_data, days_since_start = self.get_days_of_data(days)
        todays_row = days_since_start+2
        print(f'Todays row: {todays_row}')
        sheet_editor = SheetEditor(self.starting_day)


        for days_back in range(days_of_data):
            day = date.today() - timedelta(days=days_back)
            try:
                raw_lines = self.download_data(day)
                data_dict = self.parse_raw_lines(raw_lines)
                # print(data_dict)
                logger.info(f'Day {day} data!')
            except requests.exceptions.HTTPError as e:
                logger.info(f'No data to download for {day}')
            try:
                sheet_editor.update_row2(data_dict, day)
            except:
                pass

        # sheet_editor.update_header(data_dict)


    def get_days_of_data(self, days):
        days_since_start = (date.today() - self.starting_day).days
        if days <= 0 or days > days_since_start:
            days_of_data = days_since_start + 1
        else:
            days_of_data = days + 1
        return days_of_data, days_since_start


if __name__ == '__main__':
    covid = Covid19_World()
    covid.run(0)