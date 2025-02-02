#!/bin/bash

source ./scripts/version.sh

# インストールスクリプトを作成
create_install_scripts() {
    local scripts_dir="$1"

    # preinstallスクリプトの作成
    cat > "$scripts_dir/preinstall" << 'EOF'
#!/bin/bash
echo "Cleaning up old installation..."
# 古いバージョンの削除
rm -rf /usr/local/lib/codest
rm -f /usr/local/bin/codest
EOF

    # postinstallスクリプトの作成
    cat > "$scripts_dir/postinstall" << 'EOF'
#!/bin/bash
echo "Starting installation..."

# 必要なライブラリのインストール
echo "Installing required packages..."
/usr/local/bin/pip3 install -q pyperclip>=1.8.0

# 権限の設定
echo "Setting permissions..."
chmod 755 /usr/local/bin/codest
chmod -R 755 /usr/local/lib/codest

echo "Installation completed successfully!"
EOF

    # スクリプトに実行権限を付与
    chmod 755 "$scripts_dir/preinstall" "$scripts_dir/postinstall"
}

# インストーラーパッケージを作成
create_installer_package() {
    local is_production="$1"
    local version
    version=$(get_version)
    local build_dir="build"
    local package_root="$build_dir/root"
    local package_name="codest-$version.pkg"
    local scripts_dir="$build_dir/scripts"
    local resources_dir="Resources"
    local component_pkg="$build_dir/codest-component.pkg"
    local distribution_xml="$build_dir/distribution.xml"

    echo "インストーラーパッケージを作成中..."

    # スクリプトディレクトリの作成
    mkdir -p "$scripts_dir"

    # インストールスクリプトの作成
    create_install_scripts "$scripts_dir"

    # コンポーネントパッケージの作成
    pkgbuild --root "$package_root" \
             --identifier "com.noproblem.codest" \
             --version "$version" \
             --scripts "$scripts_dir" \
             "$component_pkg"

    # distribution.xmlの生成
    cat > "$distribution_xml" << EOF
<?xml version="1.0" encoding="utf-8"?>
<installer-gui-script minSpecVersion="1">
    <title>Codest</title>
    <welcome file="welcome.txt"/>
    <license file="license.txt"/>
    <conclusion file="conclusion.txt"/>
    <domains enable_anywhere="false" enable_currentUserHome="false" enable_localSystem="true"/>
    <options customize="never" require-scripts="true" rootVolumeOnly="true"/>
    <choices-outline>
        <line choice="com.noproblem.codest"/>
    </choices-outline>
    <choice id="com.noproblem.codest" visible="true" title="Codest" description="Codestのインストール">
        <pkg-ref id="com.noproblem.codest"/>
    </choice>
    <pkg-ref id="com.noproblem.codest" version="$version">#codest-component.pkg</pkg-ref>
</installer-gui-script>
EOF

    # 製品アーカイブの作成
    if [ "$is_production" = true ]; then
        if [ -z "$DEVELOPER_ID_INSTALLER" ]; then
            echo "エラー: DEVELOPER_ID_INSTALLER が設定されていません"
            return 1
        fi
        echo "署名付きパッケージを作成中..."
        # 本番モード: 署名付きでビルド
        productbuild --distribution "$distribution_xml" \
                    --resources "$resources_dir" \
                    --package-path "$build_dir" \
                    --sign "$DEVELOPER_ID_INSTALLER" \
                    "$build_dir/$package_name"
    else
        echo "署名なしパッケージを作成中..."
        # 開発モード: 署名なしでビルド
        productbuild --distribution "$distribution_xml" \
                    --resources "$resources_dir" \
                    --package-path "$build_dir" \
                    "$build_dir/$package_name"
    fi

    if [ $? -eq 0 ]; then
        local package_path="$build_dir/$package_name"
        echo "インストーラーパッケージの作成が完了しました: $package_path"
        echo "$package_path"  # パスのみを返す
        return 0
    else
        echo "エラー: パッケージの作成に失敗しました" >&2
        return 1
    fi
}