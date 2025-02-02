class CodestError(Exception):
    """Base exception for all codest errors"""
    pass


class GitIgnoreError(CodestError):
    """Raised when there's an error processing .gitignore"""
    pass


class FileCollectionError(CodestError):
    """Raised when there's an error collecting files"""
    pass


class DocumentGenerationError(CodestError):
    """Raised when there's an error generating the document"""
    pass
