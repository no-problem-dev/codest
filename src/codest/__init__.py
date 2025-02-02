"""
Codest - プロジェクトのソースコードを1つのドキュメントにまとめるツール
"""
from .document_generator import DocumentGenerator
from .exceptions import CodestError

__version__ = '0.1.0'
__all__ = ['DocumentGenerator', 'CodestError']

def main():
    from .cli import main
    return main()