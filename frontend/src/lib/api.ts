export interface QualityReport {
  id: string;
  batch_id: string;
  product_spec: string;
  pass_rate: number;
  defect_count: number;
  defect_types: string[];
  recommended_action: string;
  created_at: string;
}

export interface TrendScore {
  batch_id: string;
  score: number;
}

export async function api<T>(
  path: string,
  init: RequestInit = {}
): Promise<T> {
  const url = `/api/v1${path}`;
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(init.headers as Record<string, string>),
  };

  const res = await fetch(url, {
    ...init,
    headers,
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "Unknown error");
    throw new Error(`API error ${res.status}: ${text}`);
  }

  return res.json() as Promise<T>;
}
