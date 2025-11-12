# tinker_client.py
# EverLightOS Aether ↔ Tinker glue

from __future__ import annotations
import os, time, json, math
from typing import Iterable, List, Dict, Any, Optional
import requests

class TinkerError(RuntimeError): ...

def _env(name: str, default: Optional[str]=None) -> str:
    v = os.getenv(name, default)
    if v is None or v == "":
        raise TinkerError(f"Missing required environment variable: {name}")
    return v

class TinkerClient:
    """
    Minimal HTTP client for Tinker Index API.
    Expects:
      TINKER_API_URL = https://api.tinker.ai (example)
      TINKER_API_KEY = <key>
    """
    def __init__(self, base_url: Optional[str]=None, api_key: Optional[str]=None, timeout: int=30):
        self.base_url = (base_url or _env("TINKER_API_URL")).rstrip("/")
        self.api_key  = api_key or _env("TINKER_API_KEY")
        self.timeout  = timeout
        self.session  = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "EverLightOS-Aether/1.0"
        })

    # ---------- low-level ----------
    def _post(self, path: str, payload: dict) -> dict:
        url = f"{self.base_url}{path}"
        r = self.session.post(url, data=json.dumps(payload), timeout=self.timeout)
        if r.status_code >= 400:
            raise TinkerError(f"POST {path} failed {r.status_code}: {r.text[:500]}")
        return r.json() if r.text else {}

    def _get(self, path: str, params: dict | None=None) -> dict:
        url = f"{self.base_url}{path}"
        r = self.session.get(url, params=params, timeout=self.timeout)
        if r.status_code >= 400:
            raise TinkerError(f"GET {path} failed {r.status_code}: {r.text[:500]}")
        return r.json() if r.text else {}

    # ---------- indices ----------
    def ensure_index(self, name: str, dims: int=3072, metric: str="cosine", namespace: str | None=None) -> dict:
        payload = {"name": name, "dims": dims, "metric": metric}
        if namespace: payload["namespace"] = namespace
        return self._post("/v1/index/ensure", payload)

    def delete_index(self, name: str, namespace: str | None=None) -> dict:
        payload = {"name": name}
        if namespace: payload["namespace"] = namespace
        return self._post("/v1/index/delete", payload)

    def upsert(self,
               index_name: str,
               docs: List[Dict[str, Any]],
               namespace: Optional[str]=None,
               batch_size: int=100,
               backoff: float=0.5,
               max_retries: int=5) -> dict:
        """
        docs: [{"id": "...", "content": "...", "tags": [...], "arc": "...", "path": "...", ...}]
        """
        total = len(docs)
        ack = {"index": index_name, "namespace": namespace, "upserted": 0, "batches": 0}
        if total == 0:
            return ack

        for i in range(0, total, batch_size):
            chunk = docs[i:i+batch_size]
            payload = {"index": index_name, "namespace": namespace, "documents": chunk}
            attempt, wait = 0, backoff
            while True:
                try:
                    _ = self._post("/v1/index/upsert", payload)
                    ack["upserted"] += len(chunk)
                    ack["batches"] += 1
                    break
                except TinkerError as e:
                    attempt += 1
                    if attempt > max_retries:
                        raise
                    time.sleep(wait)
                    wait = min(wait * 2, 8.0)
        return ack

    def query(self,
              index_name: str,
              text: str,
              k: int=10,
              namespace: Optional[str]=None,
              filters: Optional[dict]=None,
              rerank: Optional[str]=None) -> dict:
        payload = {"index": index_name, "query": text, "k": k}
        if namespace: payload["namespace"] = namespace
        if filters:   payload["filters"] = filters
        if rerank:    payload["rerank"]  = rerank
        return self._post("/v1/index/query", payload)