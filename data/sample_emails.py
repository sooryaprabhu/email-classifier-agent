# Sample emails to test our classifier
# These are fake emails simulating an energy company's inbox

SAMPLE_EMAILS = [
    {
        "id": "001",
        "from": "john.smith@email.com",
        "subject": "Wrong bill amount",
        "body": "Hi, I received my bill this month and I was charged £150 but I should only be paying £89 based on my contract. Can you please look into this and correct it? This is the third time this has happened."
    },
    {
        "id": "002", 
        "from": "sarah.jones@email.com",
        "subject": "Meter reading question",
        "body": "Hello, I submitted my meter reading last week but I haven't received any confirmation. My meter reading was 45623. Could you please confirm you have received this and update my account?"
    },
    {
        "id": "003",
        "from": "mike.brown@email.com", 
        "subject": "Top up not working",
        "body": "I topped up my prepayment meter with £20 yesterday using the app but the credit hasn't appeared on my meter. I am running very low on credit and need this resolved urgently please."
    },
    {
        "id": "004",
        "from": "emma.wilson@email.com",
        "subject": "Moving house next month",
        "body": "I am moving to a new address on 15th November. My current address is 42 Oak Street and my new address will be 8 Maple Avenue. Could you please arrange to transfer my account or let me know what I need to do?"
    },
    {
        "id": "005",
        "from": "david.taylor@email.com",
        "subject": "Power cut in my area",
        "body": "We have had no electricity since 6am this morning. My neighbours are also affected. Is there a known outage in the NG7 postcode area? When will power be restored? I have food in my fridge that is at risk."
    },
    {
        "id": "006",
        "from": "lisa.martin@email.com",
        "subject": "Want to switch to green energy",
        "body": "I am interested in switching to a renewable energy tariff. Could you please send me information about your green energy options and what the costs would be compared to my current plan?"
    },
    {
        "id": "007",
        "from": "james.white@email.com",
        "subject": "Direct debit cancelled by mistake",
        "body": "I accidentally cancelled my direct debit last week. I would like to set it up again. My account number is GB29NWBK60161331926819. Could you help me reinstate this please?"
    },
    {
        "id": "008",
        "from": "claire.davis@email.com",
        "subject": "Smart meter installation",
        "body": "I would like to book an appointment to have a smart meter installed. I am available on weekdays after 2pm or any time on weekends. Please let me know the next available slot."
    }
]

# Categories used for classification
CATEGORIES = [
    "Billing",
    "Metering", 
    "Prepayment",
    "Account Management",
    "Power Outage",
    "Tariff Enquiry",
    "Payment",
    "Smart Meter"
]
