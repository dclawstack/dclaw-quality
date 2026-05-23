import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import ProductsPage from "@/app/(app)/products/page";
import * as api from "@/lib/api";

jest.mock("@/lib/api", () => ({
  ...jest.requireActual("@/lib/api"),
  listProducts: jest.fn(),
  createProduct: jest.fn(),
  updateProduct: jest.fn(),
  deleteProduct: jest.fn(),
}));

const mockList = api.listProducts as jest.Mock;
const mockCreate = api.createProduct as jest.Mock;
const mockDelete = api.deleteProduct as jest.Mock;

const sampleProducts: api.Product[] = [
  {
    id: "p1",
    name: "Widget A",
    sku: "W-001",
    category: "widgets",
    status: "active",
    created_at: "2024-01-01T00:00:00",
    updated_at: "2024-01-01T00:00:00",
  },
  {
    id: "p2",
    name: "Valve B",
    sku: "V-002",
    category: null,
    status: "discontinued",
    created_at: "2024-01-02T00:00:00",
    updated_at: "2024-01-02T00:00:00",
  },
];

describe("ProductsPage", () => {
  beforeEach(() => {
    mockList.mockResolvedValue(sampleProducts);
    mockCreate.mockResolvedValue(sampleProducts[0]);
    mockDelete.mockResolvedValue(undefined);
  });

  it("shows loading then renders product table", async () => {
    render(<ProductsPage />);
    expect(screen.getByText(/Loading/i)).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText("Widget A")).toBeInTheDocument());
    expect(screen.getByText("Valve B")).toBeInTheDocument();
  });

  it("renders SKUs in the table", async () => {
    render(<ProductsPage />);
    await waitFor(() => expect(screen.getByText("W-001")).toBeInTheDocument());
    expect(screen.getByText("V-002")).toBeInTheDocument();
  });

  it("shows — when category is null", async () => {
    render(<ProductsPage />);
    await waitFor(() => expect(screen.getByText("—")).toBeInTheDocument());
  });

  it("renders active/discontinued status badges", async () => {
    render(<ProductsPage />);
    await waitFor(() => expect(screen.getByText("active")).toBeInTheDocument());
    expect(screen.getByText("discontinued")).toBeInTheDocument();
  });

  it("opens Add Product dialog when Add Product button clicked", async () => {
    render(<ProductsPage />);
    await waitFor(() => screen.getByText("Widget A"));
    fireEvent.click(screen.getByRole("button", { name: /Add Product/i }));
    expect(screen.getByText("Add Product", { selector: "[class*='DialogTitle'], h2, h3" })).toBeInTheDocument();
  });

  it("shows search input", async () => {
    render(<ProductsPage />);
    await waitFor(() => screen.getByText("Widget A"));
    expect(screen.getByPlaceholderText(/Search products/i)).toBeInTheDocument();
  });

  it("shows empty state when no products", async () => {
    mockList.mockResolvedValue([]);
    render(<ProductsPage />);
    await waitFor(() => expect(screen.getByText(/No products found/i)).toBeInTheDocument());
  });

  it("calls listProducts with search term on input change", async () => {
    render(<ProductsPage />);
    await waitFor(() => screen.getByText("Widget A"));
    fireEvent.change(screen.getByPlaceholderText(/Search products/i), {
      target: { value: "widget" },
    });
    await waitFor(() => expect(mockList).toHaveBeenCalledWith("widget"));
  });
});
