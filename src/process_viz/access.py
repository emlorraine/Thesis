import gspread
from gspread_dataframe import get_as_dataframe


def pull_reddit_data():
    data = []
    credentials = {
        # TODO: https://docs.gspread.org/en/latest/oauth2.html#for-end-users-using-oauth-client-id
    } 
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open("svg_data")
    for wk in sh:
        wh_data = wk.get_all_records()
        data.append(wh_data)
    return data

