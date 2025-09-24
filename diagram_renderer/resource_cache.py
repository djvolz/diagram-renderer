"""
Resource caching system for static files and templates.

This module provides efficient caching of frequently accessed resources
to improve rendering performance.
"""

import importlib.resources
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class ResourceCache:
    """Manages cached loading of static resources and templates."""

    def __init__(self) -> None:
        """Initialize the resource cache."""
        self._cache: dict[str, str] = {}
        self._not_found: set[str] = set()

    def clear(self) -> None:
        """Clear all cached resources."""
        self._cache.clear()
        self._not_found.clear()

    def get_resource(
        self,
        resource_type: str,
        filename: str,
        package: str = "diagram_renderer.renderers",
        fallback_paths: Optional[list[Path]] = None,
    ) -> Optional[str]:
        """
        Get a resource file content with caching.

        Args:
            resource_type: Type of resource ('templates' or 'static/js')
            filename: Name of the file to load
            package: Package containing the resource
            fallback_paths: Optional list of paths to try if package resource fails

        Returns:
            File content as string, or None if not found
        """
        cache_key = f"{package}:{resource_type}:{filename}"

        # Check if already cached
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Check if previously not found
        if cache_key in self._not_found:
            return None

        # Try loading the resource
        content = self._load_resource(resource_type, filename, package, fallback_paths)

        if content:
            self._cache[cache_key] = content
            logger.debug(f"Cached resource: {cache_key}")
        else:
            self._not_found.add(cache_key)
            logger.debug(f"Resource not found: {cache_key}")

        return content

    def _load_resource(
        self,
        resource_type: str,
        filename: str,
        package: str,
        fallback_paths: Optional[list[Path]] = None,
    ) -> Optional[str]:
        """
        Load a resource from various sources.

        Args:
            resource_type: Type of resource
            filename: Name of the file
            package: Package containing the resource
            fallback_paths: Optional fallback paths

        Returns:
            File content or None
        """
        # Try importlib.resources first (recommended approach)
        content = self._try_importlib_resources(package, resource_type, filename)
        if content:
            return content

        # Try fallback paths if provided
        if fallback_paths:
            content = self._try_fallback_paths(fallback_paths, filename)
            if content:
                return content

        # Try legacy __file__ approach as last resort
        content = self._try_legacy_path(package, resource_type, filename)
        if content:
            return content

        return None

    def _try_importlib_resources(
        self, package: str, resource_type: str, filename: str
    ) -> Optional[str]:
        """Try loading resource using importlib.resources."""
        try:
            # For Python 3.9+
            if hasattr(importlib.resources, "files"):
                files = importlib.resources.files(package)
                resource_path = files / resource_type / filename
                if resource_path.is_file():
                    return resource_path.read_text(encoding="utf-8")
            else:
                # Fallback for Python 3.8
                with importlib.resources.path(package, resource_type) as base_path:
                    file_path = base_path / filename
                    if file_path.exists():
                        return file_path.read_text(encoding="utf-8")
        except Exception as e:
            logger.debug(f"importlib.resources failed: {e}")

        return None

    def _try_fallback_paths(self, paths: list[Path], filename: str) -> Optional[str]:
        """Try loading resource from fallback paths."""
        for base_path in paths:
            try:
                file_path = base_path / filename
                if file_path.exists():
                    return file_path.read_text(encoding="utf-8")
            except Exception as e:
                logger.debug(f"Fallback path {base_path} failed: {e}")

        return None

    def _try_legacy_path(self, package: str, resource_type: str, filename: str) -> Optional[str]:
        """Try loading resource using legacy __file__ approach."""
        try:
            import importlib.util

            spec = importlib.util.find_spec(package)
            if spec and spec.origin:
                base_path = Path(spec.origin).parent / resource_type
                file_path = base_path / filename
                if file_path.exists():
                    return file_path.read_text(encoding="utf-8")
        except Exception as e:
            logger.debug(f"Legacy path approach failed: {e}")

        return None


# Global cache instance
_global_cache = ResourceCache()


def get_cached_resource(
    resource_type: str,
    filename: str,
    package: str = "diagram_renderer.renderers",
    fallback_paths: Optional[list[Path]] = None,
) -> Optional[str]:
    """
    Get a cached resource using the global cache.

    Args:
        resource_type: Type of resource ('templates' or 'static/js')
        filename: Name of the file to load
        package: Package containing the resource
        fallback_paths: Optional list of paths to try

    Returns:
        File content as string, or None if not found
    """
    return _global_cache.get_resource(resource_type, filename, package, fallback_paths)


def clear_cache() -> None:
    """Clear the global resource cache."""
    _global_cache.clear()
