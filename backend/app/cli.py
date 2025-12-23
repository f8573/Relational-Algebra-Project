"""Additional CLI helpers for the application."""
import os
import shutil


def init_bank_db(sample_path=None):
    """Ensure a `bank.db` exists in the backend folder.

    If `sample_path` is provided it will be copied into place. Otherwise
    a zero-byte sqlite file is created as a placeholder.
    """
    backend_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
    target = os.path.join(backend_dir, "bank.db")

    if os.path.exists(target):
        return target

    if sample_path and os.path.exists(sample_path):
        shutil.copy(sample_path, target)
        return target

    # create an empty sqlite file
    open(target, "a").close()
    return target
