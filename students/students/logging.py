import logging

logging.basicConfig(filename='logFile.txt',
                            filemode='a',level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - File_Name- %(filename)s - Function_Name- %(funcName)s - Line_No- %(lineno)d - %(message)s')
root = logging.getLogger()
hdlr = root.handlers[0]
json_format = logging.Formatter('{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s", "Line_No":"%(lineno)d", "Function_Name" : "%(funcName)s"}')
hdlr.setFormatter(json_format)