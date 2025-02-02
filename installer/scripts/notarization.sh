#!/bin/bash

# 公証処理を実行する
notarize_package() {
    local package_path="$1"
    local bundle_id="$2"
    local username="$3"
    local password="$4"
    local team_id="$5"

    # パッケージパスから余分な出力を削除
    package_path=$(echo "$package_path" | tail -n 1)

    echo "パッケージの公証を開始します..."

    if [ ! -f "$package_path" ]; then
        echo "エラー: パッケージファイルが見つかりません: $package_path"
        return 1
    fi

    echo "🔒 パッケージを公証に提出中: $package_path"

    # キーチェーンプロファイルを使用して公証
    if ! xcrun notarytool submit "$package_path" \
        --keychain-profile "CODEST_NOTARY" \
        --wait; then
        echo "エラー: 公証の提出に失敗しました"
        return 1
    fi

    echo "✅ 公証が完了しました"
    return 0
}

# 公証チケットの添付
attach_notarization_ticket() {
    local package_path="$1"
    # パッケージパスから余分な出力を削除
    package_path=$(echo "$package_path" | tail -n 1)

    echo "📍 公証チケットを添付中: $package_path"
    if xcrun stapler staple "$package_path"; then
        echo "✨ 公証チケットの添付が完了しました"
        return 0
    else
        echo "エラー: 公証チケットの添付に失敗しました"
        return 1
    fi
}