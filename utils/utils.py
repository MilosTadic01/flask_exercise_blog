import sys
import os
import json
from typing import List, Dict

DATA_PATH = "data/storage.json"


class Utils:
    """General utilities"""
    @staticmethod
    def load_storage_data():
        """Returns List[Dict], of [] if empty file to start new dataset."""
        if not os.path.exists(DATA_PATH):
            fd = os.open(DATA_PATH, os.O_CREAT)
            os.close(fd)
        with open(DATA_PATH, "r") as fd:
            raw = fd.read()
        if not raw:
            return []
        return json.loads(raw)

    @staticmethod
    def list_extant_ids():
        """Produce and return a list of unique ids currently in use."""
        list_of_dicts = Utils.load_storage_data()
        list_of_used_ids = [bp_dict.get('id') for bp_dict in list_of_dicts]
        return list_of_used_ids

    @staticmethod
    def get_unique_id():
        """Returns lowest available positive integer not used as id"""
        list_of_used_ids = Utils.list_extant_ids()
        for id_int in range(1, sys.maxsize):
            if id_int not in list_of_used_ids:
                return id_int

    @staticmethod
    def write_data_to_storage(blog_posts: List[Dict]):
        """Dumps and writes List[Dict] of blog posts to storage."""
        with open("data/storage.json", "w") as fd:
            str_to_write = json.dumps(blog_posts)
            fd.write(str_to_write)
