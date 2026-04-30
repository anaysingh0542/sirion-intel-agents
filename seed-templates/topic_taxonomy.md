# Sirion Competitive Intelligence — Topic Taxonomy

The canonical taxonomy for all competitive intelligence agents. Agents read this
file every run to classify signals, tag analyses, and structure drill-down queries.

## Competitor Tiers

### Tier 1: Direct CLM

Companies whose primary product is contract lifecycle management — Sirion's
direct competitive set in enterprise deals.

| Slug | Company | HQ | Founded | Notes |
|------|---------|-----|---------|-------|
| icertis | Icertis | Bellevue, WA | 2009 | Leader in Gartner MQ; dominant in large enterprise |
| agiloft | Agiloft | Redwood City, CA | 1991 | No-code CLM; strong mid-market + public sector |
| docusign-clm | DocuSign CLM | San Francisco, CA | 2003 | CLM via Springcm acquisition; e-signature distribution |
| ironclad | Ironclad | San Francisco, CA | 2014 | Digital contracting; developer-friendly API; AI push |
| malbek | Malbek | Morristown, NJ | 2017 | AI-native CLM; mid-market focus |
| conga | Conga | Broomfield, CO | 2006 | Revenue lifecycle; CLM + CPQ + document automation |

### Tier 2: AI-Native Contract

Startups building contract platforms with AI as the core differentiator rather
than a bolt-on. Often target legal teams directly (vs. procurement/legal/sales
split in traditional CLM).

| Slug | Company | HQ | Founded | Notes |
|------|---------|-----|---------|-------|
| juro | Juro | London, UK | 2016 | In-browser contract editor; AI-native |
| spotdraft | SpotDraft | San Francisco, CA | 2017 | AI contract management for legal teams |
| precisely | Precisely | London, UK | 2016 | AI contract review + analytics |
| contractpodai | ContractPodAi | London, UK | 2012 | AI-powered CLM; Leah AI assistant |

### Tier 3: Legal AI

AI companies focused on legal workflows — not CLM-first, but increasingly
overlapping as they add contract analysis, review, and management features.

| Slug | Company | HQ | Founded | Notes |
|------|---------|-----|---------|-------|
| harvey | Harvey | San Francisco, CA | 2022 | LLM for legal; well-funded; enterprise law firms |
| cocounsel | CoCounsel / Thomson Reuters | Toronto, ON | 2023 | AI assistant integrated into Westlaw/Practical Law |
| luminance | Luminance | London, UK | 2015 | AI for contract review + due diligence |
| robin-ai | Robin AI | London, UK | 2019 | AI contract drafting + review |

### Tier 4: Enterprise AI Platforms

Large platform vendors whose AI features may commoditize contract-specific
workflows — the threat is distribution, not product depth.

| Slug | Company | HQ | Notes |
|------|---------|-----|-------|
| servicenow | ServiceNow | Santa Clara, CA | Workflow platform; expanding into legal/procurement |
| salesforce | Salesforce Einstein | San Francisco, CA | CRM AI; contract management via Revenue Cloud |
| microsoft-copilot | Microsoft Copilot | Redmond, WA | M365 AI; Word/SharePoint contract workflows |
| sap | SAP | Walldorf, Germany | Ariba + CLM integration; enterprise procurement |

### Tier 5: Procurement / S2P

Source-to-pay platforms with contract management modules — compete for the
procurement buyer, not legal.

| Slug | Company | HQ | Notes |
|------|---------|-----|-------|
| coupa | Coupa | San Mateo, CA | BSM platform; CLM module; Thoma Bravo-owned |
| sap-ariba | SAP Ariba | Palo Alto, CA | Procurement network; contract workspace |
| ivalua | Ivalua | Redwood City, CA | S2P platform; CLM integrated |
| gep | GEP | Clark, NJ | Procurement software; GEP SMART CLM |

### Tier 6: AI Agent Infrastructure

The platforms and models powering AI features across CLM and legal — Sirion
builds on this layer. Track for capability shifts that create new competitive
dynamics.

| Slug | Company | HQ | Notes |
|------|---------|-----|-------|
| anthropic | Anthropic | San Francisco, CA | Claude models; Sirion's own AI provider |
| openai | OpenAI | San Francisco, CA | GPT models; competitors may build on this |
| google | Google (DeepMind) | Mountain View, CA | Gemini models; Google Cloud AI |
| emerging-frameworks | Emerging agent frameworks | — | LangChain, CrewAI, AutoGen, etc. |

---

## Competitor Dimensions (per competitor)

Each tracked competitor should accumulate intelligence across these 10 dimensions.
Agents tag analyses with the relevant dimension slugs.

