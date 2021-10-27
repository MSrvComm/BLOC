#!/usr/bin/env python3

import os
import sys

if len(sys.argv) == 2:
    DEP_DIR = f"{sys.argv[1]}/k8s_deployment"
else:
    DEP_DIR = "k8s_deployment/"


def delete_hpa_rules():
    for name in os.listdir(DEP_DIR):
        cmd = f"kubectl delete hpa {name.split('.')[0]}"
        os.system(cmd)


if __name__ == "__main__":
    delete_hpa_rules()
