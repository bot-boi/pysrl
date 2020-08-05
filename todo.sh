#!/bin/bash
grep -nr --exclude-dir=env '# TODO:' .
