# scripts/env.sh
#!/bin/bash

# 環境変数のロード
load_env() {
    if [[ -f ".env" ]]; then
        echo "環境変数を .env からロードしています..."
        set -a
        source ".env"
        set +a
        return 0
    else
        echo "警告: .env ファイルが見つかりません"
        echo "以下の手順で設定してください:"
        echo "1. .env.example を .env にコピー"
        echo "2. .env ファイルを編集して必要な情報を設定"
        return 1
    fi
}

# エラーメッセージの表示
print_env_error() {
    cat << EOF
環境変数の設定が必要です。以下の手順で設定してください：

1. .env.exampleをコピーして.envファイルを作成
   cp .env.example .env

2. .envファイルを編集して必要な情報を設定
   - DEVELOPER_ID_INSTALLER: インストーラー署名用証明書の名前
   - NOTARY_PROFILE: 公証用のキーチェーンプロファイル名

3. キーチェーンプロファイルの設定
   xcrun notarytool store-credentials "CODEST_NOTARY" \\
       --apple-id "your.apple.id@example.com" \\
       --password "app-specific-password" \\
       --team-id "your-team-id"
EOF
}

# グローバル変数のエクスポート
export_env_vars() {
    export DEVELOPER_ID_INSTALLER
    export NOTARY_PROFILE
}