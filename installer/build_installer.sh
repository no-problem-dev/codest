#!/bin/bash

# エラー時に停止
set -e

# バージョン設定
VERSION="0.1.2"
IDENTIFIER="dev.noproblem.codest"

echo "🚀 Starting build process for Codest ${VERSION}..."

# ビルドディレクトリの作成
rm -rf build
mkdir -p build

# Pythonスクリプトとライブラリをパッケージディレクトリにコピー
echo "📦 Preparing package contents..."
mkdir -p package/usr/local/lib/codest

# ソースコードをコピー
cp -R ../src/codest package/usr/local/lib/codest/

# 実行スクリプトの作成
cat > package/usr/local/bin/codest << 'INNERSCRIPT'
#!/bin/bash
SCRIPT_DIR="/usr/local/lib/codest"
export PYTHONPATH="${SCRIPT_DIR}:${PYTHONPATH}"
python3 -m codest "$@"
INNERSCRIPT

chmod +x package/usr/local/bin/codest

# スクリプトに実行権限を付与
chmod +x scripts/*

echo "📝 Creating component package..."
# コンポーネントパッケージの作成と署名
pkgbuild \
    --root package \
    --scripts scripts \
    --identifier "$IDENTIFIER" \
    --version "$VERSION" \
    --install-location "/" \
    --sign "Developer ID Installer: Kyoichi Taniguchi (Y8MG29W5VM)" \
    build/codest-component.pkg

# Distribution XMLの作成
cat > build/distribution.xml << XMLEOF
<?xml version="1.0" encoding="utf-8"?>
<installer-script minSpecVersion="1.000000">
    <title>Codest ${VERSION}</title>
    <welcome file="welcome.txt"/>
    <readme file="readme.txt"/>
    <license file="license.txt"/>
    <conclusion file="conclusion.txt"/>
    <options customize="never" rootVolumeOnly="true"/>
    <choices-outline>
        <line choice="default"/>
    </choices-outline>
    <choice id="default" title="Codest">
        <pkg-ref id="${IDENTIFIER}"/>
    </choice>
    <pkg-ref id="${IDENTIFIER}" version="${VERSION}" auth="root">codest-component.pkg</pkg-ref>
</installer-script>
XMLEOF

echo "📄 Creating installer resources..."
# インストーラーリソースの作成
mkdir -p build/Resources
cat > build/Resources/welcome.txt << WELCOMEOF
Welcome to the Codest installer.

This will install Codest ${VERSION} on your computer.
WELCOMEOF

cat > build/Resources/readme.txt << READMEOF
Codest is a tool to collect source code files into a single document.

This tool helps you:
- Collect all source files from a directory
- Generate a single markdown document
- Respect .gitignore patterns
- Handle various programming languages
READMEOF

cat > build/Resources/conclusion.txt << CONCLUSIONEOF
Codest has been successfully installed!

You can now use the 'codest' command in your terminal.
Open a new terminal window to start using it.
CONCLUSIONEOF

# LICENSEファイルのコピー
cp ../LICENSE build/Resources/license.txt || echo "MIT License" > build/Resources/license.txt

echo "📦 Creating final installer package..."
# 最終的なインストーラーの作成と署名
productbuild \
    --distribution build/distribution.xml \
    --resources build/Resources \
    --package-path build \
    --version "$VERSION" \
    --sign "Developer ID Installer: Kyoichi Taniguchi (Y8MG29W5VM)" \
    "build/codest-${VERSION}.pkg"

echo "🔒 Submitting package for notarization..."
# パッケージの公証
xcrun notarytool submit "build/codest-${VERSION}.pkg" \
    --keychain-profile "CODEST_NOTARY" \
    --wait

echo "📍 Stapling notarization ticket..."
# 公証情報の添付
xcrun stapler staple "build/codest-${VERSION}.pkg"

echo "✨ Build complete! Signed and notarized installer package created at build/codest-${VERSION}.pkg"