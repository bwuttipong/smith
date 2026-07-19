#!/usr/bin/env python3
"""
smoke_test.py — Submit a minimal ComfyUI workflow to verify the server
accepts jobs, then immediately cancel it to avoid burning GPU time.

Standalone usage:
    python3 smoke_test.py
    python3 smoke_test.py --host https://cloud.comfy.org
    python3 smoke_test.py --ckpt model.safetensors

Also importable:
    from smoke_test import run_smoke_test
    result = run_smoke_test("http://127.0.0.1:8188", api_key=None, ckpt_name="model.safetensors")
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (  # noqa: E402
    DEFAULT_LOCAL_HOST, ENV_API_KEY, emit_json, resolve_api_key, resolve_url,
)

# Minimal SD1.5 workflow — 256×256, 1 step, no rare nodes.
# Small enough to validate submission without triggering SDXL/Flux checks.
_SMOKE_WORKFLOW: dict = {
    "3": {
        "class_type": "KSampler",
        "inputs": {
            "seed": 1, "steps": 1, "cfg": 7.0,
            "sampler_name": "euler", "scheduler": "normal", "denoise": 1.0,
            "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0],
            "latent_image": ["5", 0],
        },
    },
    "4": {"class_type": "CheckpointLoaderSimple",
          "inputs": {"ckpt_name": "REPLACE_ME"}},
    "5": {"class_type": "EmptyLatentImage",
          "inputs": {"width": 256, "height": 256, "batch_size": 1}},
    "6": {"class_type": "CLIPTextEncode",
          "inputs": {"text": "test", "clip": ["4", 1]}},
    "7": {"class_type": "CLIPTextEncode",
          "inputs": {"text": "", "clip": ["4", 1]}},
    "9": {"class_type": "SaveImage",
          "inputs": {"filename_prefix": "smoke", "images": ["3", 0]}},
}


def run_smoke_test(
    host: str,
    *,
    api_key: str | None = None,
    ckpt_name: str | None = None,
) -> dict:
    """Submit the minimal workflow and cancel it right after acceptance.

    Returns a dict with keys:
        ran             – bool, whether we attempted submission
        submitted       – bool, whether the server accepted the job
        prompt_id       – str | None, the job ID if accepted
        cancelled_after_submit – bool | None, whether cancel succeeded
        reason          – str | None, why we didn't run (no checkpoint, etc.)
        error           – str | None, if something went wrong
    """
    if not ckpt_name:
        return {"ran": False, "reason": "no checkpoint available"}

    wf = copy.deepcopy(_SMOKE_WORKFLOW)
    wf["4"]["inputs"]["ckpt_name"] = ckpt_name

    # Lazy import — run_workflow pulls in a lot of optional deps and we
    # only need it when actually submitting.
    try:
        from run_workflow import ComfyRunner
    except ImportError as e:
        return {"ran": False, "reason": f"run_workflow not importable: {e}"}

    runner = ComfyRunner(host=host, api_key=api_key)

    # Submit
    try:
        sub = runner.submit(wf)
    except Exception as e:
        return {"ran": True, "submitted": False, "error": str(e)}

    if "_http_error" in sub:
        return {
            "ran": True, "submitted": False,
            "http_status": sub["_http_error"],
            "body": sub.get("body"),
        }

    pid = sub.get("prompt_id")
    if not pid:
        return {"ran": True, "submitted": False, "response": sub}

    # Cancel immediately — we only wanted to verify the server accepts jobs.
    cancelled = False
    try:
        cancelled = runner.cancel(pid)
    except Exception:
        pass  # best-effort; the job may have already finished or been GC'd

    return {
        "ran": True,
        "submitted": True,
        "prompt_id": pid,
        "cancelled_after_submit": cancelled,
        "note": "Submission accepted; cancelled to avoid running the full pipeline.",
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Submit a minimal workflow to verify ComfyUI accepts jobs",
    )
    p.add_argument("--host", default=DEFAULT_LOCAL_HOST)
    p.add_argument("--api-key", help=f"or set ${ENV_API_KEY}")
    p.add_argument("--ckpt", help="Checkpoint name (auto-detected if omitted)")
    args = p.parse_args(argv)

    api_key = resolve_api_key(args.api_key)
    ckpt = args.ckpt

    # Auto-detect checkpoint if not provided
    if not ckpt:
        try:
            from _common import http_get, parse_model_list
            url = resolve_url(args.host, "/models/checkpoints")
            r = http_get(url, headers={"X-API-Key": api_key} if api_key else {},
                         retries=2, timeout=15)
            if r.status == 200:
                models = parse_model_list(r.json())
                ckpt = sorted(models)[0] if models else None
        except Exception:
            pass

    result = run_smoke_test(args.host, api_key=api_key, ckpt_name=ckpt)
    emit_json(result)
    return 0 if result.get("submitted") else 1


if __name__ == "__main__":
    sys.exit(main())
