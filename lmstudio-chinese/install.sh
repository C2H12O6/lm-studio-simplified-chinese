#!/bin/bash
echo ""
echo "  LM Studio 简体中文汉化补丁"
echo "  ============================"
echo ""
python3 "$(dirname "$0")/patch_lmstudio.py" "$@"
