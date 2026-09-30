from convert2qgis.xlsform2qgis.qgis_utils import LoggingSignals, QtSignalsHandler


def test_logging_signals_is_a_singleton() -> None:
    assert LoggingSignals() is LoggingSignals()
    assert QtSignalsHandler().signals is LoggingSignals()


def test_logging_signals_instance_is_not_a_class_attribute() -> None:
    # PyQt6 recurses until the stack overflows when a class holds its own instance
    assert not any(
        isinstance(value, LoggingSignals) for value in vars(LoggingSignals).values()
    )
