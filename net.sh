#!/bin/bash

git clone https://github.com/Minashi/SIEM-Lab-validation/

mv SIEM-Lab-validation/qradar150vali.py /home/ec2-user/

rm -rf SIEM-Lab-validation

chmod +x /home/ec2-user/qradar150vali.py
