import uuid
from datetime import datetime


def get_uuid():
    return str(uuid.uuid4())


def get_current_time():
    now = datetime.now()
    return now.isoformat()


# filter none values
def filter_none_values(dictionary):
    return {key: value for key, value in dictionary.items() if value is not None}


# null safe get
def safe_get(dict_data, *keys):
    for key in keys:
        if dict_data is not None and key in dict_data:
            dict_data = dict_data.get(key)
        else:
            return None
    return dict_data


# if __name__ == "__main__":
#     print(get_uuid())
#     print(get_current_time())
