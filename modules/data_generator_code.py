import random
from datetime import timedelta, datetime
from dataclasses import dataclass, field, asdict
from typing import List
import json

import factory
from faker import Faker

fake = Faker()


@dataclass
class Item:
    item_id: int
    material_number: str
    material_type: str
    description: str
    base_unit_of_measure: str
    quantity: int
    unit_price: float
    currency: str
    batch_number: str
    serial_number: str
    vendor: str
    manufacturer: str
    country_of_origin: str
    weight: float
    dimensions: str
    tax_code: str
    procurement_type: str
    material_group: str
    plant: str
    storage_location: str
    valuation_class: str
    price_control: str
    profit_center: str
    expiration_date: str
    # New properties
    total_amount: float
    pallet_dimensions: str
    contract_number: int


@dataclass
class Delivery:
    delivery_id: int
    delivery_date: str
    supplier: str
    carrier: str
    tracking_number: str
    order_number: str  # Added field
    items: List[Item] = field(default_factory=list)


def generate_pallet_dimensions():
    dims = [1200, 1000, 150]  # Standard dimensions in mm
    if random.random() < 0.05:  # 5% chance to create an outlier
        idx = random.randint(0, 2)  # Choose one dimension to modify
        dims[idx] -= 100  # Reduce the chosen dimension by 100mm
    return " x ".join(f"{dim}mm" for dim in dims)


class ItemFactory(factory.Factory):
    class Meta:
        model = Item

    item_id = factory.Sequence(lambda n: n + 1)
    material_number = factory.LazyAttribute(lambda _: fake.bothify(text="MAT-########"))
    material_type = factory.LazyAttribute(
        lambda _: random.choice(
            ["Raw Material", "Finished Product", "Semi-Finished", "Service"]
        )
    )
    description = factory.LazyAttribute(
        lambda _: f"{fake.color_name()} {fake.word().capitalize()} {fake.random_element(elements=('Widget', 'Gadget', 'Component'))}"
    )
    base_unit_of_measure = factory.LazyAttribute(
        lambda _: random.choice(["EA", "KG", "L", "M", "Reel", "Box", "Ton"])
    )
    quantity = factory.LazyAttribute(lambda _: random.randint(1, 1000))
    unit_price = factory.LazyAttribute(lambda _: round(random.uniform(5.0, 500.0), 2))
    currency = "USD"
    batch_number = factory.LazyAttribute(lambda _: fake.bothify(text="BN-########"))
    serial_number = factory.LazyAttribute(lambda _: fake.bothify(text="SN-##########"))
    vendor = factory.LazyAttribute(lambda _: fake.company())
    manufacturer = factory.LazyAttribute(lambda _: fake.company())
    country_of_origin = factory.LazyAttribute(lambda _: fake.country_code())
    weight = factory.LazyAttribute(lambda _: round(random.uniform(0.1, 50.0), 2))
    dimensions = factory.LazyAttribute(
        lambda _: f"{random.randint(5, 100)}x{random.randint(5, 100)}x{random.randint(5, 100)} cm"
    )
    tax_code = factory.LazyAttribute(lambda _: random.choice(["A0", "B1", "C2"]))
    procurement_type = factory.LazyAttribute(
        lambda _: random.choice(["External", "In-house"])
    )
    material_group = factory.LazyAttribute(
        lambda _: random.choice(["MG01", "MG02", "MG03"])
    )
    plant = factory.LazyAttribute(
        lambda _: random.choice(["Plant1", "Plant2", "Plant3"])
    )
    storage_location = factory.LazyAttribute(
        lambda _: random.choice(["SL01", "SL02", "SL03"])
    )
    valuation_class = factory.LazyAttribute(
        lambda _: random.choice(["3000", "7920", "7930"])
    )
    price_control = factory.LazyAttribute(
        lambda _: random.choice(["Standard", "Moving Average"])
    )
    profit_center = factory.LazyAttribute(lambda _: f"PC{random.randint(1000, 9999)}")
    expiration_date = factory.LazyAttribute(
        lambda _: fake.date_between(start_date="today", end_date="+2y").isoformat()
    )
    # New properties
    total_amount = factory.LazyAttribute(lambda o: round(o.unit_price * o.quantity, 2))
    pallet_dimensions = factory.LazyFunction(generate_pallet_dimensions)
    contract_number = factory.LazyAttribute(lambda _: random.randint(100000, 999999))


class DeliveryFactory(factory.Factory):
    class Meta:
        model = Delivery

    delivery_id = factory.Sequence(lambda n: n + 1)
    delivery_date = factory.LazyFunction(
        lambda: fake.date_between(start_date="-30d", end_date="today").isoformat()
    )
    supplier = factory.LazyAttribute(lambda _: fake.company())
    carrier = factory.LazyAttribute(lambda _: fake.company())
    tracking_number = factory.LazyAttribute(lambda _: fake.bothify(text="TN##########"))
    order_number = factory.LazyAttribute(
        lambda _: fake.bothify(text="ORD-#####")
    )  # Added field

    @factory.post_generation
    def items(self, create, extracted, **kwargs):
        if extracted:
            self.items = extracted
        else:
            self.items = ItemFactory.create_batch(random.randint(1, 5))


