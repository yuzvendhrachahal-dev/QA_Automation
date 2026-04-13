def handle_add_to_cart_flow(page):
    try:
        # Wait for popup
        page.wait_for_selector("text=Keep Shopping", timeout=3000)

        # Click Keep Shopping
        page.get_by_text("Keep Shopping", exact=False).click()

        print("✔ Clicked Keep Shopping")

    except Exception:
        print("ℹ No popup appeared")