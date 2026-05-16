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
import { Batch, BatchCreate, listBatches, createBatch, deleteBatch, Product, listProducts } from "@/lib/api";

export default function BatchesPage() {
  const [batches, setBatches] = useState<Batch[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState<Partial<BatchCreate>>({ quantity_produced: 0, status: "in_production" });

  async function load() {
    setLoading(true);
    const [b, p] = await Promise.all([listBatches(), listProducts()]);
    setBatches(b);
    setProducts(p);
    setLoading(false);
  }

  useEffect(() => { load(); }, []);

  function productName(id: string) {
    return products.find((p) => p.id === id)?.name ?? id.slice(0, 8);
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    await createBatch(form as BatchCreate);
    setOpen(false);
    setForm({ quantity_produced: 0, status: "in_production" });
    load();
  }

  async function handleDelete(id: string) {
    if (!confirm("Delete?")) return;
    await deleteBatch(id);
    load();
  }

  const statusColors: Record<string, string> = {
    in_production: "bg-blue-50 text-blue-700",
    in_qa: "bg-amber-50 text-amber-700",
    passed: "bg-emerald-50 text-emerald-700",
    failed: "bg-red-50 text-red-700",
    shipped: "bg-slate-50 text-slate-700",
  };

  return (
    <div className="p-6 space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-slate-900">Batches</h1>
        <Button className="bg-red-600 hover:bg-red-700" onClick={() => setOpen(true)}>
          <Plus className="h-4 w-4 mr-1" /> Add Batch
        </Button>
      </div>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent>
          <DialogHeader><DialogTitle>Add Batch</DialogTitle></DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4 mt-2">
            <div>
              <Label>Product</Label>
              <select
                className="w-full rounded-md border border-slate-200 px-3 py-2 text-sm"
                value={form.product_id ?? ""}
                onChange={(e) => setForm({ ...form, product_id: e.target.value })}
                required
              >
                <option value="">Select...</option>
                {products.map((p) => (
                  <option key={p.id} value={p.id}>{p.name}</option>
                ))}
              </select>
            </div>
            <div>
              <Label>Batch Number</Label>
              <Input value={form.batch_number ?? ""} onChange={(e) => setForm({ ...form, batch_number: e.target.value })} required />
            </div>
            <div>
              <Label>Quantity Produced</Label>
              <Input type="number" value={form.quantity_produced ?? 0} onChange={(e) => setForm({ ...form, quantity_produced: Number(e.target.value) })} required />
            </div>
            <div>
              <Label>Production Date</Label>
              <Input type="datetime-local" onChange={(e) => setForm({ ...form, production_date: new Date(e.target.value).toISOString() })} required />
            </div>
            <div>
              <Label>Status</Label>
              <select
                className="w-full rounded-md border border-slate-200 px-3 py-2 text-sm"
                value={form.status ?? "in_production"}
                onChange={(e) => setForm({ ...form, status: e.target.value as BatchCreate["status"] })}
              >
                <option value="in_production">In Production</option>
                <option value="in_qa">In QA</option>
                <option value="passed">Passed</option>
                <option value="failed">Failed</option>
                <option value="shipped">Shipped</option>
              </select>
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
                <TableHead>Batch #</TableHead>
                <TableHead>Product</TableHead>
                <TableHead>Qty</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Production Date</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {batches.length === 0 && (
                <TableRow><TableCell colSpan={6} className="text-center text-sm text-slate-400">No batches</TableCell></TableRow>
              )}
              {batches.map((b) => (
                <TableRow key={b.id}>
                  <TableCell className="font-mono text-xs">{b.batch_number}</TableCell>
                  <TableCell className="font-medium">{productName(b.product_id)}</TableCell>
                  <TableCell>{b.quantity_produced}</TableCell>
                  <TableCell>
                    <Badge className={`text-xs capitalize ${statusColors[b.status] ?? ""}`}>{b.status.replace(/_/g, " ")}</Badge>
                  </TableCell>
                  <TableCell className="text-xs">{new Date(b.production_date).toLocaleDateString()}</TableCell>
                  <TableCell className="text-right">
                    <Button size="sm" variant="ghost" className="text-red-600" onClick={() => handleDelete(b.id)}>
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
