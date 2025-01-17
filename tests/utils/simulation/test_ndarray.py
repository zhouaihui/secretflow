import numpy as np

from secretflow import reveal
from secretflow.utils.simulation.data.ndarray import create_ndarray
from secretflow.utils.simulation.datasets import dataset
from secretflow.utils.simulation.data import SPLIT_METHOD


def get_ndarray():
    npz = np.load(dataset('mnist'))
    x_test = npz["x_test"]
    y_test = npz["y_test"]
    return x_test, y_test


def test_create_horizontal_fedndarray_should_ok(
    sf_production_setup_devices,
):
    # WHEN
    x_test, y_test = get_ndarray()
    fed_data = create_ndarray(
        x_test,
        parts=[
            sf_production_setup_devices.alice,
            sf_production_setup_devices.bob,
            sf_production_setup_devices.carol,
        ],
        axis=0,
    )
    fed_label = create_ndarray(
        y_test,
        parts=[
            sf_production_setup_devices.alice,
            sf_production_setup_devices.bob,
            sf_production_setup_devices.carol,
        ],
        axis=0,
    )

    # THEN
    assert len(fed_data.partitions) == 3
    assert len(fed_label.partitions) == 3
    alice_data = reveal(fed_data.partitions[sf_production_setup_devices.alice])
    alice_label = reveal(fed_label.partitions[sf_production_setup_devices.alice])
    assert alice_data.shape == (3333, 28, 28)
    assert alice_label.shape == (3333,)


def test_create_vertical_fedndarray_should_ok(sf_production_setup_devices):
    # WHEN
    x_test, y_test = get_ndarray()
    fed_data = create_ndarray(
        x_test,
        parts=[
            sf_production_setup_devices.alice,
            sf_production_setup_devices.bob,
            sf_production_setup_devices.carol,
        ],
        axis=2,
    )
    fed_label = create_ndarray(
        y_test,
        parts=[
            sf_production_setup_devices.alice,
            sf_production_setup_devices.bob,
            sf_production_setup_devices.carol,
        ],
        axis=1,
        is_label=True,
    )

    # THEN

    alice_data = reveal(fed_data.partitions[sf_production_setup_devices.alice])
    alice_label = reveal(fed_label.partitions[sf_production_setup_devices.alice])
    assert alice_data.shape == (10000, 28, 9)
    assert alice_label.shape == (10000,)


def test_create_horizontal_fedndarray_dirichlet_should_ok(
    sf_production_setup_devices,
):
    # WHEN
    x_test, y_test = get_ndarray()
    fed_data = create_ndarray(
        x_test,
        parts=[
            sf_production_setup_devices.alice,
            sf_production_setup_devices.bob,
            sf_production_setup_devices.carol,
        ],
        num_classes=10,
        alpha=100,
        random_state=1234,
        target=y_test,
        split_method=SPLIT_METHOD.DIRICHLET,
        axis=0,
    )

    fed_label = create_ndarray(
        y_test,
        parts=[
            sf_production_setup_devices.alice,
            sf_production_setup_devices.bob,
            sf_production_setup_devices.carol,
        ],
        num_classes=10,
        alpha=100,
        random_state=1234,
        target=y_test,
        split_method=SPLIT_METHOD.DIRICHLET,
        axis=0,
    )

    # # THEN
    assert len(fed_data.partitions) == 3
    assert len(fed_label.partitions) == 3
    alice_data = reveal(fed_data.partitions[sf_production_setup_devices.alice])
    alice_label = reveal(fed_label.partitions[sf_production_setup_devices.alice])
    assert alice_data.shape == (3333, 28, 28)
    assert alice_label.shape == (3333,)


def test_create_horizontal_fedndarray_label_skew_should_ok(
    sf_production_setup_devices,
):
    # WHEN
    x_test, y_test = get_ndarray()
    max_class_nums = 5
    fed_data = create_ndarray(
        x_test,
        parts=[
            sf_production_setup_devices.alice,
            sf_production_setup_devices.bob,
            sf_production_setup_devices.carol,
        ],
        num_classes=10,
        random_state=1234,
        target=y_test,
        max_class_nums=max_class_nums,
        split_method=SPLIT_METHOD.LABEL_SCREW,
        axis=0,
    )

    fed_label = create_ndarray(
        y_test,
        parts=[
            sf_production_setup_devices.alice,
            sf_production_setup_devices.bob,
            sf_production_setup_devices.carol,
        ],
        num_classes=10,
        random_state=1234,
        target=y_test,
        max_class_nums=max_class_nums,
        split_method=SPLIT_METHOD.LABEL_SCREW,
        axis=0,
    )

    # # THEN
    assert len(fed_data.partitions) == 3
    assert len(fed_label.partitions) == 3
    alice_data = reveal(fed_data.partitions[sf_production_setup_devices.alice])
    alice_label = reveal(fed_label.partitions[sf_production_setup_devices.alice])
    assert alice_data.shape == (3333, 28, 28)
    assert alice_label.shape == (3333,)
