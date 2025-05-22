
import polars as pl
import json

from pathlib import Path

class FileReader:
    def __init__(self,path:str):
        self.path=Path(path)
        self.file_type=self.path.suffix.lower().strip(".")

    def read(self)-> pl.DataFrame:
        match self.file_type:
            case "csv":
                return self._read_csv()
            case "json":
                return self._read_json()
            case _:
                raise ValueError(f"Unsupported file type: {self.file_type}")
    
    #read csv function
    def _read_csv(self)->pl.DataFrame:
        return pl.read_csv(self.path)
    
    #read json function
    def _read_json(self)->pl.DataFrame:
        try:
            return pl.read_ndjson(self.path)
        except Exception:
            with open(self.path, 'r') as f:
                data=json.load(f)
            return pl.DataFrame(data)