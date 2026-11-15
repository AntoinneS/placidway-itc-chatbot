# PlacidWay Website Knowledge Chatbot — ITC Immunity Therapy Center

**Candidate:** Antoinne Stewart  
**Role:** AI Automation Engineer (PlacidWay assessment)  
**Live demo:** https://placidway-itc-chatbot.pages.dev  
**Last updated:** 15 November 2026

A small, reliable chatbot that answers visitor questions **only** from the 7 PlacidWay pages named in the assessment. It cites its source for every answer, and says “I don’t know” — with a pointer to a free PlacidWay quote — when the answer is not in those pages. It never invents prices, clinics, or medical facts.

## What I chose, and why

| Choice | Why |
|---|---|
| **Static site, no server, no LLM API key** | Free to host (Cloudflare Pages, $0), nothing to keep running, no API cost, no secrets in the code. The assessment explicitly allows free tiers / local models, and does not reimburse API costs. |
| **Client-side retrieval, not a generative LLM at answer time** | This is the grounding guarantee. Answers are assembled only from pre-checked chunks in `knowledge-base.json`. A generative model asked to “answer from the pages” can still paraphrase a price into existence; a retrieval bot with a threshold cannot — below the threshold it falls back to “I don’t know”. |
| **Python ingestion (`ingest.py`) + hand-checked knowledge base** | Ingestion is automated and repeatable (1 req/sec, clear User-Agent, only the 7 URLs), but the knowledge base is curated by hand from the extracted text, so every chunk was verified before it shipped. Re-running ingestion does not silently change answers. |
| **Plain HTML/CSS/JavaScript, one `index.html`** | Easy to review in the 45-minute review call, easy to change live, no build step to break. |

## The 7 source pages (only these)

1. ITC profile — https://www.placidway.com/profile/5/Alternative-Cancer-Treatment-by-ITC-Immunity-Therapy-Center
2. Adenocarcinoma package — https://www.placidway.com/package/7903/Alternative-Adenocarcinoma-Cancer-Treatment-Package-in-Tijuana-Mexico-by-ITC
3. Adrenal package — https://www.placidway.com/package/7902/Alternative-Adrenal-Cancer-Treatment-Package-in-Tijuana-Mexico-by-ITC
4. Anal package — https://www.placidway.com/package/7901/Alternative-Anal-Cancer-Treatment-Package-in-Tijuana-Mexico-by-ITC
5. ITC videos — https://www.placidway.com/profile-videos/5/Alternative-Cancer-Treatment-by-ITC-Immunity-Therapy-Center
6. ITC price list — https://www.placidway.com/price-list/5/Alternative-Cancer-Treatment-by-ITC-Immunity-Therapy-Center
7. Price comparison 2026 — https://www.placidway.com/search-medical-pricings/Alternative-Medicine/All/1

Ingested 15 November 2026. Key facts verified that day: all three ITC packages are **$18,995 USD Out-Patient / $30,000 USD In-Patient, 3 weeks**; the price list is **$18,995 USD** for breast, prostate, lung, pancreatic, colorectal, and colon; the comparison page prices are **starting estimates only**.

## How it works

```
7 PlacidWay URLs
  → ingest.py (requests + BeautifulSoup, ~1 req/sec, User-Agent: PlacidWay-Assessment-Bot/1.0)
  → data/raw/*.txt snapshots + ingestion-report.md
  → knowledge-base.json (29 hand-checked chunks, each with a source URL)
  → index.html: tokenise question → score chunks (keyword/phrase overlap + synonym map)
       → guardrails FIRST (booking / weather / medical advice / wrong-price trick)
       → best chunk above threshold → answer + source link(s)
       → below threshold → honest “I don’t know” + free-quote pointer + local log entry
```