| # | Dimension | Slug | Description |
|---|-----------|------|-------------|
| 1 | Product capabilities | `product-capabilities` | Features by module: authoring, negotiation, obligation management, analytics, AI extraction, clause libraries, templates, workflows |
| 2 | Pricing model and packaging | `pricing` | Per-user, per-contract, platform fee, tiered packaging, free trial, enterprise-only |
| 3 | Target market segments | `target-segments` | Enterprise vs. mid-market vs. SMB; industry verticals (pharma, tech, financial services, government) |
| 4 | Key customers and references | `customers` | Named accounts, case studies, logo walls, G2/Gartner Peer Insights reviews |
| 5 | Technology stack / AI approach | `tech-stack` | Which LLM, custom models, RAG architecture, on-prem vs. cloud, SOC2/ISO certifications |
| 6 | Integration ecosystem | `integrations` | Salesforce, SAP, ServiceNow, DocuSign, Adobe Sign, Slack, Teams, custom API |
| 7 | Geographic coverage | `geography` | NA, EMEA, APAC presence; language support; data residency options |
| 8 | Team size and key hires | `team` | Engineering headcount, leadership changes, key hires from competitors |
| 9 | Funding and valuation | `funding` | Last round, total raised, valuation, investors, runway signals |
| 10 | Analyst positioning | `analyst-positioning` | Gartner Magic Quadrant, Forrester Wave, IDC MarketScape placement and movement |

---

## Signal Types (per event)

Every competitive event is classified by one or more signal types. Priority
indicates how urgently the signal should reach Sirion leadership.

| # | Signal Type | Slug | Priority | Description |
|---|------------|------|----------|-------------|
| 1 | Product launch / feature release | `product-launch` | P1 | New capabilities shipped — the strongest competitive signal |
| 2 | Release notes / changelog update | `release-notes` | P1 | Incremental shipping evidence; velocity and direction signal |
| 3 | Pricing change | `pricing-change` | P1 | Packaging, tier changes, discounting patterns |
| 4 | Partnership announcement | `partnership` | P2 | Integration launches, channel partner deals, SI alliances |
| 5 | Customer win / loss | `customer-win-loss` | P2 | Named account wins, competitive displacements, case studies |
| 6 | Funding / M&A | `funding-ma` | P2 | Funding rounds, acquisitions, PE deals, IPO signals |
| 7 | Leadership change | `leadership-change` | P3 | C-suite hires, departures, board changes |
| 8 | Analyst mention | `analyst-mention` | P2 | Gartner, Forrester, IDC coverage; MQ/Wave positioning moves |
| 9 | Conference talk / webinar | `conference` | P3 | Product demos, keynotes, panel appearances, roadmap hints |
| 10 | Marketing narrative shift | `narrative-shift` | P3 | Messaging pivots, category creation attempts, rebrandings |

---

## Themes

Cross-cutting market themes that span multiple competitors and signal types.
Pattern detection agents synthesize across these.

### ai-in-clm

How AI is reshaping contract lifecycle management — from clause extraction to
autonomous contract negotiation. Track which capabilities are becoming table
stakes vs. genuine differentiators.

### market-consolidation

M&A activity, PE roll-ups, acqui-hires, and competitive exits in the CLM and
legal-tech space. Track which companies are acquiring vs. being acquired.

### regulatory-shifts

Regulatory changes affecting contract management: data privacy (GDPR, state
privacy laws), AI governance, ESG reporting requirements, and how competitors
position around compliance.

### enterprise-buyer-trends

How enterprise procurement and legal teams evaluate CLM solutions — RFP
patterns, selection criteria shifts, build-vs-buy decisions, and the role of
analyst reports in purchase decisions.

---

## Taxonomy Tree (agent file paths)

```
competitors/
  direct-clm/           # Icertis, Agiloft, DocuSign CLM, Ironclad, Malbek, Conga
  ai-native-contract/   # Juro, SpotDraft, Precisely, ContractPodAi
  legal-ai/             # Harvey, CoCounsel, Luminance, Robin AI
  enterprise-ai/        # ServiceNow, Salesforce, Microsoft Copilot, SAP
  procurement/          # Coupa, SAP Ariba, Ivalua, GEP
  ai-infra/             # Anthropic, OpenAI, Google, emerging frameworks
signals/
  product-launch/
  release-notes/
  pricing-change/
  partnership/
  customer-win-loss/
  funding-ma/
  leadership-change/
  analyst-mention/
  conference/
  narrative-shift/
themes/
  ai-in-clm/
  market-consolidation/
  regulatory-shifts/
  enterprise-buyer-trends/
```

---

## Usage by Agents

**Tagging:** Every analysis YAML frontmatter includes:
- `tier:` — one of the tier slugs above
- `signals:` — list of signal type slugs
- `dimensions:` — list of competitor dimension slugs (optional)

**Example frontmatter tags:**
```yaml
tier: direct-clm
competitor: Icertis
signals: [product-launch, release-notes]
dimensions: [product-capabilities, tech-stack]
```

**Drill-down queries this taxonomy enables:**
- "Compare Icertis vs Ironclad on clause extraction" → `tier: direct-clm`, `dimension: product-capabilities`
- "Show all pricing changes in the last quarter" → `signal: pricing-change`
- "Which competitors are investing in AI agent infrastructure?" → `theme: ai-in-clm`, `dimension: tech-stack`
- "Track Agiloft's integration ecosystem growth" → `competitor: agiloft`, `dimension: integrations`
