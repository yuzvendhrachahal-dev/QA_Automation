import uuid
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

from backend.engine.model import ELEMENT_MAP
from backend.engine.event_validator import validate_event_dates

BASE_STORAGE = Path("storage/runs")
BASE_STORAGE.mkdir(parents=True, exist_ok=True)


def handle_astroved_popup(page):
    """Called ONLY after navigation (open/home) — not on every step."""
    try:
        page.get_by_text("NO", exact=False).click(timeout=1500)
    except:
        pass


def reliable_type(page, selector, value):
    locator = page.locator(selector).first
    locator.wait_for(state="visible", timeout=20000)
    locator.scroll_into_view_if_needed()

    locator.click(force=True)
    page.wait_for_timeout(200)

    locator.fill("")
    locator.fill(value)

def set_date_input(page, selector, value):
    """
    Sets a date input (YYYY-MM-DD format).
    Chrome date input has 3 segments MM/DD/YYYY.
    Clicks left edge to land on MM, types MMDDYYYY as stream.
    Falls back to JS if keyboard method fails.
    """
    parts = value.split("-")
    yyyy, mm, dd = parts[0], parts[1], parts[2]
 
    date_input = page.locator(selector)
    date_input.wait_for(state="visible", timeout=10000)
    date_input.scroll_into_view_if_needed()
 
    # Click very left edge to land on MM segment
    box = date_input.bounding_box()
    page.mouse.click(box["x"] + 5, box["y"] + box["height"] / 2)
    page.wait_for_timeout(200)
 
    # Type MMDDYYYY — Chrome auto-advances between segments
    page.keyboard.type(mm + dd + yyyy)
    page.wait_for_timeout(300)
 
    # Check if set correctly
    actual = date_input.input_value()
    if actual != value:
        print(f"  Keyboard failed ({actual}), using JS fallback...")
        page.evaluate(f"() => {{ const el = document.querySelector('{selector}'); if(el) el.value = '{value}'; }}")
        page.wait_for_timeout(200)
 
    # Fire change event to trigger slot loading
    date_input.dispatch_event("change")
    page.wait_for_timeout(300)
    print(f"  Date set to: {date_input.input_value()}")

