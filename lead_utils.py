import re


def clean_company_name(company_name):
    """Clean and standardise company name."""

    if not company_name:
        return ""

    company_name = company_name.strip()

    company_name = re.sub(
        r"\s+",
        " ",
        company_name
    )

    return company_name


def clean_location(location):
    """Clean and standardise location."""

    if not location:
        return ""

    return re.sub(
        r"\s+",
        " ",
        location.strip()
    )


def validate_website(website):
    """Check whether a website looks valid."""

    if not website:
        return True

    pattern = r"^(https?://)?(www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}.*$"

    return bool(
        re.match(
            pattern,
            website.strip()
        )
    )


def validate_revenue(revenue):
    """Check whether revenue is a valid positive number."""

    try:
        revenue = float(revenue)

        return revenue >= 0

    except (ValueError, TypeError):
        return False


def standardise_website(website):
    """Add https:// if it is missing."""

    if not website:
        return ""

    website = website.strip()

    if not website.startswith(
        ("http://", "https://")
    ):
        website = "https://" + website

    return website


def validate_lead(lead):
    """Validate the important fields of a lead."""

    errors = []

    company_name = lead.get(
        "company_name",
        ""
    ).strip()

    website = lead.get(
        "website",
        ""
    ).strip()

    revenue = lead.get(
        "annual_revenue",
        0
    )

    if not company_name:
        errors.append(
            "Company name is required."
        )

    if website and not validate_website(
        website
    ):
        errors.append(
            "Please enter a valid website."
        )

    if not validate_revenue(
        revenue
    ):
        errors.append(
            "Annual revenue must be a valid positive number."
        )

    return errors


def prepare_lead(lead):
    """Clean and standardise lead information."""

    cleaned_lead = lead.copy()

    cleaned_lead["company_name"] = clean_company_name(
        cleaned_lead.get(
            "company_name",
            ""
        )
    )

    cleaned_lead["location"] = clean_location(
        cleaned_lead.get(
            "location",
            ""
        )
    )

    cleaned_lead["website"] = standardise_website(
        cleaned_lead.get(
            "website",
            ""
        )
    )

    try:
        cleaned_lead["annual_revenue"] = float(
            cleaned_lead.get(
                "annual_revenue",
                0
            )
        )
    except (ValueError, TypeError):
        cleaned_lead["annual_revenue"] = 0

    return cleaned_lead