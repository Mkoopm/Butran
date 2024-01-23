import json
from pathlib import Path

import tqdm

from src.translate import TranslatorMarianMT

dataset = "scifact"
base_dir = Path("data")
input_dir = base_dir / "raw" / dataset
output_dir = base_dir / "translated" / dataset


translator = TranslatorMarianMT("en", "nl")
with open(input_dir / "corpus.jsonl") as fp_in:
    nr_lines = len([1 for line in fp_in])


with open(input_dir / "corpus.jsonl") as fp_in:
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_dir / "corpus.jsonl", "w") as fp_out:
        for line in tqdm.tqdm(fp_in, total=nr_lines):
            data = json.loads(line)
            data["title"] = translator.translate(data["title"])
            data["text"] = translator.translate(data["text"])
            fp_out.write(f"{json.dumps(data)}\n")
