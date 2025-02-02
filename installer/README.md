# installer

## 準備

### 環境設定ファイル

1. `.env.example`をコピーして`.env`を作成します：
```bash
cp .env.example .env
```

2. `.env`ファイルを編集し、必要な情報を設定：
```bash
# Apple Developer アカウント情報
DEVELOPER_ID_INSTALLER="Developer ID Installer: Your Name (XXXXXXXXXX)"

# キーチェーンプロファイル名
NOTARY_PROFILE="CODEST_NOTARY"
```

3. 公証用のキーチェーンプロファイルを設定：
```bash
xcrun notarytool store-credentials "CODEST_NOTARY" \
    --apple-id "your.apple.id@example.com" \
    --password "app-specific-password" \
    --team-id "your-team-id"
```

### ディレクトリ構造
```
installer/
├── .env            # 環境変数設定ファイル（.gitignoreに追加）
├── .env.example    # 環境変数設定例
├── Resources/      # インストーラーリソース
├── scripts/        # ビルドスクリプト
└── build_installer.sh  # メインビルドスクリプト
```

## ビルド方法

### 開発用ビルド（署名なし）
```bash
./build_installer.sh
```

### 本番用ビルド（署名・公証あり）
```bash
./build_installer.sh --production
```

### その他のオプション
```bash
# ヘルプの表示
./build_installer.sh --help

# バージョン情報の表示
./build_installer.sh --version

# デバッグモードでビルド
./build_installer.sh --debug
```

## トラブルシューティング

### 証明書の確認
```bash
# 利用可能な証明書の一覧を表示
security find-identity -v -p codesigning
```

### 公証の確認
```bash
# パッケージの公証状態を確認
xcrun stapler validate "build/codest-x.x.x.pkg"
```