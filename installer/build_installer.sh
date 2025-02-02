#!/bin/bash

#
# Codestインストーラービルドスクリプト
#

set -e  # エラー時に実行を停止

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"

# 各スクリプトを読み込み
source ./scripts/env.sh
source ./scripts/version.sh
source ./scripts/validation.sh
source ./scripts/prepare.sh
source ./scripts/package.sh
source ./scripts/cleanup.sh
source ./scripts/notarization.sh

# ヘルプメッセージの表示
show_help() {
    cat << EOF
使用方法: ./build_installer.sh [オプション]

オプション:
    -h, --help              このヘルプメッセージを表示
    -v, --version           バージョン情報を表示
    -d, --debug            デバッグモードで実行
    -p, --production       本番モードで実行（署名と公証を含む）

デフォルトでは開発モードで実行され、署名と公証はスキップされます。
本番用のビルドを行う場合は --production オプションを使用してください。
EOF
}

# バージョン情報の表示
show_version() {
    local version
    version=$(get_version)
    echo "Codest Installer Builder v${version}"
}

# コマンドライン引数の解析
parse_arguments() {
    PRODUCTION_MODE=false
    DEBUG_MODE=false

    while [[ "$#" -gt 0 ]]; do
        case $1 in
            -h|--help) show_help; exit 0 ;;
            -v|--version) show_version; exit 0 ;;
            -p|--production) PRODUCTION_MODE=true ;;
            -d|--debug) DEBUG_MODE=true; set -x ;;
            *) echo "不明なオプション: $1"; show_help; exit 1 ;;
        esac
        shift
    done
}

# 一時ディレクトリの作成
setup_temp_directory() {
    TEMP_DIR=$(mktemp -d)
    trap 'rm -rf "$TEMP_DIR"' EXIT
    echo "一時ディレクトリを作成しました: $TEMP_DIR"
}

# メイン処理
main() {
    local start_time
    start_time=$(date +%s)

    echo "インストーラービルドを開始します..."

    # コマンドライン引数の解析
    parse_arguments "$@"

    # 本番モードの場合は環境変数をロード
    if [ "$PRODUCTION_MODE" = true ]; then
        echo "本番モードでビルドを実行します（署名と公証を含む）"
        # ここで load_env を呼び出し
        if ! load_env; then
            echo "環境変数の設定を確認してください"
            exit 1
        fi
    else
        echo "開発モードでビルドを実行します（署名と公証はスキップ）"
    fi

    # 一時ディレクトリのセットアップ
    setup_temp_directory

    # ビルド環境の検証
    if ! validate_build_environment; then
        echo "エラー: ビルド環境の検証に失敗しました"
        exit 1
    fi

    # 本番モードの場合のみ公証環境を検証
    if [ "$PRODUCTION_MODE" = true ]; then
        if ! validate_notarization_environment; then
            echo "エラー: 公証環境の検証に失敗しました"
            exit 1
        fi
    fi

    # バージョン番号の取得と表示
    local version
    version=$(get_version)
    echo "ビルドバージョン: $version"

    # ビルドディレクトリの準備
    if ! prepare_build_directory; then
        echo "エラー: ビルドディレクトリの準備に失敗しました"
        exit 1
    fi

    # インストーラーパッケージの作成
    local package_path
    if ! package_path=$(create_installer_package "$PRODUCTION_MODE"); then
        echo "エラー: インストーラーパッケージの作成に失敗しました"
        exit 1
    fi

    # 本番モードの場合のみ署名と公証を実行
    if [ "$PRODUCTION_MODE" = true ]; then
        if ! notarize_package "$package_path" \
            "com.noproblem.codest" \
            "$APPLE_ID" \
            "$APPLE_ID_PASS" \
            "$TEAM_ID"; then
            echo "エラー: パッケージの公証に失敗しました"
            exit 1
        fi

        if ! attach_notarization_ticket "$package_path"; then
            echo "エラー: 公証チケットの添付に失敗しました"
            exit 1
        fi
    fi

    # 後処理
    cleanup_build

    # 実行時間の計算と表示
    local end_time
    end_time=$(date +%s)
    local duration=$((end_time - start_time))

    echo "インストーラービルドが正常に完了しました"
    echo "所要時間: $duration 秒"
    echo "作成されたパッケージ: $package_path"
}

# スクリプトの実行
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi