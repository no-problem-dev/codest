#!/bin/bash

source ./scripts/version.sh

# ビルド用の一時ディレクトリを準備
prepare_build_directory() {
    local version
    version=$(get_version)
    local build_dir="build"
    local package_root="$build_dir/root"
    local bin_dir="$package_root/usr/local/bin"
    local lib_dir="$package_root/usr/local/lib/codest"

    echo "ビルドディレクトリを準備中..."

    # 古いビルドディレクトリを削除
    rm -rf "$build_dir"

    # 必要なディレクトリを作成
    mkdir -p "$bin_dir" "$lib_dir"

    # 必要なファイルをコピー
    cp -r ../src/codest/* "$lib_dir/"
    cp ../setup.py "$lib_dir/"
    cp ../README.md "$lib_dir/"

    # 実行スクリプトの作成
    cat > "$bin_dir/codest" << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHONPATH="/usr/local/lib" exec python3 -m codest "$@"
EOF

    # 実行権限を設定
    chmod 755 "$bin_dir/codest"

    echo "ビルドディレクトリの準備が完了しました"
    return 0
}