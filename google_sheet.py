import gspread
class GoogleSheet:
    def __init__(self, sheet_id):
        self.gc = gspread.service_account(filename='service_account.json')
        self.sh = self.gc.open_by_key(sheet_id)
    def read(self):
        worksheet = self.sh.sheet1
        return worksheet.get_all_values() 