#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class DataTypeInvalid(Exception):
    dataclass: str


@dataclass
class DataTypeNotSet(Exception):
    operator: str


@dataclass
class OperatorInvalid(Exception):
    operator: str


@dataclass
class ExecResultValueMissing(Exception):
    result: dict


@dataclass
class MeasurementPlugin:
    """Measurement representation."""

    source: str
    datatype: type = None
    operator: object = None
    reference: object = None

    def set_datatype(self, datatype: str) -> None:
        """Set data type of measurement object."""

        if not hasattr(__builtins__, datatype):
            raise DataTypeInvalid(datatype)
        self.datatype = __builtins__.__dict__[datatype]

    def set_operator(self, operator: str) -> None:
        """Set operator of measurement object data type."""

        if not isinstance(self.datatype, type):
            raise DataTypeNotSet(self.datatype)
        if not hasattr(self.datatype, operator):
            raise OperatorInvalid(operator)
        self.operator = getattr(self.datatype, operator)

    def set_reference(self, reference) -> None:
        """Set reference value of measurement object."""

        self.reference = reference

    def evaluate(self) -> tuple:
        """
        Evaluate measurement object and return a tuple of
        the measured value and conditional results.
        """

        result = {}
        cc = compile(self.source, "<string>", "exec")
        exec(cc, {}, result)
        measurement = result.get("result")
        if not measurement:
            raise ExecResultValueMissing(result)
        if self.operator is None:
            return (measurement, None)
        if self.operator(
            self.datatype(measurement),
            self.datatype(self.reference),
        ):
            return (measurement, "PASS")
        return (measurement, "FAIL")
