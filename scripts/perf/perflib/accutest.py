"""rocFFT accuracy tests launch utils."""

import logging
import pathlib
import re
import subprocess
import tempfile
import time


def get_active_tests_tokens(accutest):
    """Run rocfft-test and retrieves the list of all active accuracy tests tokens"""
    cmd = [pathlib.Path(accutest).resolve()]
    cmd += ['--gtest_list_tests']

    fout = tempfile.TemporaryFile(mode="w+")
    ferr = tempfile.TemporaryFile(mode="w+")

    proc = subprocess.run(cmd,
                          stdout=fout,
                          stderr=ferr)

    fout.seek(0)
    ferr.seek(0)
    cout = fout.read()
    cerr = ferr.read()

    test_token_list = []
    if proc.returncode == 0:        
        sub_str_1 = '/accuracy_test.'
        sub_str_2 = 'DISABLED'
        sub_str_3 = 'vs_fftw/'
        sub_str_4 = '#'

        get_token = False
        for line in cout.splitlines():
            sub_str_1_found = True if line.find(sub_str_1) != -1 else False
            sub_str_2_found = True if line.find(sub_str_2) != -1 else False
            sub_str_3_found = True if line.find(sub_str_3) != -1 else False

            if sub_str_1_found and not sub_str_2_found:
                get_token = True
                continue
            elif sub_str_3_found and get_token:
                token = line.split(sub_str_3)
                token = token[1].split(sub_str_4)
                token = token[0].strip()

                test_token_list.append(token)
            else:
                get_token = False
    else:
        logging.warn(f'Unable to run accuracy tests: ' + cmd )
        print(cout)
        print(cerr)

    return test_token_list