# Generate data and save to JSON files
if __name__ == "__main__":
    deliveries = DeliveryFactory.create_batch(100)

    # Convert deliveries to dicts for JSON serialization
    deliveries_data = []
    items_data = []

    for delivery in deliveries:
        delivery_dict = asdict(delivery)
        delivery_dict.pop("items")  # Remove items to store separately
        deliveries_data.append(delivery_dict)

        for item in delivery.items:
            item_dict = asdict(item)
            # Link item to delivery
            item_dict["delivery_id"] = delivery.delivery_id
            items_data.append(item_dict)

    # Create specific datasets

    # Data Set 1
    delivery1 = Delivery(
        delivery_id=max(d.delivery_id for d in deliveries) + 1,
        delivery_date="2023-12-16",
        supplier="Slovenia Copper",
        carrier=fake.company(),
        tracking_number=fake.bothify(text="TN##########"),
        order_number="ORD-12345",
        items=[],
    )

    item1 = Item(
        item_id=max(i["item_id"] for i in items_data) + 1,
        material_number="MAT-00000001",
        material_type="Raw Material",
        description="copper cable",
        base_unit_of_measure="Reel",
        quantity=1,
        unit_price=100000.0,
        currency="USD",
        batch_number=fake.bothify(text="BN-########"),
        serial_number=fake.bothify(text="SN-##########"),
        vendor="Slovenia Copper",
        manufacturer=fake.company(),
        country_of_origin=fake.country_code(),
        weight=50.0,
        dimensions="100x100x100 cm",
        tax_code=random.choice(["A0", "B1", "C2"]),
        procurement_type="External",
        material_group="MG01",
        plant="Plant1",
        storage_location="SL01",
        valuation_class="3000",
        price_control="Standard",
        profit_center=f"PC{random.randint(1000, 9999)}",
        expiration_date="2025-12-16",
        total_amount=100000.0,
        pallet_dimensions="1200mm x 1000mm x 150mm",
        contract_number=1415738,
    )

    item1.delivery_id = delivery1.delivery_id  # Link item to delivery
    delivery1.items.append(item1)

    # Data Set 2
    delivery2 = Delivery(
        delivery_id=delivery1.delivery_id + 1,
        delivery_date="2023-11-15",
        supplier="AluMetals",
        carrier=fake.company(),
        tracking_number=fake.bothify(text="TN##########"),
        order_number="ORD-67890",
        items=[],
    )

    item2 = Item(
        item_id=item1.item_id + 1,
        material_number="MAT-00000002",
        material_type="Raw Material",
        description="Aluminum Sheets",
        base_unit_of_measure="EA",
        quantity=500,
        unit_price=100.0,
        currency="USD",
        batch_number=fake.bothify(text="BN-########"),
        serial_number=fake.bothify(text="SN-##########"),
        vendor="AluMetals",
        manufacturer=fake.company(),
        country_of_origin=fake.country_code(),
        weight=10.0,
        dimensions="100x100x100 cm",
        tax_code=random.choice(["A0", "B1", "C2"]),
        procurement_type="External",
        material_group="MG02",
        plant="Plant2",
        storage_location="SL02",
        valuation_class="7920",
        price_control="Moving Average",
        profit_center=f"PC{random.randint(1000, 9999)}",
        expiration_date="2025-11-15",
        total_amount=50000.0,
        pallet_dimensions="1100mm x 900mm x 130mm",
        contract_number=789456,
    )

    item2.delivery_id = delivery2.delivery_id
    delivery2.items.append(item2)

    # Data Set 3
    delivery3 = Delivery(
        delivery_id=delivery2.delivery_id + 1,
        delivery_date="2023-10-20",
        supplier="SteelWorks",
        carrier=fake.company(),
        tracking_number=fake.bothify(text="TN##########"),
        order_number="ORD-54321",
        items=[],
    )

    item3 = Item(
        item_id=item2.item_id + 1,
        material_number="MAT-00000003",
        material_type="Raw Material",
        description="Steel Bars",
        base_unit_of_measure="Ton",
        quantity=73,
        unit_price=1100.0,
        currency="USD",
        batch_number=fake.bothify(text="BN-########"),
        serial_number=fake.bothify(text="SN-##########"),
        vendor="SteelWorks",
        manufacturer=fake.company(),
        country_of_origin=fake.country_code(),
        weight=73000.0,  # 73 tons
        dimensions="100x100x100 cm",
        tax_code=random.choice(["A0", "B1", "C2"]),
        procurement_type="External",
        material_group="MG03",
        plant="Plant3",
        storage_location="SL03",
        valuation_class="7930",
        price_control="Standard",
        profit_center=f"PC{random.randint(1000, 9999)}",
        expiration_date="2025-10-20",
        total_amount=88000.0,
        pallet_dimensions="1200mm x 1000mm x 150mm",
        contract_number=456391,
    )

    item3.delivery_id = delivery3.delivery_id
    delivery3.items.append(item3)

    # Append the new deliveries and items to the data lists
    deliveries.extend([delivery1, delivery2, delivery3])

    for delivery in [delivery1, delivery2, delivery3]:
        delivery_dict = asdict(delivery)
        delivery_dict.pop("items")  # Remove items to store separately
        deliveries_data.append(delivery_dict)

        for item in delivery.items:
            item_dict = asdict(item)
            # Link item to delivery
            item_dict["delivery_id"] = delivery.delivery_id
            items_data.append(item_dict)

    # Save deliveries and items to JSON files
    with open("db/deliveries.json", "w") as f:
        json.dump(deliveries_data, f, indent=4)

    with open("db/items.json", "w") as f:
        json.dump(items_data, f, indent=4)

    print("Data has been saved to 'deliveries.json' and 'items.json'.")
