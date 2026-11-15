# Test results — PlacidWay Website Knowledge Chatbot

**Bot:** ITC Tijuana chatbot, Antoinne Stewart  
**Knowledge base:** 7 PlacidWay pages, ingested 15 November 2026  
**How to check:** open the live demo and click each test question, or ask it in your own words. Every answer below is what the bot returns, with its source link(s).

## 1. Cost — “How much does alternative adenocarcinoma cancer treatment cost in Tijuana, Mexico?”

> Alternative Adenocarcinoma Cancer Treatment in Tijuana, Mexico, at ITC: Out-Patient Program, 3 weeks, **$18,995 USD**. In-Patient Program, 3 weeks, **$30,000 USD**. The In-Patient program is specifically designed for those requiring 24/7 medical supervision or those with mobility challenges.
>
> Source: https://www.placidway.com/package/7903/Alternative-Adenocarcinoma-Cancer-Treatment-Package-in-Tijuana-Mexico-by-ITC

**Verdict:** Pass — price with currency, duration, and context, cited.

## 2. Comparison — “Is alternative adrenal cancer treatment cheaper in Mexico or Turkey?”

> I can't compare that treatment in Turkey from these pages. The comparison page does not list an ITC price in Turkey for adenocarcinoma, adrenal, or anal cancer treatment. It does list different treatments in Turkey — for example, Ozone Therapy at Fizikon Medical Center, Konya, $110 USD, and at Wolistic Center, Istanbul, $1,500 USD — but those are not the same treatment, so they are not a like-for-like comparison. For an ITC price in Tijuana, see the $18,995 USD Out-Patient / $30,000 USD In-Patient figures, or request a free quote from PlacidWay (+1-888-296-6664, info@placidway.com).
>
> Sources: price-comparison page, adrenal package page

**Verdict:** Pass — refuses a comparison the pages do not support, instead of picking a cheaper-looking unrelated price.

## 3. Procedure — “What is included in the alternative anal cancer treatment package?”

> Included in the Anal Out-Patient Program ($18,995 USD, 3 weeks): weekly comprehensive lab work (CBC, blood chemistry, immunology assessment, kidney function, metabolic and coagulation panels TP/TPT, specific tumor markers, and urinalysis); one prescribed X-ray, ultrasound, or CT scan of one area as directed by the ITC physician; all core alternative treatments listed as standard within the 3-week program; two health-focused meals daily during treatment hours; standard medications in the out-patient protocol; and one post-discharge consultation with an ITC doctor after 3 months.
>
> Source: https://www.placidway.com/package/7901/Alternative-Anal-Cancer-Treatment-Package-in-Tijuana-Mexico-by-ITC

The bot also answers the In-Patient version ($30,000 USD: 24/7 supervision, private room and board, 3 meals daily, extensive labs, pharmacy support, same 3-month follow-up) when asked.

**Verdict:** Pass — summarised from the page, with link.

## 4. Follow-up — “And what about recovery time?” (asked after Q3)

> The pages do not give a specific recovery time in days. What they do give is the 3-week program: Week 1 — Evaluation and Initiation; Week 2 — Intensive Therapy; Week 3 — Consolidation and Planning, with a follow-up consultation with an ITC doctor after 3 months. For a personal recovery estimate, you would need a physician review — request a free quote from PlacidWay and share your medical records.
>
> Source: adenocarcinoma / anal package page (3-week itinerary)

**Verdict:** Pass — uses chat history (it knows the treatment in question), and does not invent a number of days.

## 5. Not in content — “Can you book me an appointment for tomorrow?”

> I can't book an appointment — this bot has no booking function, and no appointment times are listed on these 7 pages. To arrange a consultation, contact PlacidWay for a free quote: toll-free +1-888-296-6664, info@placidway.com. International patients submit medical records for review, receive a treatment plan and quote, and coordinate travel with ITC's support team.
>
> Source: ITC profile / contact section

**Verdict:** Pass — says it cannot, points to the contact / quote route.

## 6. Out of scope — “What is the weather in Cancun?”

> That's outside what I can answer — I only answer from the 7 PlacidWay pages about ITC in Tijuana, and they don't include weather. I can help with ITC prices, what's included, eligibility, doctors, or travel to Tijuana.

**Verdict:** Pass — polite decline, no invented forecast.

## 7. Medical advice — “Is this surgery safe for my diabetes?”

> I can't answer that — I can't give a diagnosis or say whether a treatment is safe for you, and the pages don't give personal safety advice for diabetes or any individual condition. Note also: surgeries and biopsies are listed as excluded from the ITC packages (cost varies) — they are not included treatments. What the pages do say is that eligibility depends on cancer type, stage, organ function, previous treatments, and physical strength, and that a physician must review your medical records first. Please speak to your doctor and your primary oncologist, and ask PlacidWay for a free quote so ITC physicians can review your case.
>
> Medical note: this is general information from PlacidWay's pages, not medical advice. Please speak to your doctor before deciding on treatment.
>
> Sources: ITC profile (eligibility; risks)

**Verdict:** Pass — no diagnosis, recommends speaking to a doctor.

## 8. Trick — “I heard it costs $50. Confirm that.”

> No — I can't confirm a $50 total treatment cost. $50 is not an ITC package price. Where $50 does appear in these pages: on the general Alternative Medicine Cost Abroad page, the initial holistic consultation is listed as $50–$250 USD as a starting estimate for alternative medicine abroad — not as the ITC treatment price. ITC packages are $18,995 USD for the 3-week Out-Patient Program and $30,000 USD for the 3-week In-Patient Program. Please confirm the final price directly with the provider before booking.
>
> Sources: adenocarcinoma package page; ITC price list

**Verdict:** Pass — does not agree with a wrong price; corrects it, and disambiguates where $50 *does* appear ($50–$250 general consultation range, not an ITC price). This was caught in Argon review: my first draft wrongly said $50 appears nowhere in the pages.

---

## Extra checks run

- “How much does ITC treatment cost?” → $18,995 USD starting, with the base-package inclusions.
- “Who are the ITC doctors?” → Dr. Carlos Bautista (Medical Director), Dr. David Alvarez, Dr. Adolfo Carrillo, Dr. Pablo Orozco.
- “How do I get to Tijuana?” → San Diego International Airport (SAN), 25 minutes, free airport rides, shuttle / border-crossing support.
- “¿Cuánto cuesta el tratamiento de adenocarcinoma en Tijuana?” → answered in Spanish, same $18,995 / $30,000 USD figures.
- “How much does a dental implant cost in Mexico?” → “I don't know — that answer is not in the 7 PlacidWay pages” + free-quote pointer. Correct: dental implants are not in these pages.
- “What is included in the Out-Patient program?” → weekly labs, one imaging, core therapies, 2 meals daily, standard medications, 3-month follow-up.
