#!/bin/bash

# 後処理を実行
cleanup_build() {
    echo "一時ファイルを削除中..."

    # 仮想環境を無効化
    deactivate 2>/dev/null || true

    # ビルド時に作成された中間ファイルを削除
    find ../src -name "*.pyc" -delete
    find ../src -name "__pycache__" -type d -exec rm -r {} +
    find . -name "*.pyc" -delete
    find . -name "__pycache__" -type d -exec rm -r {} +

    echo "クリーンアップが完了しました"
}