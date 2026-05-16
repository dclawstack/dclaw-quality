"use client";

import React, { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import {
  Dialog, DialogContent, DialogHeader, DialogTitle,
} from "@/components/ui/dialog";
import { Plus, Trash2, Sparkles } from "lucide-react";
import {
  Defect, DefectCreate, listDefects, createDefect, deleteDefect,
  Inspection, listInspections, classifyDefect, AIDefectSuggestion,
} from "@/lib/api";

export default function DefectsPage() {
  const [defects, setDefects] = useState<Defect[]>([]);
  const [inspections, setInspections] = useState<Inspection[]>([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [aiOpen, setAiOpen] = useState(false);
  const [aiDesc, setAiDesc] = useState("");
  const [aiLoading, setAiLoading] = useState(false);
  const [aiResult, setAiResult] = useState<AIDefectSuggestion | null>(null);
  const [form, setForm] = useState<Partial<DefectCreate>>({ severity: "medium", quantity_affected: 1 });

  async function load() {
    setLoading(true);
    const [d, i] = await Promise.all([listDefects(), listInspections()]);
    setDefects(d);
    setInspections(i);
    setLoading(false);
  }

  useEffect(() => { load(); }, []);

  function inspectionInfo(id: string) {
    const insp = inspections.find((i) => i.id === id);
    return insp ? `${insp.inspector_name} / ${id.slice(0, 8)}` : id.slice(0, 8);
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    await createDefect(form as DefectCreate);
    setOpen(false);
    setForm({ severity: "medium", quantity_affected: 1 });
    load();
  }

  async function handleDelete(id: string) {
    if (!confirm("Delete?")) return;
    await deleteDefect(id);
    load();
  }

  async function handleAiSuggest() {
    if (!aiDesc.trim()) return;
    setAiLoading(true);
    try {
      const res = await classifyDefect(aiDesc);
      setAiResult(res);
      setForm({
        ...form,
        defect_type: res.defect_type,
        severity: res.severity as DefectCreate["severity"],
        description: res.description,
        ai_suggested: true,
        ai_confidence: res.ai_confidence,
        recommended_action: res.recommended_action,
      });
    } finally {
      setAiLoading(false);
    }
  }

  const severityColor: Record<string, string> = {
    low: "bg-slate-100 text-slate-700",
    medium: "bg-amber-50 text-amber-700",
    high: "bg-orange-50 text-orange-700",
    critical: "bg-red-50 text-red-700",
  };

  return (
    <div className="p-6 space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-slate-900">Defects</h1>
        <Button className="bg-red-600 hover:bg-red-700" onClick={() => setOpen(true)}>
          <Plus className="h-4 w-4 mr-1" /> Log Defect
        </Button>
      </div>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="max-w-lg">
          <DialogHeader><DialogTitle>Log Defect</DialogTitle></DialogHeader>

          <Button variant="outline" size="sm" className="w-fit" onClick={() => { setAiOpen(!aiOpen); setAiDesc(""); setAiResult(null); }}>
            <Sparkles className="h-4 w-4 mr-1" /> AI Suggest
          </Button>

          {aiOpen && (
            <div className="rounded-lg border bg-slate-50 p-3 space-y-2">
              <Label>Describe the defect</Label>
              <Input placeholder="e.g. deep scratch on surface..." value={aiDesc} onChange={(e) => setAiDesc(e.target.value)} />
              <Button size="sm" className="bg-red-600 hover:bg-red-700" onClick={handleAiSuggest} disabled={aiLoading}>
                {aiLoading ? "Analyzing..." : "Analyze"}
              </Button>
              {aiResult && (
                <div className="text-xs space-y-1">
                  <p><strong>Type:</strong> {aiResult.defect_type.replace(/_/g, " ")}</p>
                  <p><strong>Severity:</strong> {aiResult.severity}</p>
                  <p><strong>Confidence:</strong> {Math.round((aiResult.ai_confidence ?? 0) * 100)}%</p>
                  <p><strong>Action:</strong> {aiResult.recommended_action}</p>
                </div>
              )}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4 mt-2">
            <div>
              <Label>Inspection</Label>
              <select
                className="w-full rounded-md border border-slate-200 px-3 py-2 text-sm"
                value={form.inspection_id ?? ""}
                onChange={(e) => setForm({ ...form, inspection_id: e.target.value })}
                required
              >
                <option value="">Select...</option>
                {inspections.map((i) => (
                  <option key={i.id} value={i.id}>{inspectionInfo(i.id)}</option>
                ))}
              </select>
            </div>
            <div>
              <Label>Defect Type</Label>
              <select
                className="w-full rounded-md border border-slate-200 px-3 py-2 text-sm"
                value={form.defect_type ?? ""}
                onChange={(e) => setForm({ ...form, defect_type: e.target.value })}
                required
              >
                <option value="">Select...</option>
                <option value="surface_scratch">Surface Scratch</option>
                <option value="dimensional">Dimensional</option>
                <option value="contamination">Contamination</option>
                <option value="assembly">Assembly</option>
                <option value="cosmetic">Cosmetic</option>
                <option value="functional">Functional</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div>
              <Label>Severity</Label>
              <select
                className="w-full rounded-md border border-slate-200 px-3 py-2 text-sm"
                value={form.severity ?? "medium"}
                onChange={(e) => setForm({ ...form, severity: e.target.value as DefectCreate["severity"] })}
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="critical">Critical</option>
              </select>
            </div>
            <div>
              <Label>Description</Label>
              <Input value={form.description ?? ""} onChange={(e) => setForm({ ...form, description: e.target.value })} required />
            </div>
            <div>
              <Label>Qty Affected</Label>
              <Input type="number" value={form.quantity_affected ?? 1} onChange={(e) => setForm({ ...form, quantity_affected: Number(e.target.value) })} required />
            </div>
            <Button type="submit" className="bg-red-600 hover:bg-red-700 w-full">Log Defect</Button>
          </form>
        </DialogContent>
      </Dialog>

      {loading ? (
        <div className="text-sm text-slate-500">Loading...</div>
      ) : (
        <div className="rounded-lg border bg-white">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Type</TableHead>
                <TableHead>Severity</TableHead>
                <TableHead>Description</TableHead>
                <TableHead>Qty</TableHead>
                <TableHead>AI</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {defects.length === 0 && (
                <TableRow><TableCell colSpan={6} className="text-center text-sm text-slate-400">No defects</TableCell></TableRow>
              )}
              {defects.map((d) => (
                <TableRow key={d.id}>
                  <TableCell className="text-xs capitalize">{d.defect_type.replace(/_/g, " ")}</TableCell>
                  <TableCell>
                    <Badge className={`text-xs capitalize ${severityColor[d.severity] ?? ""}`}>{d.severity}</Badge>
                  </TableCell>
                  <TableCell className="max-w-xs truncate text-xs">{d.description}</TableCell>
                  <TableCell>{d.quantity_affected}</TableCell>
                  <TableCell>
                    {d.ai_suggested ? (
                      <Badge variant="outline" className="text-xs text-purple-600 border-purple-200">
                        <Sparkles className="h-3 w-3 mr-1" />
                        {Math.round((d.ai_confidence ?? 0) * 100)}%
                      </Badge>
                    ) : (
                      <span className="text-xs text-slate-400">—</span>
                    )}
                  </TableCell>
                  <TableCell className="text-right">
                    <Button size="sm" variant="ghost" className="text-red-600" onClick={() => handleDelete(d.id)}>
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )}
    </div>
  );
}
