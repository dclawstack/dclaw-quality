import { render, screen } from "@testing-library/react";
import LandingPage from "@/app/(landing)/page";

jest.mock("next/navigation", () => ({
  useRouter: () => ({ push: jest.fn() }),
  usePathname: () => "/",
}));

describe("LandingPage", () => {
  beforeEach(() => {
    render(<LandingPage />);
  });

  it("renders the brand name in the navbar", () => {
    expect(screen.getAllByText("DClaw Quality").length).toBeGreaterThan(0);
  });

  it("renders the hero headline", () => {
    expect(screen.getByText(/Quality Control,/i)).toBeInTheDocument();
    expect(screen.getByText(/Accelerated/i)).toBeInTheDocument();
  });

  it("has nav links for Features, How It Works, Why Us", () => {
    expect(screen.getAllByRole("link", { name: /features/i }).length).toBeGreaterThan(0);
    expect(screen.getAllByRole("link", { name: /how it works/i }).length).toBeGreaterThan(0);
    expect(screen.getAllByRole("link", { name: /why us/i }).length).toBeGreaterThan(0);
  });

  it("has Launch App / Dashboard buttons linking to /dashboard", () => {
    const links = screen.getAllByRole("link", { name: /dashboard/i });
    expect(links.length).toBeGreaterThan(0);
    expect(links[0]).toHaveAttribute("href", "/dashboard");
  });

  it("renders features section heading", () => {
    expect(screen.getByText(/Everything you need to run quality/i)).toBeInTheDocument();
  });

  it("renders feature cards", () => {
    expect(screen.getByText("Full Traceability")).toBeInTheDocument();
    expect(screen.getByText("AI Defect Copilot")).toBeInTheDocument();
    expect(screen.getByText("Real-Time Dashboard")).toBeInTheDocument();
  });

  it("renders the comparison table", () => {
    expect(screen.getByText(/Escape the spreadsheet/i)).toBeInTheDocument();
    expect(screen.getByText(/Spreadsheets \/ SharePoint/i)).toBeInTheDocument();
    expect(screen.getByText(/MasterControl \/ EtQ/i)).toBeInTheDocument();
  });

  it("renders the CTA section", () => {
    expect(screen.getByText(/Ready to replace spreadsheets/i)).toBeInTheDocument();
  });

  it("renders the footer", () => {
    expect(screen.getByText(/DClaw Stack/i)).toBeInTheDocument();
  });
});
