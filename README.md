# Codest

プロジェクトのソースコードを1つのドキュメントにまとめるツール。

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
codest . -o output.txt

# クリップボードにコピー
codest . -c

# 最大ファイルサイズを指定（KB単位）
codest . --max-size 2000

# 詳細なログを表示
codest . -v
```

### 複数のディレクトリを指定

複数のディレクトリからソースコードを収集できます。カレントディレクトリ（`.`）と具体的なディレクトリを組み合わせることも可能です。

```bash
# 複数のディレクトリを指定
codest src tests docs

# カレントディレクトリと特定のディレクトリを組み合わせ
codest . src/frontend tests

# 相対パスと絶対パスの混在も可能
codest . ~/projects/shared-lib /opt/local/include
```

### 除外ディレクトリの指定

特定のディレクトリを収集対象から除外できます。

```bash
# 特定のディレクトリを除外
codest . --exclude build node_modules

# 複数のディレクトリの指定と除外を組み合わせ
codest src tests --exclude src/generated tests/fixtures
```

## 特徴

- 指定したディレクトリ以下のソースコードを収集
  - 複数のディレクトリを同時に指定可能
  - カレントディレクトリと特定のディレクトリの組み合わせをサポート
  - 除外ディレクトリの指定が可能
- .gitignoreの設定を考慮
- 多様なプログラミング言語に対応
- マークダウン形式で出力
- 大きすぎるファイルを自動でスキップ
- クリップボードへの直接コピーをサポート

## パスの取り扱い

- カレントディレクトリ（`.`）と具体的なパスは別々に処理されます
  - `codest . src`とした場合、カレントディレクトリと`src`ディレクトリの両方が対象になります
- 親子関係にあるディレクトリを指定した場合、親ディレクトリのみが使用されます
  - `codest src src/frontend`とした場合、`src`ディレクトリのみが対象になります
- 重複するパスは自動的に排除されます

## サポート

問題や提案がある場合は[Issues](https://github.com/no-problem-dev/codest/issues)にお願いします。

## ライセンス

MIT License