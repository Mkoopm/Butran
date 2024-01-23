import logging
import os
import pathlib

from beir import LoggingHandler, util  # type: ignore

# source: https://github.com/beir-cellar/beir/tree/main


#### Just some code to print debug information to stdout
logging.basicConfig(
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
    handlers=[LoggingHandler()],
)
#### /print debug information to stdout

#### Download scifact.zip dataset and unzip the dataset
dataset = "scifact"
url = (
    f"https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{dataset}.zip"
)

cur_dir = pathlib.Path(__file__).parent
target_dir = cur_dir.parent
print(cur_dir)
directories = {d for d in os.listdir(target_dir) if os.path.isdir(d)}
print(directories)
if "data" not in directories:
    raise FileNotFoundError("could not find 'data' directory in current dir.")


out_dir = target_dir / "data/raw"
print(out_dir)
data_path = util.download_and_unzip(url, out_dir)
