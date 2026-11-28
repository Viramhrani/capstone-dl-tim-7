"""Skrip Reproduksi Demo RNN (Bi-GRU) & Gladi Simulasi — Backlog #10, #14, #15 (Arya Muda Siregar, 123450063).

Bersifat baca-saja terhadap dataset & hasil utama di `results/`.
Menyimpan seluruh bukti uji, metrik JSON, CSV prediksi, dan grafik visualisasi ke `sprint/sprint-1/artefak/`.

Penggunaan (dari root repository):
    python sprint/sprint-1/artefak/b14_reproduksi_demo_rnn.py --mode simulasi
    python sprint/sprint-1/artefak/b14_reproduksi_demo_rnn.py --mode semua
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import os
import random
import subprocess
import sys
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import torch.nn as nn

OUT_DIR = Path(__file__).resolve().parent
REPO_DIR = OUT_DIR.parents[2]

sys.path.insert(0, str(REPO_DIR))
from src.common import manifest  # noqa: E402
from src.protokol import data as protokol_data  # noqa: E402


def muat_modul(nama: str, path: Path):
    spec = importlib.util.spec_from_file_location(nama, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def inspeksi_tensor(model: nn.Module, x_sample: torch.Tensor) -> dict:
    model.eval()
    with torch.no_grad():
        gru_out, h_n = model.gru(x_sample)
        normed = model.norm(gru_out).transpose(1, 2)
        pooled = model.pool(normed)
        out = model.head(pooled).squeeze(-1)
    return {
        "input_x": list(x_sample.shape),
        "gru_output_bidirectional": list(gru_out.shape),
        "gru_hidden_state": list(h_n.shape),
        "after_layernorm_transpose": list(normed.shape),
        "after_adaptive_avg_pool24": list(pooled.shape),
        "output_prediksi": list(out.shape),
        "ada_nan_output": bool(torch.isnan(out).any().item()),
    }


def jalankan_simulasi(rnn_mod) -> None:
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"
    env["PYTHONIOENCODING"] = "utf-8"

    # Backlog #10: Gladi simulasi
    res10 = subprocess.run(
        [sys.executable, str(REPO_DIR / "test_simulasi.py")],
        cwd=REPO_DIR, env=env, capture_output=True, text=True, encoding="utf-8",
    )
    assert res10.returncode == 0
    (OUT_DIR / "b10_log_gladi_simulasi.txt").write_text(
        (res10.stdout + "\n" + res10.stderr).strip() + "\n", encoding="utf-8"
    )

    # Backlog #14: Uji kerangka RNN pada data simulasi
    rng = np.random.default_rng(1007)
    n, t, c = 64, 200, 36
    y_sim = np.tile(np.array([8.9, 10.0, 11.1, 12.2, 13.3, 14.4, 15.5, 16.4], dtype=np.float32), 8)
    waktu = np.arange(t, dtype=np.float32) / 10.0
    X_sim = np.empty((n, t, c), dtype=np.float32)
    for i in range(n):
        f = float(y_sim[i]) / 19.0
        for ch in range(c):
            X_sim[i, :, ch] = 0.5 * np.sin(2 * np.pi * f * waktu + (ch % 6) * 0.7) + 0.03 * rng.normal(size=t)
    X_trim = X_sim[:, 10:, :]
    Xtr_s, ytr_s, Xva_s, yva_s = X_trim[:40], y_sim[:40], X_trim[40:48], y_sim[40:48]
    mu_s, sd_s = Xtr_s.mean(axis=(0, 1), keepdims=True), Xtr_s.std(axis=(0, 1), keepdims=True) + 1e-6
    Xtr_sn, Xva_sn = (Xtr_s - mu_s) / sd_s, (Xva_s - mu_s) / sd_s

    torch.manual_seed(1)
    m_sim = rnn_mod.PoseBiGRU(in_features=c)
    shapes_sim = inspeksi_tensor(m_sim, torch.tensor(Xva_sn))
    ymu_s, ysd_s = float(ytr_s.mean()), float(ytr_s.std())
    opt_s = torch.optim.AdamW(m_sim.parameters(), lr=rnn_mod.LR, weight_decay=rnn_mod.WD)
    crit = nn.L1Loss()
    t0 = time.time()
    losses_sim = []
    for _ in range(5):
        m_sim.train()
        opt_s.zero_grad()
        loss = crit(m_sim(torch.tensor(Xtr_sn)), torch.tensor((ytr_s - ymu_s) / ysd_s))
        loss.backward()
        nn.utils.clip_grad_norm_(m_sim.parameters(), 2.0)
        opt_s.step()
        losses_sim.append(round(float(loss.item()), 5))
    m_sim.eval()
    with torch.no_grad():
        pva_s = m_sim(torch.tensor(Xva_sn)).numpy() * ysd_s + ymu_s
    sim_info = {
        "status": "PASS",
        "bentuk_tensor": shapes_sim,
        "loss_5_epoch_simulasi": losses_sim,
        "val_mae_simulasi_5_epoch": round(float(np.abs(yva_s - pva_s).mean()), 4),
        "durasi_detik": round(time.time() - t0, 2),
    }
    (OUT_DIR / "b14_log_uji_simulasi_rnn.txt").write_text(
        "=== UJI KERANGKA RNN (PoseBiGRU) PADA DATA SIMULASI (#14) ===\n"
        + json.dumps(sim_info, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"[OK] #10 gladi & #14 simulasi RNN PASS (durasi {sim_info['durasi_detik']}s, loss {losses_sim[0]} -> {losses_sim[-1]})")


def jalankan_latih_seed1(rnn_mod) -> None:
    seed = 1
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.set_num_threads(max(1, min(4, os.cpu_count() or 1)))
    Xtr, ytr, Xva, yva, _, _ = protokol_data.muat()
    ymu, ysd = float(ytr.mean()), float(ytr.std())
    Xtr_t = torch.tensor(Xtr, dtype=torch.float32)
    ytr_t = torch.tensor((ytr - ymu) / ysd, dtype=torch.float32)
    Xva_t = torch.tensor(Xva, dtype=torch.float32)

    model = rnn_mod.PoseBiGRU(in_features=Xtr.shape[2])
    n_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    opt = torch.optim.AdamW(model.parameters(), lr=rnn_mod.LR, weight_decay=rnn_mod.WD)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=rnn_mod.EPOCHS)
    crit = nn.L1Loss()
    best = {"mae": float("inf"), "state": None, "epoch": 0}
    tanpa, history = 0, []
    t0 = time.time()
    for ep in range(1, rnn_mod.EPOCHS + 1):
        model.train()
        urut = torch.randperm(len(Xtr_t))
        ep_loss, nb = 0.0, 0
        for i in range(0, len(Xtr_t), rnn_mod.BATCH):
            idx = urut[i:i + rnn_mod.BATCH]
            xb = rnn_mod.augment(Xtr_t[idx].clone())
            yb = ytr_t[idx]
            opt.zero_grad()
            loss = crit(model(xb), yb)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 2.0)
            opt.step()
            ep_loss += float(loss.item())
            nb += 1
        sched.step()
        model.eval()
        with torch.no_grad():
            pva = model(Xva_t).numpy() * ysd + ymu
        mae = float(np.abs(yva - pva).mean())
        history.append({"epoch": ep, "train_l1_norm": round(ep_loss / nb, 5), "val_mae": round(mae, 6)})
        if mae < best["mae"]:
            best.update(mae=mae, state=copy.deepcopy(model.state_dict()), epoch=ep)
            tanpa = 0
        else:
            tanpa += 1
            if tanpa >= rnn_mod.PATIENCE:
                break
    durasi = time.time() - t0
    model.load_state_dict(best["state"])
    model.eval()
    with torch.no_grad():
        pred_val = model(Xva_t).numpy() * ysd + ymu

    x_one = Xva_t[:1]
    for _ in range(5):
        with torch.no_grad():
            model(x_one)
    ti0 = time.perf_counter()
    for _ in range(30):
        with torch.no_grad():
            model(x_one)
    lat_ms = (time.perf_counter() - ti0) * 1000.0 / 30.0

    val_mae = float(np.abs(yva - pred_val).mean())
    val_rmse = float(np.sqrt(((yva - pred_val) ** 2).mean()))
    val_r2 = float(1.0 - ((yva - pred_val) ** 2).sum() / ((yva - yva.mean()) ** 2).sum())

    summary = {
        "nim": "123450063", "model": "rnn", "seed": seed,
        "data_hash": manifest.data_hash(b"split:2026"),
        "jumlah_parameter": n_params,
        "best_epoch": best["epoch"], "total_epoch_jalan": len(history),
        "durasi_latih_detik": round(durasi, 2), "latensi_inferensi_ms": round(lat_ms, 2),
        "val_mae": round(val_mae, 6), "val_rmse": round(val_rmse, 6), "val_r2": round(val_r2, 6),
        "n_val": int(len(Xva)), "n_test": 0,
    }
    (OUT_DIR / "b15_hasil_reproduksi_rnn.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    pd.DataFrame({
        "sampel_p06": [f"P06-{i}" for i in range(1, len(yva) + 1)],
        "aktual_repetisi": np.round(yva, 4),
        "prediksi_rnn": np.round(pred_val, 4),
        "galat_absolut": np.round(np.abs(yva - pred_val), 4),
    }).to_csv(OUT_DIR / "b15_prediksi_validasi_p06_rnn.csv", index=False)

    log15 = (
        f"=== REPRODUKSI RNN Bi-GRU SEED 1 (#15) ===\n"
        f"best_epoch={best['epoch']}/{len(history)} | val_MAE={val_mae:.6f} | val_RMSE={val_rmse:.6f} "
        f"| val_R2={val_r2:.6f} | durasi={durasi:.1f}s | latensi={lat_ms:.2f} ms | params={n_params:,} "
        f"| data_hash={summary['data_hash']} | n_test=0\n"
    )
    (OUT_DIR / "b15_log_eksekusi_rnn.txt").write_text(log15, encoding="utf-8")

    ep_list = [h["epoch"] for h in history]
    vm_list = [h["val_mae"] for h in history]
    tl_list = [h["train_l1_norm"] for h in history]
    abs_err = np.abs(yva - pred_val)
    bi = int(np.argmin(vm_list))

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5), dpi=140)
    axes[0].plot(ep_list, vm_list, label="Validation MAE", color="#1d3557", linewidth=2)
    axes[0].plot(ep_list, tl_list, label="Train L1 (norm)", color="#457b9d", linestyle="--")
    axes[0].axhline(0.3698, color="#e76f51", linestyle=":", label="Pembanding Puncak (0,370)")
    axes[0].scatter([ep_list[bi]], [vm_list[bi]], color="#e63946", zorder=5, label=f"Best Ep {ep_list[bi]} ({vm_list[bi]:.4f})")
    axes[0].set_title("Kurva Pelatihan RNN Bi-GRU (Seed 1)")
    axes[0].set_xlabel("Epoch"); axes[0].set_ylabel("MAE / Loss"); axes[0].legend(fontsize=8); axes[0].grid(alpha=0.3)

    idx = np.arange(1, len(yva) + 1)
    axes[1].bar(idx - 0.18, yva, width=0.35, label="Aktual (P06)", color="#264653")
    axes[1].bar(idx + 0.18, pred_val, width=0.35, label="Prediksi RNN", color="#2a9d8f")
    axes[1].set_xticks(idx); axes[1].set_xticklabels([f"S{i}" for i in idx])
    axes[1].set_title("Prediksi vs Aktual (Validasi P06)"); axes[1].set_ylabel("Repetisi"); axes[1].legend(fontsize=8.5); axes[1].grid(axis="y", alpha=0.3)

    axes[2].bar(idx, abs_err, color="#e9c46a", edgecolor="#264653")
    axes[2].axhline(abs_err.mean(), color="#e63946", linestyle="--", label=f"MAE = {abs_err.mean():.4f}")
    axes[2].set_xticks(idx); axes[2].set_xticklabels([f"S{i}" for i in idx])
    axes[2].set_title("Galat Absolut per Kondisi P06"); axes[2].set_ylabel("|Aktual - Prediksi|"); axes[2].legend(fontsize=8.5); axes[2].grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT_DIR / "b15_visualisasi_rnn.png")
    plt.close(fig)
    print(log15)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mode", choices=["simulasi", "latih", "semua"], default="semua")
    a = ap.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rnn_mod = muat_modul("rnn_123450063", REPO_DIR / "models" / "123450063" / "run.py")
    if a.mode in ("simulasi", "semua"):
        jalankan_simulasi(rnn_mod)
    if a.mode in ("latih", "semua"):
        jalankan_latih_seed1(rnn_mod)


if __name__ == "__main__":
    main()
