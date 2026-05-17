# Demo Notes

## What this project is

A portfolio project demonstrating an **automated analysis and reporting workflow**.
The automation is the point — not the charts, not the PDF. Those are just evidence that it worked.

The value proposition in one sentence:
> Sales data goes in, a polished report lands in your inbox every week — nobody has to touch anything.

---

## Lead with this

Don't open with the tech. Open with the problem:

> "Most business owners glance at last month's revenue and move on. The stuff that actually matters — which products are slipping, which customers are going quiet — just gets missed. Not because they don't care, but because nobody has time to dig."

Then: "This is what I built to fix that."

---

## Demo flow

**1. Show the output first (the PDF)**
Start with `output/report_sample_en.pdf` or `_ja.pdf`.
Let them look at it. Don't rush. The PDF is the most convincing thing in the demo.
Point out: executive summary, product ranking, customer segments, the action notes per chart.

**2. Show how it runs itself**
Open GitHub → Actions → `weekly_report.yml`. (https://github.com/Keybladerhuy/auto-report-flow/actions/workflows/weekly_report.yml)
Show that it runs every Monday 08:00 JST on a schedule — no one triggers it.
If you can, show a recent run log. The green checkmark does a lot of work.

**3. Walk through the pipeline (briefly)**
Diagram in the pitch page, or describe it in three steps:
- Data comes in (Google Sheets or CSV)
- System analyses it and builds the report
- PDF goes out via email (or Teams / Slack)

Don't get into the notebooks or the code unless they ask.

**4. Talk about customisation**
"Everything in the report — the analyses, the layout, the language, how often it runs — can be adjusted to fit your business."
Be specific: "If you track different metrics, we'd swap those in. If you want it in Japanese, that version already exists."

---

## Questions that will come up

**"How much does it cost?"**
Don't give a number unprompted. Scope first:
"It depends on the data and what you need — a simple weekly report is different from a custom dashboard. Happy to put together a quote once I understand your setup."

**"How long does setup take?"**
"First report is usually ready within a few days of getting the data."
If they push: the setup is the fiddly part (connecting the data source, agreeing on what to track). The automation itself is already built.

**"Can it work with my data?"**
Almost always yes. Minimum needed: date, product, quantity, price, customer ID.
"If your data looks different, that's fine — we'd work it out."

**"Is it secure / where does the data go?"**
The data stays in their own Google Sheet or is sent as a file. The analysis runs in a private pipeline. Nothing is stored by third parties beyond what they already use (Google, GitHub).

**"Can I see it run live?"**
Ideally yes — trigger a run and show the email arriving.
If not: show the GitHub Actions log from the last scheduled run.

---

## Things to remember

- **Lead with the automation, not the analysis.** The charts are nice; the fact that they appear automatically is the product.
- **Make it specific to them.** Generic demos lose people. Ask early: "What does your current reporting look like?" Then map your answer to their situation.
- **The Japanese version is a differentiator.** If the audience is Japan-based, lead with `report_sample_ja.pdf`.
- **You don't need to show the code.** This is a business demo, not a technical interview. Only go there if they ask.
