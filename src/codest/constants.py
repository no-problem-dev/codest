"""定数定義モジュール"""
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

DEFAULT_IGNORE_DIRS = {
    '.git', '__pycache__', 'node_modules', 'venv', '.venv',
    '.idea', '.vscode', '.vs',
    'DerivedData', '.build', 'Pods', 'xcuserdata',
    'dist', 'build', 'out', 'bin', 'obj',
    '.cache', '.temp', '.tmp', '.sass-cache',
    'bower_components', 'jspm_packages',
    'logs'
}

DEFAULT_FILE_EXTENSIONS = {
    '.swift', '.strings', '.stringsdict', '.entitlements', '.xcconfig', '.plist',
    '.py', '.js', '.tsx', '.ts', '.jsx', '.java',
    '.cpp', '.h', '.hpp', '.c', '.cs', '.go', '.rs', '.rb',
    '.md', '.tex', '.html', '.css', '.scss',
    '.json', '.yml', '.yaml', '.xml'
}