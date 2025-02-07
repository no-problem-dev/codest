"""定数定義モジュール"""

# ファイル収集の際に使用する拡張子の定義
DEFAULT_FILE_EXTENSIONS = {
    '.swift', '.strings', '.stringsdict', '.entitlements', '.xcconfig', '.plist',
    '.py', '.js', '.tsx', '.ts', '.jsx', '.java',
    '.cpp', '.h', '.hpp', '.c', '.cs', '.go', '.rs', '.rb',
    '.md', '.tex', '.html', '.css', '.scss',
    '.json', '.yml', '.yaml', '.xml'
}

# 拡張子とマークダウンでの言語指定の対応
MARKDOWN_LANGUAGE_MAP = {
    # Python
    '.py': 'python',
    '.pyi': 'python',
    '.pyw': 'python',
    '.ipynb': 'python',

    # JavaScript/TypeScript
    '.js': 'javascript',
    '.jsx': 'jsx',
    '.ts': 'typescript',
    '.tsx': 'tsx',

    # Ruby
    '.rb': 'ruby',
    '.rake': 'ruby',
    '.gemspec': 'ruby',

    # Java
    '.java': 'java',
    '.gradle': 'groovy',

    # C/C++
    '.c': 'c',
    '.h': 'c',
    '.cpp': 'cpp',
    '.hpp': 'cpp',
    '.cc': 'cpp',

    # C#
    '.cs': 'csharp',

    # Go
    '.go': 'go',

    # Rust
    '.rs': 'rust',

    # Swift
    '.swift': 'swift',

    # Web
    '.html': 'html',
    '.htm': 'html',
    '.css': 'css',
    '.scss': 'scss',
    '.sass': 'sass',
    '.less': 'less',

    # Configuration
    '.json': 'json',
    '.yaml': 'yaml',
    '.yml': 'yaml',
    '.toml': 'toml',
    '.ini': 'ini',
    '.conf': 'conf',

    # Shell
    '.sh': 'bash',
    '.bash': 'bash',
    '.zsh': 'bash',
    '.fish': 'fish',

    # Documentation
    '.md': 'markdown',
    '.markdown': 'markdown',
    '.tex': 'tex',
    '.xml': 'xml',
    '.svg': 'svg',

    # Apple specific
    '.strings': 'swift',
    '.stringsdict': 'xml',
    '.entitlements': 'xml',
    '.xcconfig': 'xcconfig',
    '.plist': 'xml',

    # その他
    '.sql': 'sql',
    '.r': 'r',
    '.php': 'php',
    '.pl': 'perl',
    '.kt': 'kotlin',
    '.kts': 'kotlin',
    '.lua': 'lua',
    '.elm': 'elm',
    '.hs': 'haskell',
    '.fs': 'fsharp',
    '.fsx': 'fsharp',
    '.dart': 'dart',
}

# デフォルトで無視するディレクトリ
DEFAULT_IGNORE_DIRS = {
    '.git', '__pycache__', 'node_modules', 'venv', '.venv',
    '.idea', '.vscode', '.vs',
    'DerivedData', '.build', 'Pods', 'xcuserdata',
    'dist', 'build', 'out', 'bin', 'obj',
    '.cache', '.temp', '.tmp', '.sass-cache',
    'bower_components', 'jspm_packages',
    'logs'
}

# デフォルトで無視するパターン
DEFAULT_IGNORE_PATTERNS = {
    '.git', '__pycache__', '.pyc', '.env', '.venv', 'node_modules',
    '.idea', '.vscode', '.vs', '*.suo', '*.user', '*.userosscache', '*.sln.docstates',
    '*.xcuserstate', '*.xcuserdatad', '*.xccheckout', '*.xcscmblueprint',
    'xcuserdata', 'DerivedData', '.build', 'Pods',
    'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'composer.lock',
    'dist', 'build', 'out', 'bin', 'obj',
    '.cache', '.temp', '.tmp', '.sass-cache',
    '*.log', 'logs', 'npm-debug.log*', 'yarn-debug.log*', 'yarn-error.log*',
    '.DS_Store', 'Thumbs.db', '*.swp', '*.bak', '*.backup'
}