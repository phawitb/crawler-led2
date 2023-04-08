#!/bin/bash

python 1_crawler_led.py nonthaburi
python 2_find_gps.py nonthaburi
python 3_combile_data.py nonthaburi
# python 4_sent_to_DB.py nonthaburi

python 1_crawler_led.py bangkok
python 2_find_gps.py bangkok
python 3_combile_data.py bangkok
# python 4_sent_to_DB.py bangkok

python 1_crawler_led.py nakhonpathom
python 2_find_gps.py nakhonpathom
python 3_combile_data.py nakhonpathom
# python 4_sent_to_DB.py nakhonpathom



# $ chmod +x run_scripts.sh
# ./run_scripts.sh