**Argon review (15 Nov 2026, Gemini 4 Argon, chat “Muse Query - PlacidWay Chatbot Argon Review”):** Argon scored the first draft 83.5/100 and caught one real error in my source summary — $50 *does* appear in the pages, as the $50–$250 general initial holistic consultation range, not as an ITC price. That is now fixed in the bot, the KB, and the test results. Argon also flagged package cross-contamination (7901/7902/7903), follow-up carryover, and general-abroad vs ITC price confusion. Fixes applied: entity-gated retrieval (a question naming one cancer type can only retrieve that package + general ITC chunks), scope tags (`itc_clinic_specific` vs `general_abroad_comparison` vs `video_title_only`) on every KB chunk, a deterministic router (booking / weather / medical advice handled before retrieval, never carried over from a previous topic), a $50 price-interceptor, and a “Run 8 verification tests” button in the UI. One Argon suggestion was *not* taken blindly: Argon merged profile-level transport into the Anal package inclusions in its Q3 draft — the package page itself does not list that, so the bot keeps profile and package inclusions separate.

**Guardrails, in order:** (1) booking/appointment — “I can’t book”; (2) weather / out-of-scope — polite decline; (3) personal medical advice (“safe for my diabetes?”) — no diagnosis, refer to a doctor; (4) a $ amount in the question that is not a listed price, asked to be confirmed — corrected, not agreed with; (5) comparison — only if both prices for the *same* treatment are in the pages (Mexico vs Turkey for ITC treatment: Turkey has no ITC price listed, so it says so, and names what *is* listed in Turkey for different treatments).

**Follow-ups:** the bot keeps the last treatment topic in memory, so “what about in Turkey?” and “and what about recovery time?” resolve against the previous question. Recovery time: no specific number of days is stated on the pages — the bot says that, gives the 3-week itinerary and the 3-month follow-up, and does not invent a figure.

## Nice-to-haves included

- **Other languages:** Spanish questions are detected (¿, cuánto, cuesta, tratamiento…) and answered in Spanish from the same facts. Basic Arabic-script detection is in the design; Spanish is the one implemented and tested.
- **Follow-ups:** as above, via last-topic memory.
- **Medical disclaimer:** shown on medical/treatment answers only, once per session — not repeated on every answer. The PlacidWay disclaimer is also in the page footer.
- **Lead capture:** name + email form. Stored only in the visitor’s browser (localStorage) in this demo — nothing is sent to a server. “Email PlacidWay” opens a pre-addressed email to info@placidway.com.
- **Unanswered-question logging:** every “I don’t know” is logged locally (question, reason, timestamp), viewable on the page and downloadable as JSON, so content gaps can be found.

## Run it locally

```bash
# 1. Serve the folder (any static server)
python3 -m http.server 8000
# open http://localhost:8000/

# 2. Refresh the content (re-fetch the 7 pages)
pip install requests beautifulsoup4
python3 ingest.py
# diff data/raw/ against knowledge-base.json, update the KB by hand,
# re-run the 8 test questions, update the "Last updated" stamp.
```

No API key, no environment variable, no build step, no database.

## Deploy (Cloudflare Pages, free)

Direct upload of this folder, or connect the GitHub repo to Cloudflare Pages (build command: none, output directory: `.`). The live URL is a `*.pages.dev` address, public, no login required. Keep it running for at least 7 days after submission, per the assessment.

## Files

- `index.html` — chat UI + retrieval + guardrails (all client-side)
- `knowledge-base.json` — 29 chunks + 7 sources + “not in the KB” list
- `ingest.py` — re-fetch + clean extraction for the 7 URLs only
- `test-results.md` — the bot’s answers to all 8 test questions
- `ingestion-report.md` — generated by `ingest.py` on each refresh

## Known limitations (honest)

- Retrieval is keyword/TF-style scoring, not embeddings — it can miss a well-phrased question that uses none of the page’s words. The threshold + “I don’t know” fallback is the mitigation, not a fix.
- No live LLM: the bot cannot rephrase freely, summarise a long page in new words, or answer in every language. That is a deliberate trade for grounding — see “What I would improve with another week” in the submission document.
- Videos: no transcripts were in the extracted page content, so the bot only reports video titles, never what a video says.
- Prices are as listed on 15 November 2026; PlacidWay’s own disclaimer says prices are estimates only and must be confirmed directly with the provider.
- Lead capture and unanswered-question logging are local to the visitor’s browser in this demo — there is no server to collect them centrally yet.
