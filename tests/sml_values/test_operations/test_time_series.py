from tests.sml_values.test_operations.helper import check_description, check_operation_repr

from sml2mqtt.const import SmlFrameValues, TimeSeries
from sml2mqtt.sml_value.base import SmlValueInfo
from sml2mqtt.sml_value.operations import (
    MaxOfIntervalOperation,
    MeanOfIntervalOperation,
    MinOfIntervalOperation,
)


def info(timestamp: int):
    return SmlValueInfo(None, SmlFrameValues.create(timestamp, []), 0)


def test_max() -> None:
    o = MaxOfIntervalOperation(TimeSeries(5), False)
    check_operation_repr(o, 'interval=5s')

    assert o.process_value(None, info(0)) is None
    assert o.process_value(5, info(0)) == 5
    assert o.process_value(3, info(3)) == 5
    assert o.process_value(2, info(8)) == 3
    assert o.process_value(1, info(13)) == 2
    assert o.process_value(1, info(14)) == 2

    o = MaxOfIntervalOperation(TimeSeries(5, wait_for_data=True), False)
    check_operation_repr(o, 'interval=5s')

    assert o.process_value(None, info(0)) is None
    assert o.process_value(5, info(0)) is None
    assert o.process_value(3, info(3)) is None
    assert o.process_value(2, info(8)) == 3
    assert o.process_value(1, info(13)) == 2
    assert o.process_value(1, info(14)) == 2

    o = MaxOfIntervalOperation(TimeSeries(5, wait_for_data=True), True)
    check_operation_repr(o, 'interval=5s')

    assert o.process_value(None, info(0)) is None
    assert o.process_value(5, info(0)) is None
    assert o.process_value(3, info(3)) is None
    assert o.process_value(2, info(8)) == 3
    assert o.process_value(2, info(10)) is None
    assert o.process_value(1, info(14)) is None
    assert o.process_value(1, info(15)) == 2

    check_description(
        o, [
            '- Max Of Interval:',
            '    Interval: 5 seconds',
            '    Wait for data: True',
            '    Reset after value: True',
        ]
    )


def test_min() -> None:
    o = MinOfIntervalOperation(TimeSeries(5), False)
    check_operation_repr(o, 'interval=5s')

    assert o.process_value(None, info(0)) is None
    assert o.process_value(1, info(0)) == 1
    assert o.process_value(2, info(3)) == 1
    assert o.process_value(3, info(8)) == 2
    assert o.process_value(4, info(13)) == 3
    assert o.process_value(5, info(14)) == 3

    check_description(
        o, [
            '- Min Of Interval:',
            '    Interval: 5 seconds',
            '    Wait for data: False',
            '    Reset after value: False',
        ]
    )


def test_mean() -> None:
    o = MeanOfIntervalOperation(TimeSeries(10), False)
    check_operation_repr(o, 'interval=10s')

    assert o.process_value(None, info(0)) is None
    assert o.process_value(1, info(0)) is None
    assert o.process_value(2, info(5)) == 1
    assert o.process_value(2, info(10)) == 1.5
    assert o.process_value(2, info(13)) == 1.8
    assert o.process_value(4, info(15)) == 2
    assert o.process_value(4, info(20)) == 3

    o = MeanOfIntervalOperation(TimeSeries(10, wait_for_data=True), False)
    check_operation_repr(o, 'interval=10s')

    assert o.process_value(None, info(0)) is None
    assert o.process_value(1, info(0)) is None
    assert o.process_value(2, info(5)) is None
    assert o.process_value(2, info(10)) == 1.5
    assert o.process_value(2, info(13)) == 1.8
    assert o.process_value(4, info(15)) == 2
    assert o.process_value(4, info(20)) == 3

    check_description(
        o, [
            '- Mean Of Interval:',
            '    Interval: 10 seconds',
            '    Wait for data: True',
            '    Reset after value: False',
        ]
    )
