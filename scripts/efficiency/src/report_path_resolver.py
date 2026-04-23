#! /usr/bin/python

"""Utility helpers for locating efficiency report files with tape/tar fallbacks."""

import glob
import os
import shutil
import subprocess
import tarfile


def _stage_from_tape(cache_path, debug=False):
    """Attempt to stage a file from tape when the path lives under /cache/."""
    if "/cache/" not in cache_path:
        return False

    staged = False
    for command in ("srmGet", "jget"):
        if shutil.which(command) is None:
            continue
        if debug:
            print("[report_path_resolver] Attempting tape stage with {} {}".format(command, cache_path))
        result = subprocess.run([command, cache_path], check=False, capture_output=True, text=True)
        if debug and result.stdout:
            print(result.stdout.strip())
        if debug and result.stderr:
            print(result.stderr.strip())
        if result.returncode == 0:
            staged = True
            break

    return staged


def _find_tar_candidates(search_roots):
    patterns = ("*.tar", "*.tar.gz", "*.tgz")
    candidates = []
    seen = set()
    for root in search_roots:
        if not root or not os.path.isdir(root):
            continue
        for pattern in patterns:
            for match in glob.glob(os.path.join(root, "**", pattern), recursive=True):
                if match not in seen:
                    seen.add(match)
                    candidates.append(match)
    return candidates


def _extract_report_from_tar(tar_path, report_name, extract_dir, debug=False):
    try:
        with tarfile.open(tar_path) as tar_handle:
            members = tar_handle.getmembers()
            if not any(os.path.basename(member.name) == report_name for member in members):
                return None
            tar_handle.extractall(path=extract_dir)
    except (tarfile.TarError, OSError) as err:
        if debug:
            print("[report_path_resolver] Failed to extract {} ({})".format(tar_path, err))
        return None

    for root, _, files in os.walk(extract_dir):
        if report_name in files:
            return os.path.join(root, report_name)

    return None


def resolve_report_path(utilpath, root_prefix, run_num, max_event, outpath=None, debug=False):
    """Resolve path to a report file with /cache/ tape and tar extraction fallback."""
    report_rel = os.path.join("Analysis", "General", "{}_{}_{}.report".format(root_prefix, run_num, max_event))
    report_root = os.path.join(utilpath, "REPORT_OUTPUT")
    report_path = os.path.join(report_root, report_rel)

    if os.path.isfile(report_path):
        return report_path

    if "/cache/" in report_path:
        _stage_from_tape(report_path, debug=debug)
        if os.path.isfile(report_path):
            return report_path

    fallback_root = os.path.join(outpath or utilpath, "REPORT_OUTPUT_FALLBACK")
    os.makedirs(fallback_root, exist_ok=True)

    search_roots = [
        os.path.dirname(report_path),
        report_root,
        utilpath,
        outpath,
    ]
    tar_candidates = _find_tar_candidates(search_roots)

    report_name = os.path.basename(report_path)
    for tar_candidate in tar_candidates:
        extracted_report = _extract_report_from_tar(tar_candidate, report_name, fallback_root, debug=debug)
        if extracted_report and os.path.isfile(extracted_report):
            if debug:
                print("[report_path_resolver] Resolved report from {}".format(tar_candidate))
            return extracted_report

    raise FileNotFoundError(
        "Could not locate report {}. Checked standard path, tape staging for /cache/, and tar fallback.".format(report_name)
    )
