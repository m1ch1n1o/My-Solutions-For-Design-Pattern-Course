from models.item import ItemBuilder

PRODUCT_1 = (
    ItemBuilder()
    .with_name("Smartphone")
    .and_price(899.99)
    .and_discount("NoDiscount")
    .build()
)

PRODUCT_2 = (
    ItemBuilder()
    .with_name("Laptop")
    .and_price(1300)
    .and_pack_size(2)
    .and_discount("BatchDiscount")
    .and_discount_amount(10)
    .and_pack_discount(10)
    .build()
)

PRODUCT_3 = (
    ItemBuilder()
    .with_name("Headphones")
    .and_price(149.99)
    .and_discount("ItemDiscount")
    .and_discount_amount(20)
    .build()
)

PRODUCT_4 = (
    ItemBuilder()
    .with_name("Smartwatch")
    .and_price(300)
    .and_pack_size(2)
    .and_discount("BatchDiscount")
    .and_discount_amount(15)
    .and_pack_discount(2)
    .build()
)

PRODUCT_5 = (
    ItemBuilder()
    .with_name("Bluetooth Speaker")
    .and_price(80)
    .and_discount("NoDiscount")
    .build()
)
