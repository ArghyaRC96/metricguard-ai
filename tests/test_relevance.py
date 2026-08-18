from types import SimpleNamespace

from metricguard.retrieval import (
    RelevanceGate,
)


def candidate(
    score: float,
):
    return SimpleNamespace(
        rerank_score=score
    )


def test_supported_score_passes():

    gate = RelevanceGate(
        threshold=0.27
    )

    result = gate.assess(
        [
            candidate(0.53),
            candidate(0.20),
        ]
    )

    assert (
        result.is_relevant
        is True
    )

    assert (
        result.top1_rerank_score
        == 0.53
    )


def test_unsupported_score_fails():

    gate = RelevanceGate(
        threshold=0.27
    )

    result = gate.assess(
        [
            candidate(0.012),
            candidate(0.007),
        ]
    )

    assert (
        result.is_relevant
        is False
    )


def test_empty_results_fail():

    gate = RelevanceGate(
        threshold=0.27
    )

    result = gate.assess([])

    assert (
        result.is_relevant
        is False
    )

    assert (
        result.top1_rerank_score
        is None
    )


def test_gate_uses_highest_score():

    gate = RelevanceGate(
        threshold=0.27
    )

    result = gate.assess(
        [
            candidate(0.10),
            candidate(0.60),
            candidate(0.20),
        ]
    )

    assert (
        result.is_relevant
        is True
    )

    assert (
        result.top1_rerank_score
        == 0.60
    )