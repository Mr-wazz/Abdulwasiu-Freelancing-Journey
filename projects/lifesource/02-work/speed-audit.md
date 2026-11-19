# Speed and Conversion Audit: LifeSource (lifesource.earth)

Date: 16 Nov 2026. Currency: USD.
Tools: Google Lighthouse 12 (mobile and desktop), Playwright browser checks, manual phone screenshots.
Note: Lighthouse simulates a mid range phone on slow 4G from a cloud server. Real visitor numbers can differ. Google's real user data (PageSpeed Insights) was rate limited from here: check it by hand at https://pagespeed.web.dev/?url=https://lifesource.earth

## The business in one line
Green funeral home in Los Angeles (terramation, aquamation, natural burial, burial at sea). Serves LA, Ventura, Orange, San Bernardino and Riverside counties.
Site built on Duda (white label, so likely made by an agency). Obituaries and pre planning forms run on Gather (funeral software).

## What one lost visitor costs them (from their own public price list, Oct 2026)
| Package | Price |
|---|---|
| Terramation | $6,750 |
| Direct Aquamation + Parting Stone | $5,745 |
| Burial at Sea with guests | $5,395 |
| Direct Aquamation | $3,750 |
| Natural Burial | $2,750 |
| Direct Cremation | $1,295 |

One family that leaves the site and calls another funeral home = $1,300 to $6,750 lost. Add ons (memorial trees, Parting Stone, celebrations) push it higher.

## Scores
| Page | Mobile speed | Desktop speed | SEO | Main problem |
|---|---|---|---|---|
| Home | 78 to 79 | 98 | 85 | Scripts freeze the phone for 0.9s |
| Plan Ahead | **51** | | 92 | Page jumps while loading (layout shift 0.33, Google calls 0.25+ "poor") |
| Obituaries | **56** | | 92 | Main content shows after 7.2s |
| Contact | 77 | | 92 | Scripts block the phone |
| Terramation | 73 | | 92 | Main content 3.2s |
| Packages | 72 | | 92 | Main content 3.4s |
| Aquamation | 76 | | 92 | Main content 2.8s |

Good news (say this to the client first): server is very fast (50 to 80 ms), desktop scores 98, homepage text shows in 1.8s, no console errors, no sideways scroll on phones, HTTPS works.

## Findings, ranked by money

### 1. Dead "Schedule a Consultation" button on the homepage (CRITICAL, 5 min fix)
In the "Process" section, the orange SCHEDULE A CONSULTATION button links to `/`, the homepage itself. Click it and nothing happens, the page just reloads. This is the button right under "available 24/7 to answer your questions".
Fix: in Duda, point the button to `/contact-us` (or better, an online booking calendar, see 9).

### 2. No call button in the phone header (HIGH)
On a phone the header shows only the logo and the menu. The phone number (213.395.0034) is buried in the menu and the footer. Families with an immediate need are stressed and on their phones. They should be able to call in one tap, on every page.
Fix: add a sticky "Call 24/7" button to the mobile header.

### 3. Plan Ahead page jumps while loading (HIGH, mobile score 51)
A text block moves down while the page loads (layout shift 0.33). People tap the wrong thing or lose their place. Pre planning is the most valuable lead they get (paid in advance, often years before need).
Fix: give the embedded Gather form a fixed height so content does not jump. Lazy load the form.

### 4. Obituaries page is slow (HIGH, mobile score 56, main content at 7.2s)
Obituaries are usually the most visited pages of a funeral home site: families share the link with everyone. Each visitor is a future customer who has never heard of green funerals.
Fix: lighter obituary listing, compressed photos, load the Gather widget after the main content.

### 5. Third party scripts freeze the phone (MEDIUM)
These block the phone's processor for about 0.9s, and the page is not fully usable until about 12.6s in the test:
| Script | Blocking time |
|---|---|
| Klaviyo (email popups) | 400 ms |
| Google Tag Manager / Analytics | 270 ms |
| Duda runtime | 140 ms |
| Elfsight (widget) | 130 ms |
Also 423 KB of JavaScript is downloaded but never used.
Fix: delay Klaviyo and Elfsight until the visitor scrolls or after 3s. Remove any tag or widget not used.

### 6. Heavy images (MEDIUM)
| Image | Size | Problem |
|---|---|---|
| mountain-ridge.jpg | 300 KB | Below the fold but loads straight away |
| fallen-log.jpg | 233 KB | Old JPG format |
| terramation-texture.jpg | 189 KB | Old JPG format |
Saving: about 300 KB per visit on the homepage. Fix: WebP format, lazy loading, correct sizes.

### 7. SEO problems that stop Google sending visitors (MEDIUM)
- robots.txt lists the sitemap as `/sitemap.xml` (relative). Google needs the full address `https://lifesource.earth/sitemap.xml`. Lighthouse marks this as 2 errors.
- Homepage has 2 H1 headings. Should be 1.
- 9 images have no alt text (Google cannot read them, screen readers neither).
- Some text has low color contrast. Logo link has no name.

### 8. Headline is hard to read on phones (LOW, design)
Floating photo tiles sit on top of words in the main headline ("Plan a", "your", "planet"). See `test-report/mobile-hero-headline.png`.
Fix: move tiles out of the text area on mobile.

### 9. No way to book or chat outside office hours (BIGGEST GROWTH GAP, not a speed issue)
- "Schedule a consultation" sends people to a plain contact form. No calendar to pick a time.
- No live chat or text option. The site says "available 24/7" but at 2 am the only options are a phone call or a form.
- No automatic follow up seen after a form is sent (cannot confirm from outside).
Fix: online booking calendar, missed call text back, instant reply to every form, pre planning follow up emails and texts. This is GHL work and where the real money is.

### 10. Check by hand
- Facebook link (facebook.com/lifesource.earth) returned error 400 to our checker. Facebook often blocks bots, so open it in a normal browser to confirm.
- Submit the contact form once and time the reply.

## Files
- `test-report/report.md`: automatic site test (9 of 13 checks passed)
- `test-report/desktop.png`, `test-report/mobile.png`: full page screenshots
- `test-report/mobile-hero-headline.png`: headline covered by tiles
- `test-report/mobile-plan-ahead.png`: Plan Ahead page on a phone
