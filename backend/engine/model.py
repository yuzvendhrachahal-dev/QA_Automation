ELEMENT_MAP = {
    
    # USER NAME
    "username": """
        input[name*='UserName'],
        input[placeholder*='Username'],
        input[name*='email']
    """,

    "first name": """
        input.firstname,
        input[name*='txtFirstName'],
        input[name*='First Name'],
        input[placeholder*='First Name']
    """,
    
    "last name": """
        input[name*='txtLastName'],
        input[name*='Last Name'],
        input[placeholder*='Last Name']
    """,

    # USER LOGIN AND EMAIL
    "user login": """
        input[name*='User Login'],
        input[placeholder*='User Login'],
        input[name*='email']
    """,

    "email": """
        input[id='txtGuestFreeUser'],
        input[name='txtGuestFreeUser'],
        input[placeholder*='email'],
        input[name*='UserNameINR'],
        input[class*='regemail'],
        input[class*='email']
    """,
    
    "loginview2 login": "button#ctl00_placeholderMain_LoginView2_customerLogin_LoginButton",

    # PASSWORD SECTION
    "new password": "input[id*='txtNewPassword']",
    
    "password": """
        input#Password,
        input[name$='$Password'],
        input[id='ctl00_placeholderMain_LoginView1_defaultLogin_Password'],
        input[type='password']:not([id*='Confirm'])
    """,
    
    # SPECIFIC FOR THE REGERASTRATION FIELD PASSWORD - MYR/USD PAGE
    "reg password": """
        input#Password.regspaswd
    """,
    "login2 password": """
        input#ctl00_placeholderMain_LoginView2_customerLogin_Password
    """,

    "confirm password": """
        input[id*='ConfirmPassword'],
        input[placeholder*='Confirm Password']
    """,
    
    "search": "input[type='text']",

    "name": "input[placeholder*='Name'], input[name*='name']",

    
    # Register page mobile fallback
    "mobile number": "input[type='number'], input[placeholder*='Mobile']",
    "mobile": "input[type='number'], input[placeholder*='Mobile']",
    "phone": "input[type='number']",

    # ASP.NET register mobile field
    "number": "input[id*='txtPhoneNumber'], input[name*='txtPhoneNumber'], input[name*='txtMobile']",

    # OTP AND VERIFICATION
    "otp": "input[placeholder*='OTP'], input[name*='otp']",
    "verification code": "input[placeholder*='Verification Code'], input[name*='VerificationCode']",
    
    # SELECT COUNTRY IN THE REGISTER PAGE MYR/USD
    "country": "select.DropDownCountry, select#ddlCountry, select[id*='drpCountry']",

    # Close popup button

    "close": ".close-popup",

    # ───────────────── TEMPLE TABS ─────────────────

    "pooja":

        "a.pooja-tab",
    "abishekam":

        "a.abishekam-tab",
    "homa":

        "a.homa-tab",

    # address
    "address": "textarea[id*='txtStreet'], textarea[name*='txtStreet']",
    # postal
    "postal": "input[id*='txtPostalCode'], input[name*='txtPostalCode']",

    # Disclaimer in cart page 
    "disclaimer": "input[id*='ChkDisclaimerSCard']",
    "gdisclaimer": "input[id*='CheckRazorpay']",

    # Logo Targeting
    "logo": "div.av-logo-wrap a"
}



def parse_human_steps(steps, url):
    structured = []

    for raw in steps:
        raw = raw.strip()
        if not raw:
            continue

        step = raw.lower()

        if step.startswith("open"):
            structured.append({"action": "open", "raw": raw})

        elif step.startswith("home"):
            structured.append({"action": "home", "raw": raw})

        elif step.startswith("type"):
            try:
                after = raw[5:].strip()
                parts = after.split(" in ")
                value = parts[0].strip()
                field = parts[1].strip().lower()
            except:
                value = ""
                field = "search"

            structured.append({
                "action": "type",
                "target": ELEMENT_MAP.get(field, "input"),
                "value": value,
                "raw": raw
            })

        elif step.startswith("click checkbox"):
            structured.append({
                "action": "click_checkbox",
                "target": raw[len("Click checkbox"):].strip(),
                "raw": raw
            })

        elif step.startswith("click image"):
            structured.append({
                "action": "click_image",
                "target": raw[len("Click image"):].strip(),
                "raw": raw
            })

        elif step.startswith("click button"):
            structured.append({
                "action": "click_button",
                "target": raw[len("Click button"):].strip(),
                "raw": raw
            })

        elif step.startswith("click link"):
            structured.append({
                "action": "click_link",
                "target": raw[len("Click link"):].strip(),
                "raw": raw
            })

        elif step.startswith("click input"):
            structured.append({
                "action": "click_input",
                "target": raw[len("Click input"):].strip(),
                "raw": raw
            })

        elif step.startswith("click"):
            structured.append({
                "action": "click",
                "target": raw[len("Click"):].strip(),
                "raw": raw
            })

        elif step.startswith("verify"):
            structured.append({
                "action": "verify",
                "target": raw[len("Verify"):].strip(),
                "raw": raw
            })

        elif step.startswith("wait until"):
            text = step.replace("wait until", "").strip()

            if "page is loaded" in text:
                structured.append({"action": "wait_for_page", "raw": raw})

        elif step.startswith("wait"):
            try:
                secs = int(step.replace("wait", "").strip())
            except:
                secs = 2

            structured.append({
                "action": "wait",
                "value": secs,
                "raw": raw
            })

        elif step.startswith("press"):
            structured.append({
                "action": "press",
                "value": raw[len("Press"):].strip(),
                "raw": raw
            })

        elif step.startswith("hover"):
            structured.append({
                "action": "hover",
                "target": raw.replace("Hover", "").strip(),
                "raw": raw
            })

        elif step.startswith("validate event dates"):
            structured.append({
                "action": "validate_event_dates",
                "raw": raw
            })
        
        elif step.startswith("select date"):
            # "Select date 2026-03-27" → sets input[type=date]#datepicker
            value = raw[len("Select date"):].strip()
            structured.append({
                "action": "select_date",
                "value":  value,
                "raw":    raw
            })
 
        elif step.startswith("select time"):
            # "Select time 06:00 AM - 06:30 AM" → picks from #timeSlotsDropdown
            value = raw[len("Select time"):].strip()
            structured.append({
                "action": "select_time",
                "value":  value,
                "raw":    raw
            })
            
        elif step.startswith("select"):
            try:
                after = raw[7:].strip()
                parts = after.split(" in ")
                value = parts[0].strip()
                field = parts[1].strip().lower()
            except:
                value = ""
                field = ""

            # use autocomplete for state & city
            if field == "state":
                structured.append({
                    "action": "select_autocomplete",
                    "target": "input.state_input, input[id*='txtState']",
                    "value": value,
                    "raw": raw
                })
            elif field == "city":
                structured.append({
                    "action": "select_autocomplete",
                    "target": "input[id*='txtCity']",
                    "value": value,
                    "raw": raw
                })
            else:
                structured.append({
                    "action": "select",
                    "target": ELEMENT_MAP.get(field, "select"),
                    "value": value,
                    "raw": raw
                })


        else:
            raise ValueError(f"Unsupported step: {raw}")

    return structured

