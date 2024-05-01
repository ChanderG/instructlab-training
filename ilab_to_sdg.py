import json
import sys
from pathlib import Path
import glob
import os

def ilab_to_sdb(ilab_train_data_dir, taxonomy_path):
    """
    Convert a ilab train dataset to a SDG compatible format for backend training

    Parameters:
        ilab_train_data_dir: path to directory where train dataset generated by ilab lives.
                            We automatically pick the latest training file from the ones present 
                            there.
        taxonomy_path: path to the taxonomy dataset used for generating the train dataset
    """
    items_list = []
    files = glob.glob(os.path.join(ilab_train_data_dir, "train_model_*.jsonl"),  
                    recursive = False) 
    try:
        files.sort(reverse=True)
        latest_train_file = files[0]
    except IndexError:
        print("IndexError: no matching files found")
        return 
    
    with open(latest_train_file, "r") as file:
        # Read each line (which represents a JSON object)
        for line in file:
            line = json.loads(line)
            new_dict = {"messages": []}
            for key, value in line.items():
                tmp = {}
                tmp["content"] = value
                tmp["role"] = key
                new_dict["messages"].append(tmp)

            new_dict["group"] = "lab_extension"
            new_dict["dataset"] = taxonomy_path
            new_dict["metadata"] = "{\"num_turns\": 1}"
            items_list.append(new_dict)

    with open("sdg_out.jsonl", "a", encoding="utf-8") as file:
        for item in items_list:
            file.write(json.dumps(item))
            file.write('\n')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ilab_train_data_dir = sys.argv[1]
        taxonomy = sys.argv[2]
    else:
        print("provide ilab train data dir as an argument")
        sys.exit(1)
    ilab_to_sdb(ilab_train_data_dir, taxonomy)