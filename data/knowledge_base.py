# Knowledge base articles for the energy company
# These simulate the 500 articles the RAG system searches through

KNOWLEDGE_BASE = [
    {
        "id": "KB001",
        "category": "Billing",
        "title": "How to dispute a bill",
        "content": """If you believe your bill is incorrect, please follow these steps:
        1. Check your meter reading matches what is on your bill
        2. Review your contract to confirm your agreed rate
        3. Contact us with your account number and the incorrect amount
        4. We will investigate within 5 working days
        5. If an error is found, a credit will be applied to your next bill
        Our billing team is available Monday to Friday 9am to 5pm."""
    },
    {
        "id": "KB002",
        "category": "Billing", 
        "title": "Understanding your energy bill",
        "content": """Your energy bill includes:
        - Unit rate: the cost per kWh of energy used
        - Standing charge: a daily charge for being connected to the grid
        - VAT: charged at 5% on domestic energy
        - Any outstanding balance from previous bills
        Bills are generated monthly based on actual or estimated readings.
        If you have a smart meter, readings are automatic."""
    },
    {
        "id": "KB003",
        "category": "Metering",
        "title": "How to submit a meter reading",
        "content": """You can submit your meter reading in several ways:
        1. Through our app - log in and select 'Submit Reading'
        2. On our website at myaccount.energy.com
        3. By calling our automated line on 0800 123 456
        4. By texting READING followed by your meter number to 12345
        Please submit readings on or before your bill date for accurate billing.
        Confirmation is sent by email within 24 hours."""
    },
    {
        "id": "KB004",
        "category": "Prepayment",
        "title": "Prepayment meter top up issues",
        "content": """If your top up has not appeared on your meter:
        1. Wait up to 2 hours as there can be a delay
        2. Check the app or website to confirm payment was successful
        3. Try pressing the blue button on your meter to refresh
        4. If still not showing after 2 hours, contact us urgently
        5. We can issue an emergency credit while we investigate
        Emergency credit of £5 is available if you are at risk of running out."""
    },
    {
        "id": "KB005",
        "category": "Account Management",
        "title": "Moving house - what to do",
        "content": """When moving home, please notify us at least 2 weeks in advance:
        1. Log in to your account and select 'I am moving'
        2. Enter your new address and moving date
        3. Take a final meter reading on moving day
        4. We will close your old account and open a new one
        5. Any credit balance will be refunded within 10 working days
        If moving within our supply area, your tariff can be transferred."""
    },
    {
        "id": "KB006",
        "category": "Power Outage",
        "title": "What to do during a power cut",
        "content": """If you experience a power cut:
        1. Check if your neighbours are also affected
        2. Visit powercut105.com or call 105 to report and get updates
        3. Check our website for known outages in your area
        4. Do not contact your energy supplier - outages are managed by network operators
        5. Keep fridge and freezer doors closed to preserve food
        Food compensation may be available for outages over 12 hours."""
    },
    {
        "id": "KB007",
        "category": "Tariff Enquiry",
        "title": "Green energy tariffs",
        "content": """Our green energy tariffs include:
        - Green Fixed 12: 100% renewable electricity, fixed for 12 months
        - Green Flex: 100% renewable, variable rate, no exit fees
        - EV tariff: cheaper overnight rates for electric vehicle charging
        All green tariffs are backed by Renewable Energy Guarantee of Origin certificates.
        Switch online in minutes with no interruption to your supply.
        Current green tariff unit rate: 24.5p per kWh"""
    },
    {
        "id": "KB008",
        "category": "Payment",
        "title": "Setting up or reinstating direct debit",
        "content": """To set up a direct debit:
        1. Log in to your online account
        2. Go to Payment Settings
        3. Select Set up Direct Debit
        4. Enter your bank account number and sort code
        5. Choose your preferred payment date
        Direct debits take 3 working days to activate.
        You will receive confirmation by email.
        Minimum direct debit amount is £10 per month."""
    },
    {
        "id": "KB009",
        "category": "Smart Meter",
        "title": "Smart meter installation",
        "content": """Smart meter installation is free and takes around 1-2 hours:
        1. Book online at smartmeter.energy.com
        2. Choose a date and time slot that suits you
        3. An engineer will attend and replace your existing meter
        4. You will receive a in-home display showing real-time usage
        Available slots: weekdays 8am-1pm or 1pm-6pm, Saturdays 8am-1pm.
        Please ensure an adult is home during the appointment."""
    }
]
