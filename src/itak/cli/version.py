import importlib.metadata


def get_iTaK_version() -> str:
    """Get the version number of iTaK running the CLI"""
    try:
        return importlib.metadata.version("itak")
    except importlib.metadata.PackageNotFoundError:
        return "0.1.0"  # Default version when not installed as package
