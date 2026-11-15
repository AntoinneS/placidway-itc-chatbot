# PlacidWay AI Automation Assessment — Built Chatbot Assessment
**Candidate:** Antoinne Stewart — antoinnestewart@yahoo.com  
**Role:** AI Automation Engineer — Website Knowledge Chatbot  
**Date:** 15 November 2026

## Live demo
**Public demo link:** https://placidway-itc-chatbot.pages.dev  
Public, no login required. Keep running for at least 7 days after submission, per the assessment.

**Code:** GitHub repository link / zip — [TO BE INSERTED — repo to be created from ~/workspace/placidway-chatbot/]  
Files: `index.html`, `knowledge-base.json`, `ingest.py`, `README.md`, `test-results.md`

## What I built
A small, reliable chatbot that answers visitor questions **only** from the 7 PlacidWay pages named in the assessment, about ITC Immunity Therapy Center in Tijuana, Mexico. Every answer cites its source URL. If the answer is not in those pages, the bot says "I don't know" and points to a free PlacidWay quote (+1-888-296-6664, info@placidway.com). It never invents prices, clinics, or medical facts.

## What I chose, and why
- **Static site, no server, no LLM API key ($0, Cloudflare Pages free).** No API cost (the assessment does not reimburse API costs), no secrets in the code, nothing to keep running.
- **Client-side retrieval, not a generative LLM at answer time.** This is the grounding guarantee. Answers come only from pre-checked chunks in `knowledge-base.json`. A generative model can still paraphrase a price into existence; a retrieval bot with a threshold cannot — below the threshold it falls back to "I don't know".
- **Python ingestion + hand-checked knowledge base.** `ingest.py` re-fetches only the 7 URLs (~1 request/second, clear User-Agent `PlacidWay-Assessment-Bot/1.0`), strips navigation/scripts, and saves clean snapshots. The knowledge base (30 chunks) was curated by hand from that text, so every chunk was verified before it shipped. Re-running ingestion does not silently change answers.
- **Deterministic router before retrieval.** Booking, weather, personal medical advice, and wrong-price confirmation are handled by fixed rules first — they can never be "answered" by retrieval. Follow-up carryover is gated: it only applies to follow-up markers ("what about…", "and what about…") and never to booking/weather/medical questions.
- **Entity-gated retrieval.** If a question names one cancer type, only that package's chunks + general ITC chunks can win. The three packages (Adenocarcinoma 7903, Adrenal 7902, Anal 7901) have near-identical text and the same prices, so flat retrieval would cite the wrong package. Scope tags on every chunk (`itc_clinic_specific` vs `general_abroad_comparison` vs `video_title_only`) stop general-abroad prices being presented as ITC prices.

## The 7 source pages
1. ITC profile — https://www.placidway.com/profile/5/Alternative-Cancer-Treatment-by-ITC-Immunity-Therapy-Center
2. Adenocarcinoma package — https://www.placidway.com/package/7903/Alternative-Adenocarcinoma-Cancer-Treatment-Package-in-Tijuana-Mexico-by-ITC
3. Adrenal package — https://www.placidway.com/package/7902/Alternative-Adrenal-Cancer-Treatment-Package-in-Tijuana-Mexico-by-ITC
4. Anal package — https://www.placidway.com/package/7901/Alternative-Anal-Cancer-Treatment-Package-in-Tijuana-Mexico-by-ITC
5. ITC videos — https://www.placidway.com/profile-videos/5/Alternative-Cancer-Treatment-by-ITC-Immunity-Therapy-Center
6. ITC price list — https://www.placidway.com/price-list/5/Alternative-Cancer-Treatment-by-ITC-Immunity-Therapy-Center
7. Price comparison 2026 — https://www.placidway.com/search-medical-pricings/Alternative-Medicine/All/1

Ingested 15 November 2026. Key verified facts: all three packages $18,995 USD Out-Patient / $30,000 USD In-Patient, 3 weeks; price list $18,995 USD for breast, prostate, lung, pancreatic, colorectal, colon; comparison-page prices are starting estimates only.

## Architecture
```
7 PlacidWay URLs
  → ingest.py (requests + BeautifulSoup, ~1 req/sec, clear User-Agent)
  → data/raw/*.txt + ingestion-report.md
  → knowledge-base.json (30 hand-checked chunks, source URL + cancer_type + scope + topic each)
  → index.html: deterministic router → entity-gated retrieval (keyword/phrase + synonym map, topic boosts)
       → best chunk above threshold → answer + source link(s)
       → below threshold → honest "I don't know" + free-quote pointer + local log entry
```
Run locally: `python3 -m http.server 8000` in the project folder, open http://localhost:8000/. No API key, no build step, no database. Refresh: `pip install requests beautifulsoup4 && python3 ingest.py`, diff the snapshots, update the KB by hand, re-run the 8 tests (there is a "Run 8 verification tests" button in the UI), update the "Last updated" stamp.

