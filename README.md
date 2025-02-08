# Codest

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub release](https://img.shields.io/github/v/release/no-problem-dev/codest)](https://github.com/no-problem-dev/codest/releases)
[![GitHub issues](https://img.shields.io/github/issues/no-problem-dev/codest)](https://github.com/no-problem-dev/codest/issues)

</div>

プロジェクトのソースコードを1つのマークダウンドキュメントにまとめるツール。AI解析やドキュメント生成のための前処理として、またはプロジェクト全体の把握に役立ちます。

## 🌟 主な特徴

- **スマートな収集機能**
  - 複数のディレクトリから同時収集
  - `.gitignore`の設定を自動反映
  - 柔軟なファイル除外オプション
  - 相対パスと絶対パスの混在をサポート

- **最適化された出力**
  - シンタックスハイライト付きのコードブロック
  - 折りたたみ可能なマークダウンコンテンツ
  - GitHubと完全互換の表示形式
  - 大きなファイルの自動スキップ

- **使いやすい設計**
  - シンプルなコマンドライン操作
  - ファイル出力とクリップボードコピーの選択
  - カスタマイズ可能なサイズ制限
  - 豊富なログオプション

## 🚀 インストール方法

### macOSの場合

1. [Releases](https://github.com/no-problem-dev/codest/releases)から最新の`codest-x.x.x.pkg`をダウンロード
2. ダウンロードしたpkgファイルをダブルクリック
3. インストーラーの指示に従ってインストール
4. ターミナルを再起動

### その他の環境（Pythonパッケージとして）

```bash
pip install git+https://github.com/no-problem-dev/codest.git
```

## 💡 使用例

### 基本的な使い方

```bash
# カレントディレクトリのコードをまとめる
codest .

# 出力ファイルを指定
codest . -o project_source.md

# クリップボードにコピー
codest . -c

# 最大ファイルサイズを指定（KB単位）
codest . --max-size 2000

# 詳細なログを表示
codest . -v
```

### 高度な使用例

```bash
# 複数のディレクトリを指定
codest src tests docs

# 特定のディレクトリを除外
codest . --exclude build node_modules

# カレントディレクトリと特定のディレクトリを組み合わせ
codest . src/frontend tests

# 相対パスと絶対パスの混在
codest . ~/projects/shared-lib /opt/local/include
```

## 📄 出力形式

生成されるドキュメントは、以下の階層構造で整理されます：

| セクション | 説明 | 表示内容 |
|------------|------|----------|
| Source Code Collection | トップレベルヘッダー | プロジェクト全体のタイトル |
| Meta Information | 生成情報 | 生成日時、処理ファイル数 |
| Target Directories | 対象ディレクトリ | 収集元ディレクトリのリスト |
| Source Files | ソースコード | 各ファイルの内容（シンタックスハイライト付き） |

### 特記事項

- 各ソースファイルは言語に応じたシンタックスハイライトが適用されます
- マークダウンファイルは折りたたみ可能な形式で表示されます
- ファイルサイズ制限を超えるファイルは自動的にスキップされ、警告が表示されます
- 相対パスでファイル名が表示され、ディレクトリ構造が把握しやすくなっています

## 🔧 サポートされるファイル形式

### プログラミング言語
- **汎用言語**: Python, JavaScript, TypeScript, Ruby, Java, C/C++, Go, Rust
- **iOS/Mac開発**: Swift, Objective-C
- **Webフロントエンド**: HTML, CSS, SCSS, JSX, TSX
- **その他**: SQL, Shell Script, R, Kotlin, Lua

### 設定・ドキュメント
- **設定ファイル**: JSON, YAML, TOML, INI
- **ドキュメント**: Markdown, Tex, XML
- **Apple固有**: .strings, .stringsdict, .entitlements, .xcconfig, .plist

## 🤝 コントリビューション

1. このリポジトリをフォーク
2. 新しいブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチをプッシュ (`git push origin feature/amazing-feature`)
5. Pull Requestを作成

## 📝 今後の予定

- [ ] AIツール分析用の出力最適化
  - GPT対応のコンテキストウィンドウに最適化された出力形式
  - ファイルサイズとトークン数の効率的な制御
  - メタデータの強化と構造化

## 💬 サポート

- 問題報告や機能リクエストは[Issues](https://github.com/no-problem-dev/codest/issues)までお願いします
- 使用方法の質問は[Discussions](https://github.com/no-problem-dev/codest/discussions)をご利用ください

## 📜 ライセンス

このプロジェクトは[MIT License](LICENSE)のもとで公開されています。

---

<div align="center">
Made with ❤️ by <a href="https://github.com/no-problem-dev">NOPROBLEM DEV</a>
</div>