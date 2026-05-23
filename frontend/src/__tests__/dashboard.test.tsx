import { render, screen, waitFor } from "@testing-library/react";
import DashboardPage from "@/app/(app)/dashboard/page";
import * as api from "@/lib/api";

jest.mock("@/lib/api", () => ({
  ...jest.requireActual("@/lib/api"),
  getDashboard: jest.fn(),
  apiErrorMessage: jest.fn((e: unknown) => String(e)),
}));

const mockGetDashboard = api.getDashboard as jest.Mock;

const sampleStats: api.DashboardStats = {
  total_inspections: 42,
  inspections_this_month: 7,
  pass_rate: 88,
  total_defects: 5,
  defects_by_severity: { low: 2, high: 3 },
  batches_by_status: { in_qa: 4, passed: 6 },
  top_defect_types: [{ type: "surface_scratch", count: 3 }],
  recent_inspections: [
    {
      id: "i1",
      batch_id: "b1",
      inspector_name: "Alice",
      inspection_type: "visual",
      result: "pass",
      inspected_at: "2024-01-01T00:00:00",
      created_at: "2024-01-01T00:00:00",
      updated_at: "2024-01-01T00:00:00",
    },
  ],
};

describe("DashboardPage", () => {
  it("shows loading state initially", () => {
    mockGetDashboard.mockReturnValue(new Promise(() => {}));
    render(<DashboardPage />);
    expect(screen.getByText(/Loading dashboard/i)).toBeInTheDocument();
  });

  it("renders stats after load", async () => {
    mockGetDashboard.mockResolvedValue(sampleStats);
    render(<DashboardPage />);
    await waitFor(() => expect(screen.getByText("42")).toBeInTheDocument());
    expect(screen.getByText("88%")).toBeInTheDocument();
    expect(screen.getByText("5")).toBeInTheDocument();
  });

  it("shows total batches count (sum of batches_by_status)", async () => {
    mockGetDashboard.mockResolvedValue(sampleStats);
    render(<DashboardPage />);
    await waitFor(() => expect(screen.getByText("10")).toBeInTheDocument());
  });

  it("renders recent inspection inspector name", async () => {
    mockGetDashboard.mockResolvedValue(sampleStats);
    render(<DashboardPage />);
    await waitFor(() => expect(screen.getByText("Alice")).toBeInTheDocument());
  });

  it("renders defect type label in top defect types", async () => {
    mockGetDashboard.mockResolvedValue(sampleStats);
    render(<DashboardPage />);
    await waitFor(() => expect(screen.getByText(/surface scratch/i)).toBeInTheDocument());
  });

  it("shows error message when API fails", async () => {
    mockGetDashboard.mockRejectedValue(new Error("Network error"));
    (api.apiErrorMessage as jest.Mock).mockReturnValue("Network error");
    render(<DashboardPage />);
    await waitFor(() => expect(screen.getByText("Network error")).toBeInTheDocument());
  });

  it("shows empty state message when no defects", async () => {
    mockGetDashboard.mockResolvedValue({ ...sampleStats, defects_by_severity: {}, total_defects: 0 });
    render(<DashboardPage />);
    await waitFor(() => expect(screen.getByText(/No defects yet/i)).toBeInTheDocument());
  });
});
