#!/usr/bin/env python3
"""Profil cepat file CSV: ukuran, tipe, nilai kosong, duplikat, statistik, nilai teratas.
Pakai: python profil_csv.py data.csv [--md laporan.md]"""
import argparse
import pandas as pd

def profil(df: pd.DataFrame) -> str:
    L = ["# Profil Data", "",
         f"- Baris: **{len(df):,}**  |  Kolom: **{df.shape[1]}**",
         f"- Baris duplikat: **{int(df.duplicated().sum()):,}**", "",
         "## Kolom", "", "| Kolom | Tipe | Kosong | % Kosong | Unik |", "|---|---|---|---|---|"]
    for c in df.columns:
        n = int(df[c].isna().sum())
        L.append(f"| {c} | {df[c].dtype} | {n} | {n/len(df)*100:.1f}% | {df[c].nunique()} |")
    num = df.select_dtypes("number")
    if not num.empty:
        L += ["", "## Statistik numerik", "", num.describe().T.round(2).to_markdown()]
    for c in df.select_dtypes(exclude="number").columns[:5]:
        L += ["", f"## Nilai teratas: {c}", "", df[c].value_counts().head(5).to_markdown()]
    return "\n".join(L)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("csv")
    p.add_argument("--md", help="simpan laporan ke file markdown")
    a = p.parse_args()
    hasil = profil(pd.read_csv(a.csv))
    if a.md:
        open(a.md, "w", encoding="utf-8").write(hasil)
        print("Tersimpan:", a.md)
    else:
        print(hasil)
