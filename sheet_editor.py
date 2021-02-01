import gspread
from datetime import date, timedelta
from time import sleep
from setup import logger_setup
logger = logger_setup(__name__)


class SheetEditor:
    def __init__(self, starting_day):
        self.starting_day = starting_day
        logger.info('Connecting to spreadsheet...')
        self.gc = gspread.service_account(filename='service_account.json')
        self.sh = self.gc.open("Coronavirus - world").worksheet('Data')
        logger.info('Connected!')

    def update_cell(self, adr, content):
        while True:
            try:
                self.sh.update(adr, content)
                return
            except gspread.exceptions.APIError as e:
                logger.error(e)
                logger.info('Trying again in 5...')
                sleep(5)

    def update_row(self, data, day):
        logger.info(f'Uploading data for {day}')
        row = (day - self.starting_day).days + 2
        logger.debug(f'Updating row: {row}')
        logger.debug(f'Received data: {data}')

        col = 1
        adr = self.coords_to_adr(col, row)
        self.update_cell(adr, str(day))

        for region in data:
            for number in data[region].values():
                col += 1
                adr = self.coords_to_adr(col, row)
                self.update_cell(adr, str(number))

    def update_header(self, data):
        if not data:
            return

        logger.info(f'Updating header')
        row = 1

        col = 1
        adr = self.coords_to_adr(col, row)
        self.update_cell(adr, 'Date')

        for region in data:
            for category in data[region]:
                col += 1
                adr = self.coords_to_adr(col, row)
                text = region + '\n' + category
                self.update_cell(adr, text)

    def coords_to_adr(self, col, row):
        col_string = ""
        while col > 0:
            col, remainder = divmod(col - 1, 26)
            col_string = chr(65 + remainder) + col_string
        return col_string + str(row)


if __name__ == '__main__':
    sheet_editor = SheetEditor()
    print(sheet_editor.coords_to_adr(258, 4))