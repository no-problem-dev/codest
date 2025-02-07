# Codest

プロジェクトのソースコードを1つのマークダウンドキュメントにまとめるツール。

## インストール方法

1. [Releases](https://github.com/no-problem-dev/codest/releases) から最新の`codest-x.x.x.pkg`をダウンロード
2. ダウンロードしたpkgファイルをダブルクリック
3. インストーラーの指示に従ってインストール
4. ターミナルを再起動

## 使い方

### 基本的な使用方法

```bash
# カレントディレクトリのコードをまとめる
codest .

# 出力ファイルを指定
codest . -o output.md

# クリップボードにコピー
codest . -c

# 最大ファイルサイズを指定（KB単位）
codest . --max-size 2000

# 詳細なログを表示
codest . -v
```

### 複数のディレクトリを指定

複数のディレクトリからソースコードを収集できます：

```bash
# 複数のディレクトリを指定
codest src tests docs

# カレントディレクトリと特定のディレクトリを組み合わせ
codest . src/frontend tests

# 相対パスと絶対パスの混在も可能
codest . ~/projects/shared-lib /opt/local/include
```

### 除外ディレクトリの指定

特定のディレクトリを収集対象から除外できます：

```bash
# 特定のディレクトリを除外
codest . --exclude build node_modules

# 複数のディレクトリの指定と除外を組み合わせ
codest src tests --exclude src/generated tests/fixtures
```

## 出力形式

以下のような構造のマークダウンファイルが生成されます：

- トップレベルヘッダー: "Source Code Collection"
- メタ情報セクション
  - 生成日時
  - 処理されたファイル数
- ターゲットディレクトリのリスト
- 各ソースファイルのセクション
  - ファイルパスがヘッダーとして表示
  - 言語に応じたシンタックスハイライト
  - マークダウンファイルは折りたたみ表示

例：通常のソースファイル

```python
def main():
    print("Hello World")
```

例：マークダウンファイル

<details>
<summary>Markdown content (click to expand)</summary>

```markdown
# Project Overview
...
```

Rendered markdown:
# Project Overview
...

</details>

例：スキップされたファイル
```
⚠️ **File skipped**: Size (2048.0KB) exceeds limit of 1000KB
```

## 特徴

- マークダウン形式での出力
  - シンタックスハイライト付きのコードブロック
  - 折りたたみ可能なマークダウンコンテンツ
  - GitHubと互換性のある表示形式
- 複数のディレクトリをサポート
  - 複数のソースディレクトリの同時処理
  - 除外ディレクトリの指定
  - 相対パスと絶対パスの混在をサポート
- スマートなパス処理
  - 最適な相対パス表示
  - 重複パスの自動排除
  - ディレクトリ階層の明確な表示
- プロジェクト設定の考慮
  - .gitignoreの設定を反映
  - 大きなファイルの自動スキップ
  - 多様なプログラミング言語をサポート
- 柔軟な出力オプション
  - ファイルへの出力
  - クリップボードへのコピー
  - カスタマイズ可能なファイルサイズ制限

## サポートされるファイル形式

多様なファイル形式に対応し、適切なシンタックスハイライトを提供：

- プログラミング言語: Python, JavaScript, TypeScript, Ruby, Java, C/C++, Go, Rust, Swift など
- Web関連: HTML, CSS, SCSS, JavaScript, TypeScript
- 設定ファイル: JSON, YAML, TOML, INI
- ドキュメント: Markdown, Tex, XML
- その他: SQL, Shell Script, Apple固有の設定ファイルなど

## サポート

問題や提案がある場合は[Issues](https://github.com/no-problem-dev/codest/issues)にお願いします。

## ライセンス

MIT License