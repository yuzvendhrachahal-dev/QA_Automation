from datetime import datetime
import time


def try_read(locator):
    try:
        return locator.inner_text(timeout=300).strip()
    except:
        return ""


def wait_for_all_dates(page, timeout=45):
    """
    Waits inside the browser until ALL JS-populated .dsk-date spans settle.

    AstroVed Monthly Powertimes: each card with a dynamic date fires its own
    independent async callMoonPhase() API call + setTimeout(1000ms).
    With up to 15 cards, the last API call can take 8-12 seconds.

    Timing settings:
      MIN_WAIT_MS   = 10000  → always wait 10s after first span (covers up to ~15 cards)
      STABLE_NEEDED = 8      → 8 x 400ms = 3.2s stable before exit
      MAX_WAIT_MS   = 40000  → hard timeout at 40s

    Special Events page: all dates are hardcoded HTML, so they populate
    instantly and the 10s min-wait still applies — adds a small delay but
    ensures correctness. Specials never has JS-populated dates so this is safe.
    """
    print("  Waiting for all JS dates to load (up to 15 cards)...")

    js_code = """
        async () => {
            return new Promise((resolve) => {
                let lastCount        = -1;
                let stableTicks      = 0;
                let firstPopulatedAt = null;
                const STABLE_NEEDED  = 8;       // 8 x 400ms = 3.2s stable
                const MIN_WAIT_MS    = 10000;   // wait at least 10s after first span
                const MAX_WAIT_MS    = 40000;   // hard timeout 40s
                const startTime      = Date.now();

                function check() {
                    const spans   = document.querySelectorAll('.dsk-date');
                    let populated = 0;
                    spans.forEach(s => { if (s.innerText.trim()) populated++; });

                    if (populated > 0 && firstPopulatedAt === null) {
                        firstPopulatedAt = Date.now();
                    }

                    const elapsed    = Date.now() - startTime;
                    const sinceFirst = firstPopulatedAt ? Date.now() - firstPopulatedAt : 0;

                    if (populated === lastCount && populated > 0) {
                        stableTicks++;
                    } else {
                        stableTicks = 0;
                    }
                    lastCount = populated;

                    // Exit: stable for enough ticks AND minimum wait passed
                    if (stableTicks >= STABLE_NEEDED && sinceFirst >= MIN_WAIT_MS) {
                        resolve(populated);
                        return;
                    }
                    // Hard timeout
                    if (elapsed >= MAX_WAIT_MS) {
                        resolve(populated);
                        return;
                    }
                    setTimeout(check, 400);
                }
                setTimeout(check, 400);
            });
        }
    """

    try:
        count = page.evaluate(js_code)
        print(f"  All JS dates loaded — {count} spans populated ✅")
    except Exception as e:
        print(f"  page.evaluate failed: {e} — sleeping 12s fallback")
        time.sleep(12)


def parse_event_date(date_text):
    """
    Handles 2 formats:
      FORMAT 1 — "Mar. 24, 2026 at 5:30 am IST"  → full datetime compare
      FORMAT 2 — "Apr. 5, 2026"                   → date-only compare
    """
    text = date_text.strip()
    if not text:
        return None, "empty"

    clean = text.replace("IST", "").replace("  ", " ").strip()

    if "at" in clean:
        try:
            return datetime.strptime(clean, "%b. %d, %Y at %I:%M %p"), "datetime"
        except ValueError:
            pass
        try:
            return datetime.strptime(clean.replace(".", ""), "%b %d, %Y at %I:%M %p"), "datetime"
        except ValueError:
            pass
    else:
        try:
            return datetime.strptime(clean, "%b. %d, %Y"), "date"
        except ValueError:
            pass
        try:
            return datetime.strptime(clean.replace(".", ""), "%b %d, %Y"), "date"
        except ValueError:
            pass

    return None, "parse_error"


def get_status(event_date, date_type, now):
    if date_type == "datetime":
        return "EXPIRED" if event_date < now else "UPCOMING"
    elif date_type == "date":
        if event_date.date() < now.date():
            return "EXPIRED"
        elif event_date.date() == now.date():
            return "TODAY"
        return "UPCOMING"
    return "UNKNOWN"


def validate_event_dates(page, run_dir):

    results = []
    print("Starting event validation...")
    print("Scanning event cards...")

    # Wait inside browser for ALL async JS dates to settle
    wait_for_all_dates(page, timeout=45)

    cards = page.locator(".listing-section")
    total = cards.count()
    print(f"Total cards found: {total}")

    now       = datetime.now()
    event_num = 0

    for i in range(total):
        card = cards.nth(i)
        try:
            try:
                title = card.locator("h2.dsk-spcl-head a").inner_text().strip()
            except:
                title = "Unknown Event"

            date_text = try_read(card.locator(".date-section .dsk-date"))

            if not date_text:
                print(f"  Card {i+1}: '{title[:50]}' — no date, skipping")
                continue

            event_num += 1
            print(f"Checking event {event_num}: {title}")
            print(f"  Raw date  : {date_text!r}")

            event_date, date_type = parse_event_date(date_text)

            if event_date is None:
                print(f"  ⚠ Parse failed ({date_type}): {date_text!r} — skipping")
                continue

            print(f"  Date type : {date_type}")
            print(f"  Parsed    : {event_date}")

            status = get_status(event_date, date_type, now)
            print(f"  Status    : {status}")

            screenshot_path = run_dir / f"event_{event_num}.png"
            card.screenshot(path=str(screenshot_path))

            results.append({
                "event":      event_num,
                "title":      title,
                "date":       date_text,
                "date_type":  date_type,
                "status":     status,
                "screenshot": str(screenshot_path),
            })

        except Exception as e:
            print(f"  Error on card {i+1}: {e}")

    print(f"Event validation completed — {len(results)} events validated")
    return results