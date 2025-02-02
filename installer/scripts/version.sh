#!/bin/bash

# バージョン情報を取得する関数
get_version() {
    # 最新のタグを取得
    local version
    version=$(git describe --tags --abbrev=0)
    # 先頭のvを削除
    echo "${version#v}"
}