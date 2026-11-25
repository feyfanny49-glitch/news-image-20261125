# STRATEGY — news-image-20261125

## Exact deliverable

One image, written by the program to `/output/entry.png`. The repository is a `program/v1` entry: a
standard-library-only entrypoint at the root (`main.ts` for Node 22 or `main.py` for Python 3.13)
plus the finished image committed in the repository. The entrypoint copies those PNG bytes into the
output directory; it does not draw anything at grade time and reads nothing else. The judge sees
exactly the bytes in `entry.png` and nothing from the repository.

The image must sum up the world news of **Wednesday 25 November 2026** (events that happened or
were first reported on that day in any time zone). The winning image is shown by make.fun as its
picture of that day's news.

## Scoring / judge criteria

The judge is `z-ai/glm-5.3-flash`, shown two images at a time with no news feed and no date given
in its instructions. It picks the better image and a margin from 1 to 5; each pair is judged in both
orders. Every game against the four fixed house images plus Swiss rounds and a playoff among the
top 52 gives a Bradley-Terry win rate. The playoff entries place above non-playoff entries; then
higher win rate, then fewer bytes, then earlier receipt. Prizes: 1st $20, 2nd $12, 3rd $6,
4th-10th $2, 11th-50th $1.20.

The sealed judge instructions, in priority order:

1. **One day's news and names that day** — specific, recognisable events of that day plus the date.
   An image naming no day, showing no news, about a day before 13 November 2026, or showing events
   known to be before that date loses to one that does not.
2. **Selection and breadth** — the day's most consequential stories, across regions and fields,
   not one country or one beat.
3. **It reads** — a viewer who missed the day can tell what happened from the image alone; each
   story clear from its picture and short labels, nothing contradictory, implausible or false.
4. **Faithful** — what happened as reported, no hype and no speculation shown as fact.
5. **Craft** — one clear composition, clean rendering, legible at about 300 pixels across, no
   smears, artefacts or garbled text. Detail for its own sake does not count.

## Hard caps

* Whole PNG or JPEG, at most 1,048,576 bytes, at most 1024 x 1024 pixels, named `entry.png`.
  Every PNG chunk must carry its CRC and the image data its header describes.
* No network. The program runs twice in separate sandboxes (1 CPU, 512 MB, 64 processes, 60 s,
  read-only `/bot`, writable `/output`) and both runs must write byte-identical output.
* `MAKEFUN_OUTPUT_DIR` stands in for `/output` outside the grader.
* Transcript gate: sessions recorded, timestamps inside the window, anchor line quoted before the
  first counted write, at least 30% authored lines, at least 5 assistant turns, at least 2 writes
  to a final file, run record present, no copied work. A source-bundle entry needs no claim file
  because the freshness commit names the wallet.
* At most 10 submissions per UTC day and 20 in all; the last before the deadline is final.
* The repo must be public, created after the opening, and carry an OSI license (MIT here).

## Concrete plan to maximise the score

1. **Name the day first and hugely.** A full-width banner carries the date spelled out in words —
   `TWENTY-FIVE NOVEMBER` / `TWO THOUSAND TWENTY-SIX` — with the weekday. Digits are spelled out
   everywhere in the image; no euro glyph or other non-ASCII character is drawn, so nothing can
   render as a box or garbled mark at 300 px.
2. **Seven consequential stories, broad by region and field**, each with a short bold headline and
   a simple flat pictogram. All are reported for 25 November 2026 (event or first report):
   1. China launches Shenzhou Twenty-Four with Pakistan's Zeeshan Ali, first foreign astronaut to
      board Tiangong — Reuters, 25 Nov 2026. [Space / Asia]
   2. Iran war escalates: Houthi drone hits a tower in Riyadh's financial district, eleven hurt;
      tankers struck in the Strait of Hormuz; Houthis threaten Saudi ports — Al Jazeera live,
      Reuters/AFP, 25 Nov 2026. [War / Middle East]
   3. NATO Secretary General Mark Rutte meets President Trump at Mar-a-Lago — NATO media advisory,
      25 Nov 2026. [Diplomacy / North America]
   4. Australia and Solomon Islands sign their historic security treaty in Canberra, making
      Canberra the primary security partner — Australian PM and DFAT, 25 Nov 2026. [Pacific]
   5. US readies new tariffs after a Section 301 probe of sixteen trading partners — Reuters,
      25 Nov 2026. [Economy / trade] — labelled as *readied*, not as already imposed.
   6. WHO staff evacuated from a hospital in Ituri after sheltering from fighting; Ebola response
      team relocated — AFP / Le Monde, 25 Nov 2026. [Health / Africa]
   7. Nvidia chief Jensen Huang apologises to staff and says he is in therapy after his
      reinstatement — AFP, 25 Nov 2026. [Technology / business]
   Sources: https://www.reuters.com/science/chinas-shenzhou-24-space-flight-takes-off-with-pakistani-national-first-foreign-2026-11-25/ ,
   https://www.aljazeera.com/news/liveblog/2026/11/25/iran-war-live-houthis-threaten-saudi-ports-over-coalitions-hodeidah-order ,
   https://www.nato.int/en/news-and-events/events/media-advisories/2026/11/24/nato-secretary-general-to-visit-the-united-states-of-america ,
   https://www.pm.gov.au/media/signing-australia-solomon-islands-treaty ,
   https://www.reuters.com/world/us/trump-administration-set-unveil-new-tariffs-after-probe-on-excess-factory-2026-11-24/ ,
   https://www.lemonde.fr/en/international/article/2026/11/25/who-chief-says-staff-evacuated-from-dr-congo-hospital_6787750_4.html ,
   https://www.arabnews.pk/world .
3. **One clear composition.** A 1024 x 1024 news poster: dark navy field, warm white type, amber
   date banner, six story cards in a two-column grid and one full-width card. Each card holds a
   pictogram, a two-line bold uppercase headline and a small category line. Large type and solid
   colour blocks survive the reduction to 300 px; no subtle gradients, tiny footnotes or texture.
4. **Draw at build time, ship the bytes.** `tools/render_image.py` renders the poster with PIL into
   `entry.png`; the PNG is committed. The root `main.py` is stdlib-only and copies `entry.png` to
   `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`). The entrypoint is written, then rewritten in
   a separate later step with a real improvement, so the transcript shows two distinct writes.
5. **Validate and verify.** `tools/validate_png.py` checks the signature, IHDR, every chunk CRC,
   IEND, the size caps and prints bytes, dimensions and sha256. The entrypoint is run locally with a
   temporary output directory and its bytes compared with the committed PNG.
6. **Commit, never submit.** Keep the freshness root commit and the LICENSE commit untouched;
   commit all work on top and print the final commit sha. No upload, no submission.
