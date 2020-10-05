import json
import fasteners
import os
import gzip
from itertools import zip_longest
import re

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)

def write_to_record(object, file_output_path, by_line=False, is_append=False):
    os.makedirs(os.path.dirname(file_output_path), exist_ok=True)
    with fasteners.InterProcessLock(file_output_path):
        try:
            if not is_append:
                with open(file_output_path, "w+") as file:
                    if not by_line:
                        file.write(object)
                    else:
                        file.write(object + '\n')

            else:
                with open(file_output_path, "a") as file:
                    if not by_line:
                        file.write(object)
                    else:
                        file.write(object + '\n')
        except Exception as e:
            print("write_to_record error: ", e)


def load_json(json_path):
    try:
        with open(json_path, "r", encoding='utf8') as json_file:
            return json.load(json_file)
    except Exception as e:
        print("load_json({}): {}".format(json_path, e))


def read_text(file_path):
    contents = []
    with open(file_path, "r") as txt_file:
        for line in txt_file.readlines():
            contents.append(line.replace("\n", ""))

    return contents


def store_json_gz(json_obj, file_output_path, is_append=False):
    os.makedirs(os.path.dirname(file_output_path), exist_ok=True)
    with fasteners.InterProcessLock(file_output_path):
        if is_append:
            with gzip.open(file_output_path, 'ab') as f:
                f.write(('\n' + json.dumps(json_obj, ensure_ascii=False, indent=2)).encode('utf-8'))
        else:
            with gzip.open(file_output_path, 'wb') as f:
                f.write((json.dumps(json_obj, ensure_ascii=False, indent=2)).encode('utf-8'))


def store_gz(obj, file_output_path):
    os.makedirs(os.path.dirname(file_output_path), exist_ok=True)
    with fasteners.InterProcessLock(file_output_path):
        with gzip.open(file_output_path, 'wt') as f:
            f.write(obj)


def load_jsonl_from_gz(file_gz_path):
    try:
        with gzip.open(file_gz_path, 'rt') as f:
            file_content = f.read()
            obj = json.loads(file_content)
            return obj
    except Exception as e:
        print("load_jsonl_from_gz {} error {}".format(file_gz_path, e))


def make_sitemap_paper_title(title):
    sub1 = re.sub("[\(|\[|{]([^)]*)[\)|\]|}]","",title.strip())
    sub2 = re.sub("\s+|\W+","-",sub1)
    sub3 = re.sub("\-{2,}","-",sub2)
    sub4 = re.sub("\-$","",sub3)

    return sub4


if __name__ == '__main__':
    title = "Aurora-A/STK15 T+91A is a general low penetrance cancer susceptibility gene: a meta-analysis of multiple cancer types."
    print(make_sitemap_paper_title(title))
