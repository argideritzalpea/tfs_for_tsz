#!/bin/bash

LINE=$1

diff <(./translate-line.sh eng tsz $LINE 2>&1) <(./translate-line.sh eng tmp_tsz $LINE 2>&1)
