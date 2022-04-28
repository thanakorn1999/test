from cgi import test
from email import message
from fastapi import FastAPI,UploadFile,File
from test_function import *
import pandas as pd
from typing import List

from fastapi import FastAPI, File, UploadFile
import pandas as pd
app = FastAPI()



@app.post("/files/")
async def create_file(files: bytes = File(...)):
    return {"file_size": [len(file) for file in files]}


@app.post("/uploadfile/")

# https://fastapi.tiangolo.com/tutorial/request-files/  Multiple File Uploads with Additional Metadata
async def create_upload_file(files: List[UploadFile]):
    # https://stackoverflow.com/questions/22216076/unicodedecodeerror-utf8-codec-cant-decode-byte-0xa5-in-position-0-invalid-s

    data=["centroids","coordinates"]

    for file in files:
        data_f = pd.read_csv(file.filename, encoding = 'unicode_escape')
        if file.filename.split(".")[0] == "centroids":
            data[0] = data_f

        elif file.filename.split(".")[0] == "coordinates":
            data[1] = data_f

    # return {data}
    if type(data[0]) and type(data[1]) is not type("str"):
        print("run")
        n_5_meters ,n_10_meters ,radius_min_of_80 ,rcdmax_less_than_minrct=calculate(data[0],data[1])

        return {"coordinates are within 5 meters ": n_5_meters,
                "coordinates are within 10 meters ":n_10_meters,
                "radius R such that 80 percent ":radius_min_of_80,
                "radius_max_coordinates < min_radius_centroids ":rcdmax_less_than_minrct,
                }
    else:
        return{
            "file name": [len(file) for file in files]
            }