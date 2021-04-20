import requests
import data_info
import json
import gzip
import os

class Download:
    def __init__(self):
        self.data_url = data_info.data_url
        self.data_name = data_info.data_name


    def download(self):

        for i in range(len(self.data_url)):
            file_url = self.data_url[i]
            file_name =self.data_name[i]
            file_name_gz = file_name + ".gz"
            # get data.gz
            resp = requests.get(file_url, allow_redirects=True)
            # save file
            open(file_name_gz, "wb").write(resp.content)
            # read gz
            with gzip.open(file_name_gz, "r") as f:
                # use utf-8 decode
                file_content = f.read().decode("utf-8")
                # convert str to json
                file_content = json.loads(file_content)
                # save file in json format
                open(file_name + ".json", "w").write(json.dumps(file_content, ensure_ascii=False, indent=4))
            # remove .gz file
            if os.path.exists(file_name_gz):
                os.remove(file_name_gz)