## Nice-to-haves included
- Spanish questions detected and answered in Spanish from the same facts.
- Follow-ups using chat history ("what about in Turkey?", "and what about recovery time?").
- Short medical disclaimer on medical/treatment answers only, once per session — not on every answer. PlacidWay's own disclaimer is in the page footer.
- Lead capture: name + email form, stored only in the visitor's browser in this demo (nothing sent to a server); "Email PlacidWay" opens a pre-addressed email to info@placidway.com.
- Logging of unanswered questions: logged locally with reason + timestamp, viewable on the page and downloadable as JSON.

## Test results — all 8 questions (full text in test-results.md; also testable live via the buttons on the demo page)
1. **Cost — adenocarcinoma in Tijuana:** $18,995 USD Out-Patient / $30,000 USD In-Patient, 3 weeks. Pass.
2. **Comparison — adrenal, Mexico or Turkey:** Cannot compare — no ITC price in Turkey is listed for that treatment. Mexico price given ($18,995 / $30,000). Pass.
3. **Procedure — what is included in the anal package:** Out-Patient inclusions listed (weekly labs, one imaging, core therapies, 2 meals daily, standard medications, 3-month follow-up); In-Patient version also answered. Pass.
4. **Follow-up — recovery time:** No specific recovery time in days is stated. Gives the 3-week itinerary + 3-month follow-up instead. Pass.
5. **Not in content — book an appointment for tomorrow:** Cannot book; points to free quote / medical-review process. Pass.
6. **Out of scope — weather in Cancun:** Politely declines. Pass.
7. **Medical advice — safe for my diabetes:** No diagnosis; notes surgeries/biopsies are excluded from the packages; refers to a doctor + physician review. Pass.
8. **Trick — "I heard it costs $50. Confirm that.":** No — $50 is not an ITC package price. $50 does appear as the low end of the $50–$250 general initial holistic consultation range on the comparison page (starting estimates, not ITC). Pass.

Verified locally with an automated harness: 13/13 checks passed (the 8 test questions + doctors, travel, generic cost, dental-implant out-of-KB, and Out-Patient inclusions).

## Source-fact audit — a mistake I caught before submitting
My first source summary wrongly said "$50 appears nowhere in the pages". It does — as the $50–$250 consultation range above. That was caught in a Gemini 4 Argon review (chat "Muse Query - PlacidWay Chatbot Argon Review", 15 Nov 2026) and fixed in the bot, the knowledge base, and the test results before submission. Argon also flagged package cross-contamination, follow-up carryover, and general-vs-ITC price confusion; all three were fixed as described above. One Argon suggestion was not taken blindly: it merged profile-level transport into the Anal package inclusions — the package page does not list that, so the bot keeps profile and package inclusions separate.

## What I would improve with another week, and known limitations
**Limitations:** Retrieval is keyword-based, not embeddings — a heavily paraphrased question using none of the page's words may miss, and the threshold + "I don't know" is the mitigation, not a fix. No live LLM, so the bot cannot rephrase freely or answer in every language — a deliberate trade for grounding. Videos: no transcripts were in the extracted page content, so the bot reports video titles only, never what a video says. Prices are as listed on 15 November 2026; PlacidWay's own disclaimer says prices are estimates only and must be confirmed directly with the provider. Lead capture and unanswered-question logging are local to the visitor's browser in this demo — there is no server to collect them centrally yet. Multi-turn memory tracks one active treatment; complex "compare the first one I asked about with the second one" references fall back to "I don't know" rather than guessing.

**With another week:** (1) Hybrid BM25 + quantized client-side embeddings that only re-rank already scope-filtered chunks — never generating free text. (2) A nightly drift check: re-run `ingest.py`, open a pull request with a diff if any price, doctor, or inclusion changes, and re-run the 8 tests before the KB can be updated. (3) Schema validation on ingestion, so a page redesign that drops a required field halts ingestion instead of overwriting the KB with incomplete data. (4) An in-browser dashboard for unanswered questions (top topics, language, time) to prioritise which KB chunks to add next — without sending any data to a server.

---
Antoinne Stewart — antoinnestewart@yahoo.com — 15 November 2026
