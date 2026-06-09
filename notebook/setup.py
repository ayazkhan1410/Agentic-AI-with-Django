import os
import pathlib
import sys

DJANGO_SETTINGS_MODULE = "aiengine.settings"


def _project_paths():
    repo_dir = pathlib.Path(__file__).resolve().parent.parent
    return repo_dir


def init(verbose=False):
    repo_dir = _project_paths()
    repo_dir_str = str(repo_dir)

    if repo_dir_str not in sys.path:
        sys.path.insert(0, repo_dir_str)

    os.chdir(repo_dir)

    if verbose:
        print(f"Project root: {repo_dir}")
        print(f"aiengine exists: {(repo_dir / 'aiengine').is_dir()}")

    if not (repo_dir / "aiengine").is_dir():
        raise RuntimeError(
            f"Cannot find Django project at {repo_dir}. "
            "Expected an 'aiengine' package next to the notebook/ folder."
        )

    try:
        import nest_asyncio

        nest_asyncio.apply()
        if verbose:
            print("Applied nest_asyncio patch for Jupyter compatibility")
    except ImportError:
        if verbose:
            print("nest_asyncio not available, skipping patch")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", DJANGO_SETTINGS_MODULE)
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

    import django
    from django.apps import apps

    if not apps.ready:
        django.setup()
        if verbose:
            print("Django setup complete")
    elif verbose:
        print("Django already configured")
