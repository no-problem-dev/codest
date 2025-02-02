#!/bin/bash

# 本番環境の検証
validate_production_environment() {
    echo "本番環境の検証を開始します..."
    local missing_vars=()

    # 必要な環境変数のチェック
    declare -a required_vars=(
        "DEVELOPER_ID_APPLICATION"
        "DEVELOPER_ID_INSTALLER"
        "APPLE_ID"
        "APPLE_ID_PASS"
        "TEAM_ID"
    )

    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            missing_vars+=("$var")
        fi
    done

    if [ ${#missing_vars[@]} -gt 0 ]; then
        echo "以下の環境変数が設定されていません："
        printf '%s\n' "${missing_vars[@]}"
        echo ""
        echo "環境変数の設定例："
        echo 'export DEVELOPER_ID_APPLICATION="Developer ID Application: Your Name (XXXXXXXXXX)"'
        echo 'export DEVELOPER_ID_INSTALLER="Developer ID Installer: Your Name (XXXXXXXXXX)"'
        echo 'export APPLE_ID="your.apple.id@example.com"'
        echo 'export APPLE_ID_PASS="app-specific-password"'
        echo 'export TEAM_ID="your-team-id"'
        echo ""
        echo "証明書情報の確認方法："
        echo "security find-identity -v -p codesigning"
        return 1
    fi

    # 証明書の存在確認
    local cert_count
    cert_count=$(security find-identity -v -p codesigning | grep -c "Developer ID Application")

    if [ "$cert_count" -eq 0 ]; then
        echo "警告: Developer ID Application証明書が見つかりません"
        echo "以下のコマンドで利用可能な証明書を確認できます："
        echo "security find-identity -v -p codesigning"
        echo ""
        echo "証明書がない場合は、Apple Developer Programに登録し、"
        echo "証明書を作成してください。"
        return 1
    fi

    return 0
}

# 開発環境の検証
validate_build_environment() {
    local errors=0

    # pkgbuildが利用可能か確認
    if ! command -v pkgbuild > /dev/null 2>&1; then
        echo "エラー: pkgbuildが見つかりません"
        echo "Command Line Tools for Xcode をインストールしてください"
        errors=$((errors + 1))
    fi

    # productbuildが利用可能か確認
    if ! command -v productbuild > /dev/null 2>&1; then
        echo "エラー: productbuildが見つかりません"
        echo "Command Line Tools for Xcode をインストールしてください"
        errors=$((errors + 1))
    fi

    # 必要なディレクトリが存在するか確認
    if [ ! -d "../src/codest" ]; then
        echo "エラー: ソースディレクトリ(src/codest)が見つかりません"
        errors=$((errors + 1))
    fi

    if [ ! -f "../setup.py" ]; then
        echo "エラー: setup.pyが見つかりません"
        errors=$((errors + 1))
    fi

    # エラーがある場合は終了
    if [ $errors -gt 0 ]; then
        echo "エラー: 必要な環境が整っていません"
        return 1
    fi

    return 0
}

# 公証環境の検証
validate_notarization_environment() {
    echo "公証環境を検証中..."
    local errors=0

    # 必要なツールの確認
    if ! command -v xcrun > /dev/null 2>&1; then
        echo "エラー: xcrunが見つかりません"
        echo "Command Line Tools for Xcode をインストールしてください"
        errors=$((errors + 1))
    fi

    if ! command -v stapler > /dev/null 2>&1; then
        echo "エラー: staplerが見つかりません"
        errors=$((errors + 1))
    fi

    # エラーがある場合は終了
    if [ $errors -gt 0 ]; then
        echo "エラー: 公証に必要なツールが不足しています"
        return 1
    fi

    return 0
}