def run_test(url, steps, test_name):

    results = []
    run_id  = str(uuid.uuid4())[:8]
    run_dir = BASE_STORAGE / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        context = browser.new_context(permissions=[])
        page    = context.new_page()
        page.set_default_timeout(60000)

        for i, step in enumerate(steps, start=1):

            print("Executing step:", step["raw"])
            screenshot_path = run_dir / f"step_{i}.png"

            try:

                action = step["action"]
                target = step.get("target")
                value  = step.get("value")

                # ── OPEN URL ──────────────────────────────────────────────
                if action == "open":
                    page.goto(url)
                    page.wait_for_load_state("networkidle")
                    handle_astroved_popup(page)

                # ── HOME ──────────────────────────────────────────────────
                elif action == "home":
                    page.goto("https://www.astroved.com")
                    page.wait_for_load_state("networkidle")
                    handle_astroved_popup(page)

                # ── CLICK ─────────────────────────────────────────────────
                elif action == "click":
                    if target in ELEMENT_MAP:
                        locator = page.locator(ELEMENT_MAP[target]).first
                    else:
                        locator = page.locator(f"text={target}").first

                    locator.wait_for(state="attached", timeout=60000)

                    try:
                        locator.scroll_into_view_if_needed()
                    except:
                        pass

                    # click immediately (like old executor)
                    locator.click(force=True)

                    page.wait_for_timeout(200)

                # ── CLICK BUTTON ──────────────────────────────────────────
                elif action == "click_button":
                    if target in ELEMENT_MAP:
                        locator = page.locator(ELEMENT_MAP[target])
                        locator.first.wait_for(state="visible", timeout=45000)
                        locator.first.click()
                    else:
                        locator = page.get_by_role("button", name=target)
                        locator.first.wait_for(state="visible", timeout=45000)
                        locator.first.click()

                # ── CLICK LINK ────────────────────────────────────────────
                elif action == "click_link":
                    page.get_by_role("link", name=target).click()
                    page.wait_for_timeout(400)

                # ── CLICK INPUT ───────────────────────────────────────────
                elif action == "click_input":
                    page.locator(f"input[value='{target}']").click()
                    page.wait_for_timeout(300)

                # ── CLICK CHECKBOX ────────────────────────────────────────
                elif action == "click_checkbox":
                    if target in ELEMENT_MAP:
                        locator = page.locator(ELEMENT_MAP[target]).first
                    else:
                        locator = page.locator(
                            f"input[type='checkbox'][name*='{target}'], input[type='checkbox'][id*='{target}']"
                        ).first

                    locator.click(force=True)

                    page.wait_for_timeout(300)

                # ── CLICK IMAGE ───────────────────────────────────────────
                elif action == "click_image":
                    image = page.get_by_role("img", name=target).first
                    image.wait_for(state="visible")
                    image.click()
                    page.wait_for_timeout(400)

                # ── TYPE ──────────────────────────────────────────────────
                elif action == "type":
                    reliable_type(page, target, value)

                # ── VERIFY ────────────────────────────────────────────────
                elif action == "verify":
                    page.get_by_text(target, exact=False).first.wait_for()

                # ── WAIT ──────────────────────────────────────────────────
                elif action == "wait":
                    time.sleep(value)

                elif action == "wait_for_page":
                    page.wait_for_load_state("networkidle")

                elif action == "wait_visible":
                    page.get_by_text(target, exact=False).first.wait_for(state="visible")

                elif action == "wait_clickable":
                    locator = page.get_by_text(target, exact=False).first
                    locator.wait_for(state="visible")
                    locator.is_enabled()

                elif action == "wait_text":
                    page.get_by_text(target, exact=False).first.wait_for()

                # ── PRESS KEY ─────────────────────────────────────────────
                elif action == "press":
                    page.keyboard.press(value)

                # ── HOVER ─────────────────────────────────────────────────
                elif action == "hover":
                    locator = page.get_by_text(target, exact=False).first
                    locator.wait_for(state="visible")
                    locator.hover()

                # ── SELECT DROPDOWN ───────────────────────────────────────
                elif action == "select":
                    dropdown = page.locator(target).first
                    dropdown.wait_for(state="visible")
                    dropdown.select_option(label=value)
                    dropdown.dispatch_event("change")
                    page.wait_for_timeout(800)

                # ── SELECT AUTOCOMPLETE ───────────────────────────────────
                elif action == "select_autocomplete":
                    field = page.locator(target).first
                    field.wait_for(state="visible", timeout=10000)
                    field.scroll_into_view_if_needed()
                    field.click()
                    field.fill("")
                    field.press_sequentially(value, delay=80)

                    try:
                        page.wait_for_selector(".ui-autocomplete .ui-menu-item", timeout=5000)
                    except:
                        page.wait_for_timeout(2000)

                    page.keyboard.press("ArrowDown")
                    page.wait_for_timeout(300)
                    page.keyboard.press("Enter")
                    page.wait_for_timeout(500)

                 # ── SELECT DATE

                # ── SELECT DATE ───────────────────────────────────────────
                # "Select date 2026-03-27"
                # Uses id="datepicker", fires change to load time slots
                elif action == "select_date":
                    set_date_input(page, "#datepicker", value)
 
                # ── SELECT TIME ───────────────────────────────────────────
                # "Select time 06:00 AM - 06:30 AM"
                # Waits for #timeSlotsDropdown to load then selects by label
                elif action == "select_time":
                    page.wait_for_function(
                        "() => { const s = document.getElementById('timeSlotsDropdown'); return s && s.options.length > 1; }",
                        timeout=15000
                    )
                    page.locator("#timeSlotsDropdown").select_option(label=value)
                    print(f"  Time set to: {value}")

                

                # ── HANDLE POPUP ────────────────────────────
                elif action == "handle_popup":
                    handle_astroved_popup(page)

                # ── EVENT VALIDATION ────────────────────────
                elif action == "validate_event_dates":
                    events = validate_event_dates(page, run_dir)

                    page.screenshot(path=str(screenshot_path))

                    results.append({
                        "stepNumber":  i,
                        "description": step["raw"],
                        "status":      "PASSED",
                        "screenshot":  f"storage/runs/{run_id}/step_{i}.png",
                        "events":      events,
                    })
                    continue

                # ── NORMAL SCREENSHOT ───────────────────────
                page.screenshot(path=str(screenshot_path))
                results.append({
                    "stepNumber":  i,
                    "description": step["raw"],
                    "status":      "PASSED",
                    "screenshot":  f"storage/runs/{run_id}/step_{i}.png",
                    "events":      [],
                })

            except Exception as e:
                page.screenshot(path=str(screenshot_path))
                results.append({
                    "stepNumber":  i,
                    "description": step["raw"],
                    "status":      "FAILED",
                    "error":       str(e),
                    "screenshot":  f"storage/runs/{run_id}/step_{i}.png",
                    "events":      [],
                })

        browser.close()

    return {
        "testName": test_name,
        "runId":    run_id,
        "status":   "PASSED" if all(r["status"] == "PASSED" for r in results) else "FAILED",
        "steps":    results,
    }