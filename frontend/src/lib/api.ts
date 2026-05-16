const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";

class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function fetchJson<T>(path: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${path}`;
  const response = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    ...options,
  });
  if (!response.ok) {
    const error = await response.text();
    throw new ApiError(`API error ${response.status}: ${error}`, response.status);
  }
  if (response.status === 204) return undefined as T;
  return response.json();
}

export async function getHealth() {
  return fetchJson<{ status: string }>("/health/");
}

export { ApiError };

export const api = fetchJson;

// ── Types ──

export interface Product {
  id: string;
  name: string;
  sku: string;
  description?: string | null;
  category?: string | null;
  status: "active" | "discontinued";
  created_at: string;
  updated_at: string;
}

export interface ProductCreate {
  name: string;
  sku: string;
  description?: string | null;
  category?: string | null;
  status?: "active" | "discontinued";
}

export interface Batch {
  id: string;
  product_id: string;
  batch_number: string;
  quantity_produced: number;
  production_date: string;
  status: "in_production" | "in_qa" | "passed" | "failed" | "shipped";
  notes?: string | null;
  created_at: string;
  updated_at: string;
  product?: Product | null;
}

export interface BatchCreate {
  product_id: string;
  batch_number: string;
  quantity_produced: number;
  production_date: string;
  status?: "in_production" | "in_qa" | "passed" | "failed" | "shipped";
  notes?: string | null;
}

export interface Inspection {
  id: string;
  batch_id: string;
  inspector_name: string;
  inspection_type: string;
  result: "pass" | "fail" | "pending";
  notes?: string | null;
  inspected_at: string;
  created_at: string;
  updated_at: string;
  batch?: Batch | null;
}

export interface InspectionCreate {
  batch_id: string;
  inspector_name: string;
  inspection_type?: string;
  result?: "pass" | "fail" | "pending";
  notes?: string | null;
  inspected_at: string;
}

export interface Defect {
  id: string;
  inspection_id: string;
  defect_type: string;
  severity: "low" | "medium" | "high" | "critical";
  description: string;
  quantity_affected: number;
  ai_suggested: boolean;
  ai_confidence?: number | null;
  recommended_action?: string | null;
  created_at: string;
  updated_at: string;
  inspection?: Inspection | null;
}

export interface DefectCreate {
  inspection_id: string;
  defect_type: string;
  severity: "low" | "medium" | "high" | "critical";
  description: string;
  quantity_affected?: number;
  ai_suggested?: boolean;
  ai_confidence?: number | null;
  recommended_action?: string | null;
}

export interface DashboardStats {
  total_inspections: number;
  inspections_this_month: number;
  pass_rate: number;
  total_defects: number;
  defects_by_severity: Record<string, number>;
  batches_by_status: Record<string, number>;
  top_defect_types: Array<{ type: string; count: number }>;
  recent_inspections: Inspection[];
}

export interface AIDefectSuggestion {
  id: string;
  inspection_id: string;
  defect_type: string;
  severity: string;
  description: string;
  quantity_affected: number;
  ai_suggested: boolean;
  ai_confidence: number;
  recommended_action: string;
}

// ── API Functions ──

// Products
export async function listProducts(search?: string) {
  const qs = search ? `?search=${encodeURIComponent(search)}` : "";
  return api<Product[]>(`/api/v1/products${qs}`);
}
export async function createProduct(data: ProductCreate) {
  return api<Product>("/api/v1/products", { method: "POST", body: JSON.stringify(data) });
}
export async function getProduct(id: string) {
  return api<Product>(`/api/v1/products/${id}`);
}
export async function updateProduct(id: string, data: Partial<ProductCreate>) {
  return api<Product>(`/api/v1/products/${id}`, { method: "PUT", body: JSON.stringify(data) });
}
export async function deleteProduct(id: string) {
  return api<void>(`/api/v1/products/${id}`, { method: "DELETE" });
}

// Batches
export async function listBatches(params?: { product_id?: string; status?: string }) {
  const sp = new URLSearchParams();
  if (params?.product_id) sp.set("product_id", params.product_id);
  if (params?.status) sp.set("status", params.status);
  const qs = sp.toString() ? `?${sp.toString()}` : "";
  return api<Batch[]>(`/api/v1/batches${qs}`);
}
export async function createBatch(data: BatchCreate) {
  return api<Batch>("/api/v1/batches", { method: "POST", body: JSON.stringify(data) });
}
export async function getBatch(id: string) {
  return api<Batch>(`/api/v1/batches/${id}`);
}
export async function updateBatch(id: string, data: Partial<BatchCreate>) {
  return api<Batch>(`/api/v1/batches/${id}`, { method: "PUT", body: JSON.stringify(data) });
}
export async function deleteBatch(id: string) {
  return api<void>(`/api/v1/batches/${id}`, { method: "DELETE" });
}

// Inspections
export async function listInspections(params?: { batch_id?: string; result?: string }) {
  const sp = new URLSearchParams();
  if (params?.batch_id) sp.set("batch_id", params.batch_id);
  if (params?.result) sp.set("result", params.result);
  const qs = sp.toString() ? `?${sp.toString()}` : "";
  return api<Inspection[]>(`/api/v1/inspections${qs}`);
}
export async function createInspection(data: InspectionCreate) {
  return api<Inspection>("/api/v1/inspections", { method: "POST", body: JSON.stringify(data) });
}
export async function getInspection(id: string) {
  return api<Inspection>(`/api/v1/inspections/${id}`);
}
export async function updateInspection(id: string, data: Partial<InspectionCreate>) {
  return api<Inspection>(`/api/v1/inspections/${id}`, { method: "PUT", body: JSON.stringify(data) });
}
export async function deleteInspection(id: string) {
  return api<void>(`/api/v1/inspections/${id}`, { method: "DELETE" });
}

// Defects
export async function listDefects(params?: { inspection_id?: string; severity?: string; defect_type?: string }) {
  const sp = new URLSearchParams();
  if (params?.inspection_id) sp.set("inspection_id", params.inspection_id);
  if (params?.severity) sp.set("severity", params.severity);
  if (params?.defect_type) sp.set("defect_type", params.defect_type);
  const qs = sp.toString() ? `?${sp.toString()}` : "";
  return api<Defect[]>(`/api/v1/defects${qs}`);
}
export async function createDefect(data: DefectCreate) {
  return api<Defect>("/api/v1/defects", { method: "POST", body: JSON.stringify(data) });
}
export async function getDefect(id: string) {
  return api<Defect>(`/api/v1/defects/${id}`);
}
export async function updateDefect(id: string, data: Partial<DefectCreate>) {
  return api<Defect>(`/api/v1/defects/${id}`, { method: "PUT", body: JSON.stringify(data) });
}
export async function deleteDefect(id: string) {
  return api<void>(`/api/v1/defects/${id}`, { method: "DELETE" });
}

// Dashboard
export async function getDashboard() {
  return api<DashboardStats>("/api/v1/dashboard");
}

// AI
export async function classifyDefect(description: string) {
  return api<AIDefectSuggestion>(`/api/v1/ai/classify-defect?description=${encodeURIComponent(description)}`);
}

export function apiErrorMessage(err: unknown): string {
  if (err instanceof ApiError) return err.message;
  if (err instanceof Error) return err.message;
  return String(err);
}
