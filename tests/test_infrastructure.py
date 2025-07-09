from faker import Faker
import pytest

from app.domain.entities.orders import OrderDM
from app.infrastructure.adapters.application.orders_gateway import (
    OrdersGatewayImpl,
)


@pytest.fixture
def orders_gateway() -> OrdersGatewayImpl:
    return OrdersGatewayImpl()


def test_create_order(orders_gateway: OrdersGatewayImpl, faker: Faker) -> None:
    uuid = faker.uuid4()
    provider = faker.pystr()
    storage_gb = faker.pyint()

    order = OrderDM(order_id=uuid, provider=provider, storage_gb=storage_gb)
    orders_gateway.add_order(order)
    created_order = orders_gateway.get_order(uuid)

    assert created_order is not None
    assert isinstance(created_order, OrderDM)

    assert created_order.order_id == uuid
    assert created_order.provider == provider
    assert created_order.storage_gb == storage_gb
    assert created_order.status == "pending"


def test_update_order_status(
    orders_gateway: OrdersGatewayImpl,
    faker: Faker,
) -> None:
    test_uuid = faker.uuid4()
    initial_order = OrderDM(
        order_id=test_uuid,
        provider=faker.pystr(),
        storage_gb=faker.pyint(),
        status="pending",
    )
    orders_gateway.add_order(initial_order)

    orders_gateway.update_status(order_id=test_uuid, status="complete")
    updated_order = orders_gateway.get_order(test_uuid)

    assert updated_order is not None
    assert updated_order.status == "complete"

    assert updated_order.order_id == initial_order.order_id
    assert updated_order.provider == initial_order.provider
    assert updated_order.storage_gb == initial_order.storage_gb
