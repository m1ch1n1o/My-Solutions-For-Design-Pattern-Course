from DAO_files.items_DAO import ItemDatabaseProtocol
from DAO_files.revenue_DAO import RevenueDatabaseProtocol
from DAO_files.sales_DAO import SalesDatabaseProtocol
from models.cashier import Cashier
from models.customer import RandomCustomer


class Store:
    def __init__(
        self,
        items_db: ItemDatabaseProtocol,
        sales_db: SalesDatabaseProtocol,
        revenue_db: RevenueDatabaseProtocol,
    ):
        self.items_db = items_db
        self.sales_db = sales_db
        self.revenue_db = revenue_db

        self.cashier = Cashier(self.revenue_db, self.sales_db)
        self.receipt = None

    def simulate(self) -> None:
        count = 0
        while count != 3:
            for _ in range(5):
                for _ in range(20):
                    customer = RandomCustomer(self.items_db)
                    chosen_items = customer.choose_items()
                    payment_method = customer.choose_payment_method()
                    (
                        self.cashier.open_receipt()
                        .add_items_to_receipt(chosen_items)
                        .generate_receipt()
                        .close_receipt(payment_method)
                    )
                self.cashier.generate_x_report()
            count = self.cashier.generate_z_report(count)

    def generate_report(self) -> None:
        items_sold = self.sales_db.get_sales_record()
        revenue_data = self.revenue_db.get_revenue_record()

        self.cashier.print_report(items_sold, "Sales Report", ["Product", "Sales"])

        self.cashier.print_report(
            revenue_data, "Revenue Report", ["Payment", "Revenue"]
        )

    def generate_list(self) -> None:
        x_report_info = ""

        available_items = self.items_db.get_items()

        # Headers for the columns
        headers = [
            "Name",
            "Price",
            "Pack Size",
            "Discount Strategy",
            "Discount Amount",
            "Discount Pack",
        ]

        # Calculate maximum lengths for each column
        max_lengths = [len(header) for header in headers]
        for item in available_items:
            item_data = item.item_data()
            for i, data in enumerate(item_data):
                max_lengths[i] = max(max_lengths[i], len(str(data)))

        # Construct the header line
        header_line = " | ".join(
            f"{header.ljust(max_lengths[i])}" for i, header in enumerate(headers)
        )

        x_report_info += f"{header_line}\n"
        x_report_info += "-" * (sum(max_lengths) + len(max_lengths) * 3 - 1) + "\n"

        # Construct the rows with adjusted column widths
        for item in available_items:
            item_data = item.item_data()
            row = " | ".join(
                f"{str(data).ljust(max_lengths[i])}" for i, data in enumerate(item_data)
            )
            x_report_info += f"{row}\n"

        print(x_report_info)
