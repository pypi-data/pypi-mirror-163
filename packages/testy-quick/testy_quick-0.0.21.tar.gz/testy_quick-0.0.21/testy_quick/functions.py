import os

import pandas as pd

from . import settings
from .handlers import BaseReader, BaseAnswer
from .structures import TestyRunner


def read_input(complete_file_path, var_name, reader_key):
    """

    :param complete_file_path:
    :param var_name:
    :param reader_key:
    :return:
    """
    reader = BaseReader.get_handler(reader_key)
    ans = reader.read(complete_file_path, var_name)
    return ans


def run_fct(f, case):
    args, kwargs = _extract_inputs(case)
    ans = f(*args, **kwargs)
    return ans

def _reverse_join(path):
    head,tail=os.path.split(path)
    if head:
        return _reverse_join(head)+[tail]
    return [tail]
def _shorted_path(path):
    l=_reverse_join(path)
    i=1
    while i<len(l):
        if i==0:
            i+=1
            continue
        if l[i]=="..":
            del (l[i - 1])
            del (l[i - 1])
            i-=1
        else:
            i+=1
    return os.path.join(l)



def _extract_inputs(case):
    folder = os.path.join(settings.BASE_DATA_FOLDER, case)
    reader_key = settings.INPUT_META_READER[0]
    input_meta_file = os.path.join(folder, settings.INPUT_META_FILE_NAME)
    input_meta: pd.DataFrame = read_input(input_meta_file, settings.INPUT_META_READER[1], reader_key)
    assert not input_meta[settings.INPUT_META_VAR_COL].duplicated().any()
    args = list()
    kwargs = dict()
    for _, r in input_meta.iterrows():
        var_name = r[settings.INPUT_META_VAR_COL]
        complete_file_path = os.path.join(folder, r[settings.INPUT_META_FILE_COL])
        complete_file_path=_shorted_path(complete_file_path)
        input_datum = read_input(
            complete_file_path=complete_file_path,
            var_name=var_name,
            reader_key=r[settings.INPUT_META_READER_COL]
        )
        if r[settings.INPUT_META_NAMED_COL]:
            kwargs[var_name] = input_datum
        else:
            args.append(input_datum)

    return args, kwargs


def _extract_outputs(case):
    folder = os.path.join(settings.BASE_DATA_FOLDER, case)
    reader_key = settings.OUTPUT_META_READER[0]
    output_meta_file = os.path.join(folder, settings.OUTPUT_META_FILE_NAME)
    input_meta: pd.DataFrame = read_input(output_meta_file, settings.OUTPUT_META_READER[1], reader_key)
    ans = list()
    for _, r in input_meta.iterrows():
        complete_file_path = os.path.join(folder, r[settings.OUTPUT_META_FILE_COL])
        complete_file_path = _shorted_path(complete_file_path)
        var_name = r[settings.OUTPUT_META_VAR_COL]
        handler = BaseAnswer.get_handler(r[settings.OUTPUT_META_READER_COL])
        output_datum = handler.read(complete_file_path, var_name)
        ans.append((var_name, output_datum, handler))
    return ans


def create_test(fct_to_test, case, case_name) -> TestyRunner:
    args, kwargs = _extract_inputs(case)
    run_fct_c = lambda: fct_to_test(*args, **kwargs)
    outputs = _extract_outputs(case)
    ans = TestyRunner(run_function=run_fct_c, check_functions=outputs, case_name=case_name)
    return ans
