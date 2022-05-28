# Standard imports
import time

# Third party imports
import gspread

# User imports
from settings import *


def get_worksheet(worksheet_id):
    # service_account.json: Sri Nithya Priyeshananda google developers console file
    gc = gspread.service_account(filename=GSPREAD_SERVICE_ACCOUNT_FILE)
    sh = gc.open_by_key(worksheet_id)
    return sh.sheet1


# TODO: fix when we have an empty string after filled cells, we do not get the empty string cell after
def get_last_empty_string_index(list_of_strings, filter_string_func=True):
    try:
        last_empty_string_index = 0

        index = 1
        for s in list_of_strings:
            if len(s) == 0:
                last_empty_string_index = index
            index += 1

        return last_empty_string_index
        # return next(s for s in list_of_strings if s and filter_string_func(s))
    except StopIteration:
        return False


# TODO: fix when we have an empty string after filled cells, we do not get the empty string cell after
def get_last_cell_with_value(list_of_strings, lookup_value):
    try:
        last_cell_index = 0

        index = 1
        for s in list_of_strings:
            if len(s) == 1 and s[0] == lookup_value:
                last_cell_index = index
            index += 1

        return last_cell_index
        # return next(s for s in list_of_strings if s and filter_string_func(s))
    except StopIteration:
        return False


# TODO: fix when we have an empty string after filled cells, we do not get the empty string cell after
def get_first_empty_string_index(list_of_strings, filter_string_func=True):
    try:
        index = 1
        for s in list_of_strings:
            if len(s) == 0:
                return index
            index += 1

        return index
        # return next(s for s in list_of_strings if s and filter_string_func(s))
    except StopIteration:
        return False


# TODO handle errors
# Error 1
#     raise APIError(response)
# example message
# gspread.exceptions.APIError: {'code': 429, 'message': "Quota exceeded for quota group 'WriteGroup' and limit 'Write requests per user per 100 seconds' of service 'sheets.googleapis.com' for consumer 'project_number:69182034214'.", 'status': 'RESOURCE_EXHAUSTED', 'details': [{'@type': 'type.googleapis.com/google.rpc.Help', 'links': [{'description': 'Google developer console API key', 'url': 'https://console.developers.google.com/project/69182034214/apiui/credential'}]}]}
# Error 2
#  raise ReadTimeout(e, request=request)
# requests.exceptions.ReadTimeout: HTTPSConnectionPool(host='sheets.googleapis.com', port=443): Read timed out. (read timeout=120)


def worksheet_update(worksheet, range_name, values=None, **kwargs):
    while True:
        try:
            worksheet.update(range_name, values)
            break
        except gspread.exceptions.APIError as e:
            quota_error_message = "Quota exceeded for quota group 'WriteGroup' and limit 'Write requests per user per 100 seconds' of service 'sheets.googleapis.com'"

            if quota_error_message in str(e):
                print(quota_error_message)
                print("Waiting for 108 seconds...")
                time.sleep(108)
                print("Retrying...")


def set_file_link_in_google_sheet(worksheet, row_num, file_link_path):
    worksheet_update(worksheet, "G" + str(row_num), file_link_path)


def set_status_in_google_sheet(worksheet, row_num, status):
    worksheet_update(worksheet, "F" + str(row_num), status)


def set_uploaded_in_google_sheet(worksheet, row_num):
    set_status_in_google_sheet(worksheet, row_num, "uploaded")


def set_youtube_link_in_google_sheet(worksheet, row_num, youtube_link):
    worksheet_update(worksheet, "E" + str(row_num), youtube_link)


def set_all_fields_same_value(worksheet, row_num, status):
    set_youtube_link_in_google_sheet(worksheet, row_num, status)
    set_status_in_google_sheet(worksheet, row_num, status)
    set_file_link_in_google_sheet(worksheet, row_num, status)


def is_valid_row(row_num):
    return row_num != 1 and row_num != None


def get_start_row_num(worksheet):
    """
    Get start row number for processing uploads
    from bottom to top of the file
    => from oldest years to newer years
    """
    try:
        hpedia_yt_links = worksheet.get("E1:E" + str(worksheet.row_count))
        # print(len(hpedia_yt_links))
        # sys.exit()
        # first_non_empty_hpedia_yt_link = get_first_non_empty_string(
        last_empty_hpedia_yt_link_row_num = get_last_empty_string_index(
            hpedia_yt_links, lambda s: s[0] != "HPedia YouTube link"
        )

        # if not first_non_empty_hpedia_yt_link:
        #     last_empty_hpedia_yt_link_row_num = worksheet.row_count
        # else:
        #     last_empty_hpedia_yt_link_row_num = hpedia_yt_links.index(
        #         first_non_empty_hpedia_yt_link
        #     )
    except KeyError as e:
        print("No Hpedia link for now")
        last_empty_hpedia_yt_link_row_num = worksheet.row_count

    return last_empty_hpedia_yt_link_row_num


def get_start_row_num_download50(worksheet):
    """
    Get start row number for processing uploads
    from bottom to top of the file
    => from oldest years to newer years
    """
    try:
        hpedia_yt_links = worksheet.get("E1:E" + str(worksheet.row_count))
        # print(len(hpedia_yt_links))
        # sys.exit()
        # first_non_empty_hpedia_yt_link = get_first_non_empty_string(
        first_empty_hpedia_yt_link_row_num = get_first_empty_string_index(
            hpedia_yt_links, lambda s: s[0] != "HPedia YouTube link"
        )

        # if not first_non_empty_hpedia_yt_link:
        #     last_empty_hpedia_yt_link_row_num = worksheet.row_count
        # else:
        #     last_empty_hpedia_yt_link_row_num = hpedia_yt_links.index(
        #         first_non_empty_hpedia_yt_link
        #     )
    except KeyError as e:
        print("No Hpedia link for now")
        first_empty_hpedia_yt_link_row_num = worksheet.row_count

    return first_empty_hpedia_yt_link_row_num


def get_draft_start_row_num(worksheet):
    """
    Get start row number for processing uploads
    from bottom to top of the file
    => from oldest years to newer years
    """
    try:
        status_rows = worksheet.get("F1:F" + str(worksheet.row_count))
        # print(len(hpedia_yt_links))
        # sys.exit()
        # first_non_empty_hpedia_yt_link = get_first_non_empty_string(
        last_draft_row_num = get_last_cell_with_value(status_rows, "draft")

        # if not first_non_empty_hpedia_yt_link:
        #     last_empty_hpedia_yt_link_row_num = worksheet.row_count
        # else:
        #     last_empty_hpedia_yt_link_row_num = hpedia_yt_links.index(
        #         first_non_empty_hpedia_yt_link
        #     )
    except KeyError as e:
        print("No drafts")
        last_draft_row_num = worksheet.row_count

    return last_draft_row_num