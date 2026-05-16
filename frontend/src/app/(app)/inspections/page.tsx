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
import { Plus, Trash2 } from "lucide-react";
import { Inspection, InspectionCreate, listInspections, createInspection, deleteInspection, Batch, listBatches } from "@/lib/api";

export default function InspectionsPage() {
  const [inspections, setInspections] = useState<Inspection[]>([]);
  const [batches, setBatches] = useState<Batch[]>([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<Partial<InspectionCreate>>({ result: "pending" });

  async function load() {
    setLoading(true);
    const [i, b] = await Promise.all([listInspections(), listBatches()]);
    setInspections(i);
    setBatches(b);
    setLoading(false);
  }

  useEffect(() => { load(); }, []);

  function batchNumber(id: string) {
    return batches.find((b) => b.id === id)?.batch_number ?? id.slice(0, 8);
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    await createInspection(form as InspectionCreate);
    setOpen(false);
    setForm({ result: "pending" });
    load();
  }

  async function handleDelete(id: string) {
    if (!confirm("Delete?")) return;
    await deleteInspection(id);
    load();
  }

  return (
    <div className="p-6 space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-slate-900">Inspections</h1>
        <Button className="bg-red-600 hover:bg-red-700" onClick={() => setOpen(true)}>
          <Plus className="h-4 w-4 mr-1" /> Add Inspection
        </Button>
      </div>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent>
          <DialogHeader><DialogTitle>Add Inspection</DialogTitle></DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4 mt-2">
            <div>
              <Label>Batch</Label>
              <select
                className="w-full rounded-md border border-slate-200 px-3 py-2 text-sm"
                value={form.batch_id ?? ""}
                onChange={(e) => setForm({ ...form, batch_id: e.target.value })}
                required
              >
                <option value="">Select...</option>
                {batches.map((b) => (
                  <option key={b.id} value={b.id}>{b.batch_number}</option>
                ))}
              </select>
            </div>
            <div>
              <Label>Inspector Name</Label>
              <Input value={form.inspector_name ?? ""} onChange={(e) => setForm({ ...form, inspector_name: e.target.value })} required />
            </div>
            <div>
              <Label>Type</Label>
              <Input value={form.inspection_type ?? "visual"} onChange={(e) => setForm({ ...form, inspection_type: e.target.value })} />
            </div>
            <div>
              <Label>Result</Label>
              <select
                className="w-full rounded-md border border-slate-200 px-3 py-2 text-sm"
                value={form.result ?? "pending"}
                onChange={(e) => setForm({ ...form, result: e.target.value as InspectionCreate["result"] })}
              >
                <option value="pass">Pass</option>
                <option value="fail">Fail</option>
                <option value="pending">Pending</option>
              </select>
            </div>
            <div>
              <Label>Inspected At</Label>
              <Input type="datetime-local" onChange={(e) => setForm({ ...form, inspected_at: new Date(e.target.value).toISOString() })} required />
            </div>
            <div>
              <Label>Notes</Label>
              <Input value={form.notes ?? ""} onChange={(e) => setForm({ ...form, notes: e.target.value })} />
            </div>
            <Button type="submit" className="bg-red-600 hover:bg-red-700 w-full">Create</Button>
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
                <TableHead>Inspector</TableHead>
                <TableHead>Batch</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Result</TableHead>
                <TableHead>Inspected</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {inspections.length === 0 && (
                <TableRow><TableCell colSpan={6} className="text-center text-sm text-slate-400">No inspections</TableCell></TableRow>
              )}
              {inspections.map((i) => (
                <TableRow key={i.id}>
                  <TableCell className="font-medium">{i.inspector_name}</TableCell>
                  <TableCell className="font-mono text-xs">{batchNumber(i.batch_id)}</TableCell>
                  <TableCell className="text-xs capitalize">{i.inspection_type}</TableCell>
                  <TableCell>
                    <Badge variant={i.result === "pass" ? "default" : i.result === "fail" ? "destructive" : "secondary"} className="text-xs capitalize">
                      {i.result}
                    </Badge>
                  </TableCell>
                  <TableCell className="text-xs">{new Date(i.inspected_at).toLocaleDateString()}</TableCell>
                  <TableCell className="text-right">
                    <Button size="sm" variant="ghost" className="text-red-600" onClick={() => handleDelete(i.id)}>
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
