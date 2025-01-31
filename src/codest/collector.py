import os
import logging
from datetime import datetime
from typing import List, Set
from pathlib import Path
import fnmatch

# ロギングの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def parse_gitignore(root_dir: str) -> Set[str]:
    """
    .gitignoreファイルを解析し、除外パターンのセットを返します
    """
    gitignore_patterns = set()
    gitignore_path = os.path.join(root_dir, '.gitignore')
    
    if not os.path.exists(gitignore_path):
        logger.debug("No .gitignore file found")
        return gitignore_patterns
    
    try:
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if line.startswith('/'):
                        line = line[1:]
                    if line.endswith('/'):
                        line = line[:-1]
                    gitignore_patterns.add(line)
        
        logger.debug(f"Loaded {len(gitignore_patterns)} patterns from .gitignore")
    except Exception as e:
        logger.error(f"Error reading .gitignore: {str(e)}")
    
    return gitignore_patterns

def should_ignore(path: str, root_dir: str, ignore_patterns: Set[str], ignore_dirs: Set[str], gitignore_patterns: Set[str]) -> bool:
    """
    指定されたパスを無視すべきかどうかを判定します
    """
    rel_path = os.path.relpath(path, root_dir)
    parts = path.split(os.sep)
    
    if any(part in ignore_dirs for part in parts):
        logger.debug(f"Ignoring directory: {path}")
        return True
    
    if any(pattern in path for pattern in ignore_patterns):
        logger.debug(f"Ignoring file due to pattern match: {path}")
        return True
    
    for pattern in gitignore_patterns:
        if pattern.endswith('/'):
            if any(part == pattern[:-1] for part in parts):
                return True
        if fnmatch.fnmatch(rel_path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
            logger.debug(f"Ignoring file due to .gitignore pattern '{pattern}': {path}")
            return True
    
    return False

def collect_source_files(
    root_dir: str,
    ignore_patterns: Set[str] = {
        '.git', '__pycache__', '.pyc', '.env', '.venv', 'node_modules',
        '.idea', '.vscode', '.vs', '*.suo', '*.user', '*.userosscache', '*.sln.docstates',
        '*.xcuserstate', '*.xcuserdatad', '*.xccheckout', '*.xcscmblueprint',
        'xcuserdata', 'DerivedData', '.build', 'Pods',
        'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml', 'composer.lock',
        'dist', 'build', 'out', 'bin', 'obj',
        '.cache', '.temp', '.tmp', '.sass-cache',
        '*.log', 'logs', 'npm-debug.log*', 'yarn-debug.log*', 'yarn-error.log*',
        '.DS_Store', 'Thumbs.db', '*.swp', '*.bak', '*.backup'
    },
    ignore_dirs: Set[str] = {
        '.git', '__pycache__', 'node_modules', 'venv', '.venv',
        '.idea', '.vscode', '.vs',
        'DerivedData', '.build', 'Pods', 'xcuserdata',
        'dist', 'build', 'out', 'bin', 'obj',
        '.cache', '.temp', '.tmp', '.sass-cache',
        'bower_components', 'jspm_packages',
        'logs'
    },
    file_extensions: Set[str] = {
        '.swift', '.strings', '.stringsdict', '.entitlements', '.xcconfig', '.plist',
        '.py', '.js', '.tsx', '.ts', '.jsx', '.java',
        '.cpp', '.h', '.hpp', '.c', '.cs', '.go', '.rs', '.rb',
        '.md', '.tex', '.html', '.css', '.scss',
        '.json', '.yml', '.yaml', '.xml'
    }
) -> List[str]:
    """
    指定されたディレクトリ以下のソースファイルを収集します
    """
    if not os.path.exists(root_dir):
        raise FileNotFoundError(f"Directory not found: {root_dir}")
    
    if not os.path.isdir(root_dir):
        raise NotADirectoryError(f"Path is not a directory: {root_dir}")
    
    logger.info(f"Starting to collect files from: {root_dir}")
    logger.debug(f"File extensions to collect: {file_extensions}")
    
    gitignore_patterns = parse_gitignore(root_dir)
    source_files = []
    
    try:
        for dirpath, dirnames, filenames in os.walk(root_dir):
            logger.debug(f"Scanning directory: {dirpath}")
            if should_ignore(dirpath, root_dir, ignore_patterns, ignore_dirs, gitignore_patterns):
                dirnames.clear()
                continue
                
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                if any(filename.endswith(ext) for ext in file_extensions):
                    if not should_ignore(full_path, root_dir, ignore_patterns, ignore_dirs, gitignore_patterns):
                        logger.debug(f"Found source file: {full_path}")
                        source_files.append(full_path)
    except Exception as e:
        logger.error(f"Error while walking directory: {str(e)}")
        raise
    
    logger.info(f"Found {len(source_files)} source files")
    return sorted(source_files)

def create_source_document(
    root_dir: str,
    output_file: str = None,
    max_file_size_kb: int = 1000
) -> None:
    """
    ソースコードをまとめたドキュメントを生成します
    """
    try:
        root_dir = os.path.abspath(root_dir)
        logger.info(f"Using absolute path: {root_dir}")
        
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f'source_code_{timestamp}.txt'
        
        logger.info(f"Output will be written to: {output_file}")
        source_files = collect_source_files(root_dir)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Project Source Code Collection\n")
            f.write(f"# Generated at: {datetime.now().isoformat()}\n")
            f.write(f"# Root directory: {root_dir}\n")
            f.write(f"# Total files found: {len(source_files)}\n\n")
            
            for file_path in source_files:
                rel_path = os.path.relpath(file_path, root_dir)
                logger.debug(f"Processing file: {rel_path}")
                
                file_size_kb = os.path.getsize(file_path) / 1024
                if file_size_kb > max_file_size_kb:
                    logger.warning(f"Skipping large file: {rel_path} ({file_size_kb:.1f}KB)")
                    f.write(f"\n### File: {rel_path}\n")
                    f.write(f"# [SKIPPED] File size ({file_size_kb:.1f}KB) exceeds limit of {max_file_size_kb}KB\n\n")
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as source_file:
                        content = source_file.read()
                        f.write(f"\n### File: {rel_path}\n")
                        f.write("```" + os.path.splitext(file_path)[1][1:] + "\n")
                        f.write(content)
                        f.write("\n```\n")
                except Exception as e:
                    logger.error(f"Error reading file {rel_path}: {str(e)}")
                    f.write(f"\n### File: {rel_path}\n")
                    f.write(f"# [ERROR] Failed to read file: {str(e)}\n\n")
        
        logger.info(f"Successfully created source code collection: {output_file}")
        
    except Exception as e:
        logger.error(f"Error creating source document: {str(e)}")
        raise
