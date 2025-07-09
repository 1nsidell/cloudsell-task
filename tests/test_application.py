from typing import cast
from unittest.mock import Mock, create_autospec
from uuid import uuid4

from faker import Faker
import pytest

from app.application.common.dto.orders import GetOrderDTO, NewOrderDTO
from app.application.common.dto.pricing_plans import PricingPlansPagination
from app.application.common.ports import OrdersGateway
from app.application.common.ports.api_client import ProviderClient
from app.application.common.ports.uuid_generator import UUIDGenerator
from app.application.interactors import (
    GetOrderInteractor,
    NewOrderInteractor,
    PricingPlansPaginationInteractor,
)
from app.domain.entities.orders import OrderDM
from app.domain.entities.pricing_plans import PricingPlanDM


@pytest.fixture
def orders_gateway_mock() -> Mock:
    return cast(Mock, create_autospec(OrdersGateway))


@pytest.fixture
def get_order_interactor(
    orders_gateway_mock: OrdersGateway,
) -> GetOrderInteractor:
    return GetOrderInteractor(orders_gateway=orders_gateway_mock)


@pytest.fixture
def get_order_sample_order() -> OrderDM:
    return OrderDM(
        order_id=str(uuid4()),
        provider="A",
        storage_gb=100,
        status="complete",
    )


class TestGetOrderInteractor:
    def test_returns_order_when_exists(
        self,
        get_order_interactor: GetOrderInteractor,
        orders_gateway_mock: Mock,
        get_order_sample_order: OrderDM,
    ) -> None:
        test_dto = GetOrderDTO(order_id=str(get_order_sample_order.order_id))
        orders_gateway_mock.get_order.return_value = get_order_sample_order

        result = get_order_interactor.run(test_dto)

        assert result == get_order_sample_order
        orders_gateway_mock.get_order.assert_called_once_with(
            test_dto.order_id
        )

    def test_returns_none_when_not_exists(
        self,
        get_order_interactor: GetOrderInteractor,
        orders_gateway_mock: Mock,
        faker: Faker,
    ) -> None:
        test_dto = GetOrderDTO(order_id=faker.uuid4())
        orders_gateway_mock.get_order.return_value = None

        result = get_order_interactor.run(test_dto)

        assert result is None
        orders_gateway_mock.get_order.assert_called_once_with(
            test_dto.order_id
        )


@pytest.fixture
def uuid_generator_mock() -> Mock:
    return Mock(spec=UUIDGenerator)


@pytest.fixture
def new_order_interactor(
    orders_gateway_mock: OrdersGateway,
    uuid_generator_mock: UUIDGenerator,
) -> NewOrderInteractor:
    return NewOrderInteractor(
        orders_gateway=orders_gateway_mock,
        uuid_genetator=uuid_generator_mock,
    )


@pytest.fixture
def new_order_dto(faker: Faker) -> NewOrderDTO:
    return NewOrderDTO(
        provider=faker.pystr(),
        storage_gb=faker.pyint(min_value=1, max_value=1000),
    )


class TestNewOrderInteractor:
    def test_creates_order_with_correct_parameters(
        self,
        new_order_interactor: NewOrderInteractor,
        orders_gateway_mock: Mock,
        uuid_generator_mock: Mock,
        new_order_dto: NewOrderDTO,
        faker: Faker,
    ) -> None:

        test_uuid = faker.uuid4()
        uuid_generator_mock.return_value = test_uuid
        orders_gateway_mock.add_order.return_value = str(test_uuid)

        result = new_order_interactor.run(new_order_dto)

        uuid_generator_mock.assert_called_once()

        orders_gateway_mock.add_order.assert_called_once()
        call_args = orders_gateway_mock.add_order.call_args[1]
        assert call_args["order"].order_id == test_uuid
        assert call_args["order"].provider == new_order_dto.provider
        assert call_args["order"].storage_gb == new_order_dto.storage_gb
        assert call_args["order"].status == "pending"

        assert result == str(test_uuid)

    def test_returns_order_id_from_gateway(
        self,
        new_order_interactor: NewOrderInteractor,
        orders_gateway_mock: Mock,
        uuid_generator_mock: Mock,
        new_order_dto: NewOrderDTO,
        faker: Faker,
    ) -> None:

        test_uuid = faker.uuid4()
        expected_id = "custom-id-123"
        uuid_generator_mock.return_value = test_uuid
        orders_gateway_mock.add_order.return_value = expected_id

        result = new_order_interactor.run(new_order_dto)

        assert result == expected_id

    def test_uses_new_uuid_for_each_order(
        self,
        new_order_interactor: NewOrderInteractor,
        orders_gateway_mock: Mock,
        uuid_generator_mock: Mock,
        new_order_dto: NewOrderDTO,
    ) -> None:
        uuid1 = uuid4()
        uuid2 = uuid4()
        uuid_generator_mock.side_effect = [uuid1, uuid2]
        orders_gateway_mock.add_order.side_effect = lambda order: str(
            order.order_id
        )

        result1 = new_order_interactor.run(new_order_dto)
        result2 = new_order_interactor.run(new_order_dto)

        assert result1 == str(uuid1)
        assert result2 == str(uuid2)
        assert uuid_generator_mock.call_count == 2  # noqa


@pytest.fixture
def provider_a_mock() -> Mock:
    return cast(Mock, create_autospec(ProviderClient))


@pytest.fixture
def provider_b_mock() -> Mock:
    return cast(Mock, create_autospec(ProviderClient))


@pytest.fixture
def pricing_plans_interactor(
    provider_a_mock: Mock,
    provider_b_mock: Mock,
) -> PricingPlansPaginationInteractor:
    return PricingPlansPaginationInteractor(provider_a_mock, provider_b_mock)


def create_test_provider_plans(
    provider: str,
    storage_gb: int,
    price_per_gb: float,
) -> PricingPlanDM:
    return PricingPlanDM(
        provider=provider,
        storage_gb=storage_gb,
        price_per_gb=price_per_gb,
    )


class TestPricingPlansInteractor:
    def test_returns_filtered_and_sorted_plans(
        self,
        pricing_plans_interactor: PricingPlansPaginationInteractor,
        provider_a_mock: Mock,
        provider_b_mock: Mock,
    ) -> None:

        test_plans_a = [
            create_test_provider_plans(
                provider="A",
                storage_gb=100,
                price_per_gb=0.02,
            ),
            create_test_provider_plans(
                provider="A",
                storage_gb=150,
                price_per_gb=0.021,
            ),
        ]
        test_plans_b = [
            create_test_provider_plans(
                provider="B",
                storage_gb=120,
                price_per_gb=0.017,
            ),
            create_test_provider_plans(
                provider="B",
                storage_gb=180,
                price_per_gb=0.016,
            ),
        ]

        provider_a_mock.get_plans.return_value = test_plans_a
        provider_b_mock.get_plans.return_value = test_plans_b

        pagination = PricingPlansPagination(min_storage=110)

        result = pricing_plans_interactor.run(pagination)

        assert result is not None
        assert len(result) == 3  # noqa
        assert [p.storage_gb for p in result] == [
            120,
            180,
            150,
        ]
        assert all(p.storage_gb >= 110 for p in result)  # noqa
