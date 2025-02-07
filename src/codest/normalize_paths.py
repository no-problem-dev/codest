import logging
import os
from typing import List, Union

PathLike = Union[str, bytes, os.PathLike]

logger = logging.getLogger(__name__)


def normalize_paths(directories: List[PathLike]) -> List[str]:
    """
    ディレクトリパスを正規化し、重複と包含関係を排除

    Args:
        directories (List[PathLike]): ディレクトリパスのリスト

    Returns:
        List[str]: 正規化され重複が排除されたパスのリスト
    """
    # すべてのパスを絶対パスに変換
    abs_paths = set()  # 重複を自動的に排除するためにsetを使用
    cwd = os.getcwd()

    # カレントディレクトリのフラグ
    has_current_dir = False

    for path in directories:
        path_str = str(path)

        # カレントディレクトリの特別処理
        if path_str == '.':
            has_current_dir = True
            abs_paths.add(cwd)
            continue

        # 相対パスを絶対パスに変換（単純な結合のみ）
        if not os.path.isabs(path_str):
            abs_path = os.path.abspath(os.path.join(cwd, path_str))
        else:
            abs_path = path_str

        abs_paths.add(abs_path)

    # リストに変換
    unique_paths = list(abs_paths)

    # 親子関係のチェックと排除
    result = []
    for path1 in sorted(unique_paths, key=len, reverse=True):  # 長いパスから処理
        # カレントディレクトリは常に残す
        if path1 == cwd and has_current_dir:
            result.append(path1)
            continue

        # path1が他のパスの子ディレクトリでない場合、または
        # 親がカレントディレクトリの場合は追加
        is_child = False
        for path2 in unique_paths:
            if path1 != path2:
                try:
                    rel_path = os.path.relpath(path1, path2)
                    # カレントディレクトリが指定されている場合は、
                    # カレントディレクトリの直下のパスは別パスとして扱う
                    if path2 == cwd and has_current_dir:
                        continue
                    # 相対パスが'..'で始まらず、かつ'.'でもない場合は子ディレクトリ
                    if not rel_path.startswith('..') and rel_path != '.':
                        is_child = True
                        break
                except ValueError:
                    # 異なるドライブの場合などはスキップ
                    continue
        if not is_child:
            result.append(path1)

    # 結果を長さでソート（一貫性のため）
    return sorted(result, key=len)


def is_subdirectory(parent: PathLike, child: PathLike) -> bool:
    """
    子ディレクトリが親ディレクトリの配下にあるかチェック

    Args:
        parent (PathLike): 親ディレクトリのパス
        child (PathLike): 子ディレクトリのパス

    Returns:
        bool: childがparentの子ディレクトリの場合True
    """
    try:
        parent_path = os.path.abspath(str(parent))
        child_path = os.path.abspath(str(child))

        if parent_path == child_path:
            return False

        # 相対パスを計算してチェック
        rel_path = os.path.relpath(child_path, parent_path)

        # 相対パスが'..'で始まらず、かつパスが同一でない場合のみTrue
        return not rel_path.startswith('..') and rel_path != '.'
    except (ValueError, OSError):
        return False