#!/bin/bash
# cobot1 디렉토리를 제외한 모든 항목 삭제

for item in *; do
    if [ "$item" != "cobot1" ]; then
        echo "삭제 중: \$item"
        rm -rf "\$item"
    fi
done
