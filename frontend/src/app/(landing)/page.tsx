"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  ShieldCheck,
  ArrowRight,
  Zap,
  BarChart3,
  Brain,
  Layers,
  CheckCircle2,
  XCircle,
  Boxes,
  ClipboardCheck,
  AlertTriangle,
  ChevronRight,
  Sparkles,
} from "lucide-react";

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-white text-slate-900">
      {/* ── Navbar ── */}
      <nav className="sticky top-0 z-50 border-b bg-white/80 backdrop-blur-md">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <Link href="/" className="flex items-center gap-2">
            <ShieldCheck className="h-7 w-7 text-red-600" />
            <span className="text-xl font-bold tracking-tight text-slate-900">
              DClaw Quality
            </span>
          </Link>
          <div className="hidden items-center gap-8 text-sm font-medium text-slate-600 md:flex">
            <a href="#features" className="hover:text-red-600 transition-colors">
              Features
            </a>
            <a href="#how-it-works" className="hover:text-red-600 transition-colors">
              How It Works
            </a>
            <a href="#comparison" className="hover:text-red-600 transition-colors">
              Why Us
            </a>
          </div>
          <div className="flex items-center gap-3">
            <Link href="/dashboard">
              <Button variant="ghost" size="sm" className="hidden md:inline-flex">
                Dashboard
              </Button>
            </Link>
            <Link href="/dashboard">
              <Button
                size="sm"
                className="bg-red-600 hover:bg-red-700 text-white"
              >
                Launch App <ArrowRight className="ml-1 h-4 w-4" />
              </Button>
            </Link>
          </div>
        </div>
      </nav>

      {/* ── Hero ── */}
      <section className="relative overflow-hidden bg-gradient-to-b from-white via-slate-50 to-white">
        <div className="mx-auto max-w-7xl px-6 py-24 md:py-32">
          <div className="grid gap-12 lg:grid-cols-2 lg:gap-16 items-center">
            <div className="space-y-8">
              <div className="inline-flex items-center gap-2 rounded-full bg-red-50 px-4 py-1.5 text-sm font-medium text-red-700">
                <Sparkles className="h-4 w-4" />
                AI-Powered Quality Management
              </div>
              <h1 className="text-4xl font-extrabold tracking-tight text-slate-900 md:text-5xl lg:text-6xl">
                Quality Control,{" "}
                <span className="text-red-600">Accelerated</span>
              </h1>
              <p className="text-lg leading-relaxed text-slate-600 md:text-xl">
                Replace spreadsheets and expensive QMS suites with a modern,
                affordable quality platform that works in{" "}
                <span className="font-semibold text-slate-900">days, not quarters</span>.
                AI-assisted defect analysis, real-time dashboards, and full
                traceability from product to defect.
              </p>
              <div className="flex flex-wrap gap-4">
                <Link href="/dashboard">
                  <Button
                    size="lg"
                    className="bg-red-600 hover:bg-red-700 text-white px-8"
                  >
                    Launch the App
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Button>
                </Link>
                <a href="#features">
                  <Button
                    variant="outline"
                    size="lg"
                    className="px-8 border-slate-300"
                  >
                    Explore Features
                  </Button>
                </a>
              </div>
              <div className="flex items-center gap-6 text-sm text-slate-500">
                <div className="flex items-center gap-1.5">
                  <CheckCircle2 className="h-4 w-4 text-emerald-500" />
                  Zero setup time
                </div>
                <div className="flex items-center gap-1.5">
                  <CheckCircle2 className="h-4 w-4 text-emerald-500" />
                  Docker-ready
                </div>
                <div className="flex items-center gap-1.5">
                  <CheckCircle2 className="h-4 w-4 text-emerald-500" />
                  Open source
                </div>
              </div>
            </div>

            {/* Hero visual — abstract dashboard mockup */}
            <div className="relative">
              <div className="absolute -inset-4 rounded-3xl bg-gradient-to-tr from-red-100 via-slate-100 to-emerald-50 opacity-70 blur-2xl" />
              <div className="relative rounded-2xl border border-slate-200 bg-white shadow-2xl overflow-hidden">
                <div className="border-b bg-slate-50 px-4 py-3 flex items-center gap-2">
                  <div className="h-3 w-3 rounded-full bg-red-400" />
                  <div className="h-3 w-3 rounded-full bg-amber-400" />
                  <div className="h-3 w-3 rounded-full bg-emerald-400" />
                  <span className="ml-2 text-xs text-slate-400">DClaw Quality — Dashboard</span>
                </div>
                <div className="grid grid-cols-2 gap-4 p-6">
                  <div className="rounded-xl bg-slate-50 p-4">
                    <div className="text-xs text-slate-500 mb-1">Pass Rate</div>
                    <div className="text-2xl font-bold text-emerald-600">94.2%</div>
                    <div className="mt-2 h-2 w-full rounded-full bg-slate-200">
                      <div className="h-2 w-[94%] rounded-full bg-emerald-500" />
                    </div>
                  </div>
                  <div className="rounded-xl bg-slate-50 p-4">
                    <div className="text-xs text-slate-500 mb-1">Defects</div>
                    <div className="text-2xl font-bold text-red-600">12</div>
                    <div className="mt-2 flex gap-1">
                      <div className="h-2 flex-1 rounded-full bg-red-300" />
                      <div className="h-2 flex-1 rounded-full bg-amber-300" />
                      <div className="h-2 flex-1 rounded-full bg-slate-200" />
                    </div>
                  </div>
                  <div className="col-span-2 rounded-xl bg-slate-50 p-4">
                    <div className="text-xs text-slate-500 mb-2">Recent Inspections</div>
                    <div className="space-y-2">
                      <div className="flex items-center justify-between rounded-lg bg-white px-3 py-2 text-xs">
                        <span className="font-medium">Visual Inspection — Batch #A-102</span>
                        <span className="rounded-full bg-emerald-100 px-2 py-0.5 text-emerald-700">Pass</span>
                      </div>
                      <div className="flex items-center justify-between rounded-lg bg-white px-3 py-2 text-xs">
                        <span className="font-medium">Dimensional Check — Batch #A-103</span>
                        <span className="rounded-full bg-red-100 px-2 py-0.5 text-red-700">Fail</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Stats Band ── */}
      <section className="border-y bg-slate-900 py-12">
        <div className="mx-auto max-w-7xl px-6">
          <div className="grid grid-cols-2 gap-8 md:grid-cols-4 text-center">
            <div>
              <div className="text-3xl font-bold text-white">5 min</div>
              <div className="mt-1 text-sm text-slate-400">Time to first inspection</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-white">100%</div>
              <div className="mt-1 text-sm text-slate-400">Database-backed — zero mocks</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-white">AI</div>
              <div className="mt-1 text-sm text-slate-400">Defect classification engine</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-white">Docker</div>
              <div className="mt-1 text-sm text-slate-400">One command, full stack</div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Features ── */}
      <section id="features" className="py-24">
        <div className="mx-auto max-w-7xl px-6">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl font-bold tracking-tight text-slate-900 md:text-4xl">
              Everything you need to run quality
            </h2>
            <p className="mt-4 text-lg text-slate-600">
              From product registration to AI defect analysis — a complete traceability chain.
            </p>
          </div>
          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            <Card className="border-slate-200">
              <CardHeader>
                <div className="mb-3 inline-flex h-10 w-10 items-center justify-center rounded-lg bg-red-50 text-red-600">
                  <Layers className="h-5 w-5" />
                </div>
                <CardTitle>Full Traceability</CardTitle>
                <CardDescription>
                  Product → Batch → Inspection → Defect. Every step linked, every record
                  auditable.
                </CardDescription>
              </CardHeader>
              <CardContent className="text-sm text-slate-600">
                Cascading relationships with automatic on-delete rules keep your data
                consistent and clean.
              </CardContent>
            </Card>

            <Card className="border-slate-200">
              <CardHeader>
                <div className="mb-3 inline-flex h-10 w-10 items-center justify-center rounded-lg bg-red-50 text-red-600">
                  <Brain className="h-5 w-5" />
                </div>
                <CardTitle>AI Defect Copilot</CardTitle>
                <CardDescription>
                  Describe a defect in plain English and get instant classification,
                  severity scoring, and corrective actions.
                </CardDescription>
              </CardHeader>
              <CardContent className="text-sm text-slate-600">
                  Runs entirely offline with a rules-based engine — no API keys, no
                  latency, no bill shock.
              </CardContent>
            </Card>

            <Card className="border-slate-200">
              <CardHeader>
                <div className="mb-3 inline-flex h-10 w-10 items-center justify-center rounded-lg bg-red-50 text-red-600">
                  <BarChart3 className="h-5 w-5" />
                </div>
                <CardTitle>Real-Time Dashboard</CardTitle>
                <CardDescription>
                  Live pass rates, defect severity breakdowns, batch status
                  distribution, and recent inspection feeds.
                </CardDescription>
              </CardHeader>
              <CardContent className="text-sm text-slate-600">
                Every number comes from your database. No mock data, no stale exports,
                no Excel gymnastics.
              </CardContent>
            </Card>

            <Card className="border-slate-200">
              <CardHeader>
                <div className="mb-3 inline-flex h-10 w-10 items-center justify-center rounded-lg bg-red-50 text-red-600">
                  <ClipboardCheck className="h-5 w-5" />
                </div>
                <CardTitle>Structured Inspections</CardTitle>
                <CardDescription>
                  Log visual, dimensional, functional, or custom inspection types
                  with pass / fail / pending results.
                </CardDescription>
              </CardHeader>
              <CardContent className="text-sm text-slate-600">
                Filter by result, date range, or batch. Searchable, paginated, and
                ready for audit.
              </CardContent>
            </Card>

            <Card className="border-slate-200">
              <CardHeader>
                <div className="mb-3 inline-flex h-10 w-10 items-center justify-center rounded-lg bg-red-50 text-red-600">
                  <Boxes className="h-5 w-5" />
                </div>
                <CardTitle>Batch Lifecycle</CardTitle>
                <CardDescription>
                  Track batches from in-production through QA to passed, failed, or
                  shipped with full quantity history.
                </CardDescription>
              </CardHeader>
              <CardContent className="text-sm text-slate-600">
                Color-coded status badges and filterable tables keep production flow
                visible at a glance.
              </CardContent>
            </Card>

            <Card className="border-slate-200">
              <CardHeader>
                <div className="mb-3 inline-flex h-10 w-10 items-center justify-center rounded-lg bg-red-50 text-red-600">
                  <Zap className="h-5 w-5" />
                </div>
                <CardTitle>Zero-to-Value in 48 Hours</CardTitle>
                <CardDescription>
                  One Docker command spins up the entire stack. No consultants, no
                  six-month implementation cycles.
                </CardDescription>
              </CardHeader>
              <CardContent className="text-sm text-slate-600">
                Built for teams that need to move fast: startups, contract
                manufacturers, and agile quality departments.
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* ── How It Works ── */}
      <section id="how-it-works" className="bg-slate-50 py-24">
        <div className="mx-auto max-w-7xl px-6">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl font-bold tracking-tight text-slate-900 md:text-4xl">
              From signup to first inspection in 5 minutes
            </h2>
            <p className="mt-4 text-lg text-slate-600">
              DClaw Quality is designed for teams that can't wait for enterprise onboarding.
            </p>
          </div>
          <div className="grid gap-8 md:grid-cols-4">
            {[
              {
                step: "01",
                title: "Add Products",
                desc: "Register your product catalog with SKU, category, and lifecycle status.",
                icon: <Boxes className="h-5 w-5" />,
              },
              {
                step: "02",
                title: "Create Batches",
                desc: "Log production runs with quantity, date, and current status.",
                icon: <Layers className="h-5 w-5" />,
              },
              {
                step: "03",
                title: "Run Inspections",
                desc: "Quality checks with inspector name, type, result, and timestamp.",
                icon: <ClipboardCheck className="h-5 w-5" />,
              },
              {
                step: "04",
                title: "Log & Classify Defects",
                desc: "Use AI Suggest to auto-classify defects and get corrective actions instantly.",
                icon: <Sparkles className="h-5 w-5" />,
              },
            ].map((item) => (
              <div key={item.step} className="relative">
                <div className="rounded-2xl border border-slate-200 bg-white p-6 h-full">
                  <div className="mb-4 flex items-center justify-between">
                    <div className="inline-flex h-10 w-10 items-center justify-center rounded-lg bg-red-50 text-red-600">
                      {item.icon}
                    </div>
                    <span className="text-3xl font-extrabold text-slate-100">
                      {item.step}
                    </span>
                  </div>
                  <h3 className="text-lg font-semibold text-slate-900">
                    {item.title}
                  </h3>
                  <p className="mt-2 text-sm text-slate-600">{item.desc}</p>
                </div>
                {item.step !== "04" && (
                  <div className="hidden md:block absolute top-1/2 -right-4 text-slate-300">
                    <ChevronRight className="h-5 w-5" />
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Comparison ── */}
      <section id="comparison" className="py-24">
        <div className="mx-auto max-w-7xl px-6">
          <div className="mx-auto max-w-2xl text-center mb-16">
            <h2 className="text-3xl font-bold tracking-tight text-slate-900 md:text-4xl">
              Escape the spreadsheet → enterprise trap
            </h2>
            <p className="mt-4 text-lg text-slate-600">
              Mid-market manufacturers are stuck between two broken options. We built the third.
            </p>
          </div>
          <div className="mx-auto max-w-4xl overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
            <table className="w-full text-sm">
              <thead className="bg-slate-50">
                <tr>
                  <th className="px-6 py-4 text-left font-semibold text-slate-700">
                    Approach
                  </th>
                  <th className="px-6 py-4 text-left font-semibold text-slate-700">
                    Cost
                  </th>
                  <th className="px-6 py-4 text-left font-semibold text-slate-700">
                    Time to Value
                  </th>
                  <th className="px-6 py-4 text-left font-semibold text-slate-700">
                    AI / Analytics
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-t">
                  <td className="px-6 py-4 font-medium text-slate-900">
                    <span className="inline-flex items-center gap-2">
                      <XCircle className="h-4 w-4 text-red-500" />
                      Spreadsheets / SharePoint
                    </span>
                  </td>
                  <td className="px-6 py-4 text-slate-600">$</td>
                  <td className="px-6 py-4 text-red-600">∞ (manual forever)</td>
                  <td className="px-6 py-4 text-slate-600">None</td>
                </tr>
                <tr className="border-t bg-slate-50/50">
                  <td className="px-6 py-4 font-medium text-slate-900">
                    <span className="inline-flex items-center gap-2">
                      <XCircle className="h-4 w-4 text-amber-500" />
                      MasterControl / EtQ
                    </span>
                  </td>
                  <td className="px-6 py-4 text-slate-600">$$$$</td>
                  <td className="px-6 py-4 text-amber-600">6 months+</td>
                  <td className="px-6 py-4 text-slate-600">Limited / bolt-on</td>
                </tr>
                <tr className="border-t border-red-200 bg-red-50/30">
                  <td className="px-6 py-4 font-semibold text-red-700">
                    <span className="inline-flex items-center gap-2">
                      <CheckCircle2 className="h-4 w-4 text-emerald-600" />
                      DClaw Quality
                    </span>
                  </td>
                  <td className="px-6 py-4 font-medium text-slate-900">$$</td>
                  <td className="px-6 py-4 font-medium text-emerald-700">
                    48 hours
                  </td>
                  <td className="px-6 py-4 font-medium text-slate-900">
                    Built-in AI classification + real-time dashboards
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="bg-gradient-to-br from-red-600 to-red-700 py-24">
        <div className="mx-auto max-w-3xl px-6 text-center">
          <h2 className="text-3xl font-bold tracking-tight text-white md:text-4xl">
            Ready to replace spreadsheets?
          </h2>
          <p className="mt-4 text-lg text-red-100">
            Spin up DClaw Quality in one command. Start logging inspections today.
          </p>
          <div className="mt-10 flex flex-wrap justify-center gap-4">
            <Link href="/dashboard">
              <Button
                size="lg"
                className="bg-white text-red-700 hover:bg-red-50 px-8"
              >
                Launch the App
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <a href="https://github.com/dclawstack/dclaw-quality" target="_blank" rel="noreferrer">
              <Button
                size="lg"
                variant="outline"
                className="border-white text-white hover:bg-white/10 px-8"
              >
                View on GitHub
              </Button>
            </a>
          </div>
          <div className="mt-8 flex justify-center gap-6 text-sm text-red-200">
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="h-4 w-4" /> Docker-ready
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="h-4 w-4" /> PostgreSQL-backed
            </span>
            <span className="flex items-center gap-1.5">
              <CheckCircle2 className="h-4 w-4" /> MIT License
            </span>
          </div>
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="border-t bg-white py-12">
        <div className="mx-auto max-w-7xl px-6">
          <div className="flex flex-col items-center justify-between gap-6 md:flex-row">
            <div className="flex items-center gap-2">
              <ShieldCheck className="h-6 w-6 text-red-600" />
              <span className="text-lg font-bold text-slate-900">DClaw Quality</span>
            </div>
            <div className="flex gap-6 text-sm text-slate-500">
              <Link href="/dashboard" className="hover:text-slate-900">
                Dashboard
              </Link>
              <a href="#features" className="hover:text-slate-900">
                Features
              </a>
              <a href="https://github.com/dclawstack/dclaw-quality" target="_blank" rel="noreferrer" className="hover:text-slate-900">
                GitHub
              </a>
            </div>
            <p className="text-sm text-slate-400">
              © {new Date().getFullYear()} DClaw Quality. Built on the DClaw Stack.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
