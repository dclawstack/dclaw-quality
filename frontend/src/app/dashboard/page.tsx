"use client";

import React, { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  ClipboardCheck,
  TrendingUp,
  AlertTriangle,
  Boxes,
} from "lucide-react";
import { getDashboard, DashboardStats, apiErrorMessage } from "@/lib/api";

function SeverityBar({ label, count, total }: { label: string; count: number; total: number }) {
  const pct = total > 0 ? Math.round((count / total) * 100) : 0;
  return (
    <div className="mb-2">
      <div className="flex justify-between text-xs mb-1">
        <span className="font-medium capitalize">{label}</span>
        <span>{count}</span>
      </div>
      <div className="h-2 w-full rounded-full bg-slate-100">
        <div
          className="h-2 rounded-full bg-red-500"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  );
}

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        const data = await getDashboard();
        setStats(data);
      } catch (err) {
        setError(apiErrorMessage(err));
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-sm text-slate-500">Loading dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          {error}
        </div>
      </div>
    );
  }

  const totalDefects = stats?.total_defects ?? 0;
  const severityEntries = Object.entries(stats?.defects_by_severity ?? {});

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-slate-900">Dashboard</h1>
        <div className="flex gap-2">
          <Button variant="outline" size="sm">Export</Button>
        </div>
      </div>

      {/* Stats cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Total Inspections</CardTitle>
            <ClipboardCheck className="h-4 w-4 text-slate-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats?.total_inspections ?? 0}</div>
            <p className="text-xs text-slate-500">
              {stats?.inspections_this_month ?? 0} this month
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Pass Rate</CardTitle>
            <TrendingUp className="h-4 w-4 text-emerald-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-emerald-600">
              {stats?.pass_rate ?? 0}%
            </div>
            <p className="text-xs text-slate-500">Across all inspections</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Total Defects</CardTitle>
            <AlertTriangle className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">{totalDefects}</div>
            <p className="text-xs text-slate-500">Logged to date</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium">Batches</CardTitle>
            <Boxes className="h-4 w-4 text-slate-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {Object.values(stats?.batches_by_status ?? {}).reduce((a, b) => a + b, 0)}
            </div>
            <p className="text-xs text-slate-500">In system</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        {/* Defects by severity */}
        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Defects by Severity</CardTitle>
          </CardHeader>
          <CardContent>
            {severityEntries.length === 0 && (
              <p className="text-xs text-slate-400">No defects yet</p>
            )}
            {severityEntries.map(([label, count]) => (
              <SeverityBar key={label} label={label} count={count} total={totalDefects} />
            ))}
          </CardContent>
        </Card>

        {/* Top defect types */}
        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Top Defect Types</CardTitle>
          </CardHeader>
          <CardContent>
            {(stats?.top_defect_types ?? []).length === 0 && (
              <p className="text-xs text-slate-400">No defects yet</p>
            )}
            <div className="space-y-2">
              {(stats?.top_defect_types ?? []).map((dt, i) => (
                <div key={i} className="flex items-center justify-between rounded-lg bg-slate-50 px-3 py-2">
                  <span className="text-xs font-medium capitalize">{dt.type.replace(/_/g, " ")}</span>
                  <Badge variant="secondary" className="text-xs">{dt.count}</Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Recent inspections */}
        <Card>
          <CardHeader>
            <CardTitle className="text-sm">Recent Inspections</CardTitle>
          </CardHeader>
          <CardContent>
            {(stats?.recent_inspections ?? []).length === 0 && (
              <p className="text-xs text-slate-400">No recent inspections</p>
            )}
            <div className="space-y-2">
              {(stats?.recent_inspections ?? []).slice(0, 6).map((insp) => (
                <div key={insp.id} className="flex items-center justify-between rounded-lg bg-slate-50 px-3 py-2">
                  <div className="min-w-0">
                    <p className="text-xs font-medium truncate">{insp.inspector_name}</p>
                    <p className="text-xs text-slate-500 truncate">{insp.inspection_type}</p>
                  </div>
                  <Badge
                    variant={insp.result === "pass" ? "default" : insp.result === "fail" ? "destructive" : "outline"}
                    className="text-xs capitalize"
                  >
                    {insp.result}
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
