# Codest

プロジェクトのソースコードを1つのドキュメントにまとめるツール。

## インストール方法

1. [Releases](https://github.com/no-problem-dev/codest/releases) から最新の`codest-x.x.x.pkg`をダウンロード
2. ダウンロードしたpkgファイルをダブルクリック
3. インストーラーの指示に従ってインストール
4. ターミナルを再起動

## 使い方

```bash
# カレントディレクトリのコードをまとめる
codest .

# 出力ファイルを指定
codest . -o output.txt

# 最大ファイルサイズを指定（KB単位）
codest . --max-size 2000
```

## 特徴

- 指定したディレクトリ以下のソースコードを収集
- .gitignoreの設定を考慮
- 多様なプログラミング言語に対応
- マークダウン形式で出力
- 大きすぎるファイルを自動でスキップ

## サポート

問題や提案がある場合は[Issues](https://github.com/no-problem-dev/codest/issues)にお願いします。

## ライセンス

MIT License