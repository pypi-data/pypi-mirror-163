"""This module provides a class for pushdown automata

"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple, Sequence, Set

import formgram.classes.grammar as grammar_classes
from formgram.machines.pushdown_automata.grammar_interface import from_context_free_grammar
from formgram.machines.pushdown_automata.simulation_functions import run_full_simulation


@dataclass(frozen=True)
class PushdownAutomatonData:
    """Container for all internal values for any finite automaton

    As it is frozen all internal values for any finite automaton are fixed,
    """
    states: Set[str]
    starting_state: str
    accepting_states: Set[str]
    alphabet: Set[str]
    stack_alphabet: Set[str]
    initial_stack_symbol: str
    transitions: Set[Tuple[str, str, str, str, str]]

    def to_dict(self) -> dict:
        """Create dictionary representation of this pushdown automaton

        :return:
        """
        return {
            "transitions": self.transitions,
            "accepting_states": self.accepting_states,
            "initial_stack_symbol": self.initial_stack_symbol,
            "starting_state": self.starting_state,
            "states": self.states,
            "alphabet": self.alphabet,
            "stack_alphabet": self.stack_alphabet
            }

    @classmethod
    def from_dict(cls, pushdown_automaton_dictionary: dict) -> PushdownAutomatonData:
        """Create new pushdown automaton from dictionary

        :param pushdown_automaton_dictionary:
        :return:
        """
        return cls(**pushdown_automaton_dictionary)

    @classmethod
    def from_grammar(cls, grammar: grammar_classes.ContextFreeGrammar) -> PushdownAutomatonData:
        """Create new pushdown automaton from Grammar object

        :param grammar:
        :return:
        """
        return cls.from_dict(from_context_free_grammar(grammar.to_dict()))


class PushdownAutomaton(PushdownAutomatonData):
    """A nondeterministic push down automaton.
    """

    def does_accept(self, word: Sequence[str], state_accepting: bool = False) -> bool:
        """Simulate the automaton on the word

        :param word:
        :param state_accepting: Toggle between state and stack accepting
            * `True`: accept if and only if halts in accepting state
            * `False`: accept if and only if halts with empty stack
        :return:
        """
        return run_full_simulation(machine=self.to_dict(), input_tape=word, state_accepting=state_accepting)
