import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import DefectsPage from "@/app/(app)/defects/page";
import * as api from "@/lib/api";

jest.mock("@/lib/api", () => ({
  ...jest.requireActual("@/lib/api"),
  listDefects: jest.fn(),
  listInspections: jest.fn(),
  createDefect: jest.fn(),
  deleteDefect: jest.fn(),
  classifyDefect: jest.fn(),
}));

const mockListDefects = api.listDefects as jest.Mock;
const mockListInspections = api.listInspections as jest.Mock;
const mockClassify = api.classifyDefect as jest.Mock;

const sampleDefects: api.Defect[] = [
  {
    id: "d1",
    inspection_id: "i1",
    defect_type: "surface_scratch",
    severity: "low",
    description: "Scratch on top surface",
    quantity_affected: 2,
    ai_suggested: true,
    ai_confidence: 0.85,
    created_at: "2024-01-01T00:00:00",
    updated_at: "2024-01-01T00:00:00",
  },
  {
    id: "d2",
    inspection_id: "i1",
    defect_type: "functional",
    severity: "critical",
    description: "Unit does not power on",
    quantity_affected: 1,
    ai_suggested: false,
    created_at: "2024-01-02T00:00:00",
    updated_at: "2024-01-02T00:00:00",
  },
];

describe("DefectsPage", () => {
  beforeEach(() => {
    mockListDefects.mockResolvedValue(sampleDefects);
    mockListInspections.mockResolvedValue([]);
  });

  it("shows loading then renders defects table", async () => {
    render(<DefectsPage />);
    expect(screen.getByText(/Loading/i)).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText(/surface scratch/i)).toBeInTheDocument());
  });

  it("renders defect descriptions", async () => {
    render(<DefectsPage />);
    await waitFor(() => expect(screen.getByText("Scratch on top surface")).toBeInTheDocument());
    expect(screen.getByText("Unit does not power on")).toBeInTheDocument();
  });

  it("renders severity badges", async () => {
    render(<DefectsPage />);
    await waitFor(() => expect(screen.getByText("low")).toBeInTheDocument());
    expect(screen.getByText("critical")).toBeInTheDocument();
  });

  it("shows AI confidence badge for ai_suggested defects", async () => {
    render(<DefectsPage />);
    await waitFor(() => expect(screen.getByText("85%")).toBeInTheDocument());
  });

  it("shows — for non-AI defects", async () => {
    render(<DefectsPage />);
    await waitFor(() => expect(screen.getByText("—")).toBeInTheDocument());
  });

  it("shows empty state when no defects", async () => {
    mockListDefects.mockResolvedValue([]);
    render(<DefectsPage />);
    await waitFor(() => expect(screen.getByText(/No defects/i)).toBeInTheDocument());
  });

  it("opens Log Defect dialog on button click", async () => {
    render(<DefectsPage />);
    await waitFor(() => screen.getByText(/surface scratch/i));
    fireEvent.click(screen.getByRole("button", { name: /Log Defect/i }));
    expect(screen.getByText("Log Defect", { selector: "[class*='DialogTitle'], h2, h3" })).toBeInTheDocument();
  });

  it("shows AI Suggest button inside the dialog", async () => {
    render(<DefectsPage />);
    await waitFor(() => screen.getByText(/surface scratch/i));
    fireEvent.click(screen.getByRole("button", { name: /Log Defect/i }));
    expect(screen.getByRole("button", { name: /AI Suggest/i })).toBeInTheDocument();
  });

  it("calls classifyDefect and displays result after analyze", async () => {
    mockClassify.mockResolvedValue({
      id: "ai1",
      inspection_id: "",
      defect_type: "dimensional",
      severity: "high",
      description: "test",
      quantity_affected: 1,
      ai_suggested: true,
      ai_confidence: 0.92,
      recommended_action: "Rework the part",
    });

    render(<DefectsPage />);
    await waitFor(() => screen.getByText(/surface scratch/i));

    fireEvent.click(screen.getByRole("button", { name: /Log Defect/i }));
    fireEvent.click(screen.getByRole("button", { name: /AI Suggest/i }));

    const descInput = screen.getByPlaceholderText(/deep scratch/i);
    fireEvent.change(descInput, { target: { value: "part is off dimension" } });

    fireEvent.click(screen.getByRole("button", { name: /Analyze/i }));

    await waitFor(() => expect(mockClassify).toHaveBeenCalledWith("part is off dimension"));
    await waitFor(() => expect(screen.getByText(/Rework the part/i)).toBeInTheDocument());
  });
});
