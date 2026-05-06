"use client";

import React, { useState } from "react";
import { Award, Search } from "lucide-react";
import { api, QualityReport, TrendScore } from "@/lib/api";

export default function DashboardPage() {
  const [batchId, setBatchId] = useState("");
  const [productSpec, setProductSpec] = useState("");
  const [report, setReport] = useState<QualityReport | null>(null);
  const [trends, setTrends] = useState<TrendScore[] | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleInspect(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setTrends(null);
    try {
      const result = await api<QualityReport>("/reports", {
        method: "POST",
        body: JSON.stringify({ batch_id: batchId, product_spec: productSpec }),
      });
      setReport(result);
      const trendData = await api<TrendScore[]>(`/reports/${result.id}/trends`);
      setTrends(trendData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b bg-white px-6 py-4 flex items-center gap-3">
        <Award className="h-6 w-6" style={{ color: "#DC2626" }} />
        <h1 className="text-xl font-bold" style={{ color: "#DC2626" }}>
          DClaw Quality
        </h1>
      </header>

      <section className="mx-auto max-w-2xl px-6 py-10">
        <h2 className="mb-6 text-2xl font-semibold text-slate-800">Dashboard</h2>

        <form onSubmit={handleInspect} className="mb-8 rounded-xl border bg-white p-6 shadow-sm">
          <div className="mb-4">
            <label htmlFor="batch" className="mb-1 block text-sm font-medium text-slate-700">
              Batch ID
            </label>
            <input
              id="batch"
              type="text"
              value={batchId}
              onChange={(e) => setBatchId(e.target.value)}
              placeholder="BATCH-001"
              className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:border-[#DC2626] focus:ring-1 focus:ring-[#DC2626]"
              required
            />
          </div>

          <div className="mb-6">
            <label htmlFor="spec" className="mb-1 block text-sm font-medium text-slate-700">
              Product spec
            </label>
            <input
              id="spec"
              type="text"
              value={productSpec}
              onChange={(e) => setProductSpec(e.target.value)}
              placeholder="Model-A v2"
              className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:border-[#DC2626] focus:ring-1 focus:ring-[#DC2626]"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="inline-flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-semibold text-white transition-opacity hover:opacity-90 disabled:opacity-60"
            style={{ backgroundColor: "#DC2626" }}
          >
            <Search className="h-4 w-4" />
            {loading ? "Inspecting..." : "Inspect Batch"}
          </button>
        </form>

        {report && (
          <div className="rounded-xl border bg-white p-6 shadow-sm">
            <h3 className="mb-4 text-lg font-semibold text-slate-800">Quality Report</h3>
            <dl className="grid grid-cols-1 gap-3 sm:grid-cols-2">
              <div className="rounded-lg bg-slate-50 p-3">
                <dt className="text-xs font-medium uppercase tracking-wide text-slate-500">Pass rate</dt>
                <dd className="mt-1 text-sm font-semibold text-slate-900">{report.pass_rate}%</dd>
              </div>
              <div className="rounded-lg bg-slate-50 p-3">
                <dt className="text-xs font-medium uppercase tracking-wide text-slate-500">Defect count</dt>
                <dd className="mt-1 text-sm font-semibold text-slate-900">{report.defect_count}</dd>
              </div>
              <div className="rounded-lg bg-slate-50 p-3">
                <dt className="text-xs font-medium uppercase tracking-wide text-slate-500">Defect types</dt>
                <dd className="mt-1 text-sm text-slate-900">{report.defect_types.join(", ")}</dd>
              </div>
              <div className="rounded-lg bg-slate-50 p-3">
                <dt className="text-xs font-medium uppercase tracking-wide text-slate-500">Recommended action</dt>
                <dd className="mt-1 text-sm text-slate-900">{report.recommended_action}</dd>
              </div>
              <div className="rounded-lg bg-slate-50 p-3">
                <dt className="text-xs font-medium uppercase tracking-wide text-slate-500">Report ID</dt>
                <dd className="mt-1 text-sm font-mono text-slate-900">{report.id}</dd>
              </div>
              <div className="rounded-lg bg-slate-50 p-3">
                <dt className="text-xs font-medium uppercase tracking-wide text-slate-500">Created at</dt>
                <dd className="mt-1 text-sm text-slate-900">{report.created_at}</dd>
              </div>
            </dl>

            {trends && trends.length > 0 && (
              <div className="mt-6">
                <h4 className="mb-3 text-sm font-semibold text-slate-700">Recent Batch Trend Scores</h4>
                <div className="grid grid-cols-5 gap-2">
                  {trends.map((t, i) => (
                    <div key={i} className="rounded-lg bg-slate-50 p-3 text-center">
                      <div className="text-xs text-slate-500">{t.batch_id}</div>
                      <div className="mt-1 text-sm font-bold" style={{ color: "#DC2626" }}>{t.score}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </section>
    </main>
  );
}
