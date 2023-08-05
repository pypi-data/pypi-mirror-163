"""This module provides a class for turing machines

"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Sequence, Set

from formgram.machines.turing_machines.grammar_interface import from_grammar
from formgram.machines.turing_machines.simulation_functions import run_full_simulation
import formgram.classes.grammar as grammar_classes


@dataclass
class TuringMachineData:
    """Container for all internal values for any finite automaton

    As it is frozen all internal values for any finite automaton are fixed,
    """
    states: Set[str]
    initial_state: str
    accepting_states: Set[str]
    alphabet: Set[str]
    control_symbols: Set[str]
    blank_symbol: str
    transitions: Set[Tuple[Tuple[str, str], Tuple[str, str, str]]]

    def to_dict(self) -> dict:
        """Create a dictionary representation of this machine

        :return:
        """
        return {
            "states": self.states,
            "initial_state": self.initial_state,
            "accepting_states": self.accepting_states,
            "alphabet": self.alphabet,
            "control_symbols": self.control_symbols,
            "blank_symbol": self.blank_symbol,
            "transitions": self.transitions
        }

    @classmethod
    def from_dict(cls, machine_dict: dict) -> TuringMachineData:
        """Create a turing machine from dictionary representation

        :param machine_dict:
        :return:
        """
        return cls(**machine_dict)

    @classmethod
    def from_grammar(cls, grammar: grammar_classes.Grammar) -> TuringMachineData:
        """Create a turing machine from a grammar object

        :param grammar:
        :return:
        """
        return cls.from_dict(from_grammar(grammar.to_dict()))


class TuringMachine(TuringMachineData):
    """A Turing Machine
    """

    def __init__(self, *args, **kwargs):
        """Initialize the object by various methods

        Allowed methods:
        * By grammar object
        * By machine dictionary

        :param args:
        :param kwargs:
        """

    def does_accept(self, word: Sequence[str], fuel: int = 100, raise_exception_on_empty_fuel: bool = True) -> bool:
        """Simulate the machine on given word for a limited amount of steps

        :param word:
        :param fuel: Limit of steps
        :param raise_exception_on_empty_fuel: If `False` the machine just
            rejects when fuel runs out. For `True` the machine will raise an
            :class:`TimeoutError`
        :raises TimeoutError:
        :return:
        """
        return run_full_simulation(machine=self.to_dict(),
                                   input_tape=word, fuel=fuel,
                                   raise_exception_on_empty_fuel=raise_exception_on_empty_fuel)
