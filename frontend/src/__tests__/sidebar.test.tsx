import { render, screen } from "@testing-library/react";
import Sidebar from "@/components/sidebar";

const mockUsePathname = jest.fn();

jest.mock("next/navigation", () => ({
  usePathname: () => mockUsePathname(),
}));

describe("Sidebar", () => {
  const navItems = [
    { label: "Dashboard", href: "/dashboard" },
    { label: "Products", href: "/products" },
    { label: "Batches", href: "/batches" },
    { label: "Inspections", href: "/inspections" },
    { label: "Defects", href: "/defects" },
  ];

  beforeEach(() => {
    mockUsePathname.mockReturnValue("/dashboard");
    render(<Sidebar />);
  });

  it("renders all 5 nav links", () => {
    navItems.forEach(({ label }) => {
      expect(screen.getByText(label)).toBeInTheDocument();
    });
  });

  it("each nav item has correct href", () => {
    navItems.forEach(({ label, href }) => {
      expect(screen.getByRole("link", { name: new RegExp(label, "i") })).toHaveAttribute("href", href);
    });
  });

  it("active link has red styling when on /dashboard", () => {
    const dashLink = screen.getByRole("link", { name: /dashboard/i });
    expect(dashLink.className).toMatch(/text-red-700/);
  });

  it("inactive links do not have red-700 text", () => {
    const productsLink = screen.getByRole("link", { name: /products/i });
    expect(productsLink.className).not.toMatch(/text-red-700/);
  });

  it("renders brand name", () => {
    expect(screen.getByText("DClaw Quality")).toBeInTheDocument();
  });

  it("marks /products as active when pathname is /products", () => {
    mockUsePathname.mockReturnValue("/products");
    render(<Sidebar />);
    const links = screen.getAllByRole("link", { name: /products/i });
    const activeLink = links.find((l) => l.className.includes("text-red-700"));
    expect(activeLink).toBeTruthy();
  });
});
