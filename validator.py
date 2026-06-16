import pandas as pd
from datetime import datetime
from country_rules import COUNTRY_PHONE_RULES

VALID_PAYMENT_MODES = [
    "UPI",
    "CARD",
    "CASH",
    "NETBANKING"
]


def validate_data(df):

    errors = []
    valid_rows = []

    for index, row in df.iterrows():

        row_errors = []

        # Missing values
        if row.isnull().any():
            row_errors.append("Missing Value")

        # Phone validation
        try:

            phone = str(row["phone"]).strip()
            country = str(row["country"]).strip()

            if country in COUNTRY_PHONE_RULES:

                required_length = COUNTRY_PHONE_RULES[country]

                if not phone.isdigit():
                    row_errors.append("Invalid Phone")

                elif len(phone) != required_length:
                    row_errors.append("Invalid Phone")

        except:
            row_errors.append("Invalid Phone")

        # Payment validation
        try:

            payment_mode = str(row["payment_mode"]).strip()

            if payment_mode not in VALID_PAYMENT_MODES:
                row_errors.append("Invalid Payment Mode")

        except:
            row_errors.append("Invalid Payment Mode")

        # Date validation
        try:

            datetime.strptime(
                str(row["date"]),
                "%Y-%m-%d"
            )

        except:
            row_errors.append("Invalid Date")

        if row_errors:

            errors.append({
                "row_number": index + 1,
                "errors": ", ".join(row_errors)
            })

        else:

            valid_rows.append(index)

    clean_df = df.iloc[valid_rows]

    error_df = pd.DataFrame(errors)

    return clean_df, error_df