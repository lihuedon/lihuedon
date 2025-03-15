from os import system, name
import matplotlib.pyplot as plt

import locale


class Loan:
    """A class for calculating the payment for a fixed rate loan."""

    def __init__(self):
        """Initialize the Loan class."""
        self.locale = locale.setlocale(locale.LC_ALL, '')

    def print_header(self):
        """Print the purpose of the class and let user know the formula."""
        header = "\nCalculate Payment for fixed Rate loan\n"
        header += "\n        r(PV)"
        header += "\nP = ________________"
        header += "\n      1-(1+r)^-n\n"
        header += "\nP = Payment"
        header += "\nPV = Present Value"
        header += "\nr = rate per period"
        header += "\nn = number of periods\n"
        return header

    def calculate_payment(self, PV, r, n):
        """Calculate the payment amount and return float value."""
        if 0 == r:
            return PV / n
        else:
            return (r * .01 / 12) * (PV) / (1 - (1 + r * .01 / 12) ** -n)

    def present_payment(self, P, PV, r, n):
        """Take input values and format the summary."""
        display = ""
        display += f"\nPresent Value = {locale.currency(PV, grouping=True)}\n"
        display += f"rate per period = {r}%\n"
        display += f"number of periods = {n} months\n"
        display += f"\nYour payment will be {locale.currency(P, grouping=True)}\n"
        display += f"\nTotal of payments {locale.currency(P * n, grouping=True)}\n"
        display += f"Cost of credit {locale.currency(P * n - PV, grouping=True)}\n"

        return display

    def prepare_plot_title(self, P, PV, r, n):
        """Take input values and format the title."""
        title = f"Loan amount = {locale.currency(PV, grouping=True)}, "
        title += f"Rate = {r}%, "
        title += f"Length of loan = {n} months"
        title += f"\nMonthly payment = {locale.currency(P, grouping=True)}"
        title += f"\nTotal of payments = {locale.currency(P * n, grouping=True)}"
        title += f"\nCost of credit = {locale.currency(P * n - PV, grouping=True)}"
        return title

    def plot_loan(self, P, PV, r, n):
        """Take loan data and graph amortization, payment, interest, and principle."""
        principle = PV
        rate = r * .01
        num_payments = n
        monthly_payment = P

        x_payment_numbers = []
        y_monthly_payments = []
        y_interest_values = []
        y_principle_values = []

        for payment_no in range(1, num_payments + 1):
            x_payment_numbers.append(payment_no)
            y_monthly_payments.append(monthly_payment)
            int_pmt = principle * rate / 12
            y_interest_values.append(int_pmt)
            princ_pmt = monthly_payment - int_pmt
            y_principle_values.append(princ_pmt)
            principle -= princ_pmt

        plt.style.use('fivethirtyeight')

        fig, ax = plt.subplots(figsize=(15, 9))
        ax.plot(x_payment_numbers, y_principle_values, linewidth=3, color='yellow')
        ax.plot(x_payment_numbers, y_interest_values, linewidth=3, color='cyan')
        ax.plot(x_payment_numbers, y_monthly_payments, linewidth=1, color='magenta')

        # Set chart title and label axes
        ax.set_title(f"{self.prepare_plot_title(P, PV, r, n)}", fontsize=14)
        ax.set_xlabel("Number of Payments", fontsize=14)
        ax.set_ylabel("Principle and Interest", fontsize=14)

        # Set size of tick labels.
        ax.tick_params(axis='both', labelsize=14)

        plt.show()


    def clear(self):
        """Clear screen to start a new calculation."""
        # for windows
        if name == 'nt':
            system('cls')

            # for mac and linux(here, os.name is 'posix')
        else:
            system('clear')
