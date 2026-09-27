"""
Local test suite for the Business Decision Intelligence investigation tools.

IMPORTANT:
- This test does NOT call Gemini.
- It does NOT consume Gemini API quota.
- It tests PostgreSQL analytics + RAG locally.
"""

import sys
from pathlib import Path

# Add project root to Python import path
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.agents.langgraph_investigation_demo import (
    monthly_trend_tool,
    month_comparison_tool,
    dimension_analysis_tool,
    operational_analysis_tool,
    business_document_search_tool,
)


def check_result(name, result):
    """Basic validation for a tool result."""

    print("\n" + "=" * 70)
    print(f"TEST: {name}")
    print("=" * 70)

    print("Result:")
    print(result)

    if result is None:
        raise AssertionError(f"{name} returned None")

    if isinstance(result, dict):
        if len(result) == 0:
            raise AssertionError(f"{name} returned an empty dictionary")

    elif isinstance(result, list):
        if len(result) == 0:
            raise AssertionError(f"{name} returned an empty list")

    elif isinstance(result, str):
        if not result.strip():
            raise AssertionError(f"{name} returned an empty string")

    else:
        print(f"Returned type: {type(result)}")

    print(f"PASS: {name}")


def test_monthly_trend():
    result = monthly_trend_tool(
        year=2014,
        month=7
    )

    check_result(
        "Monthly Trend",
        result
    )


def test_month_comparison():
    result = month_comparison_tool(
        year=2014,
        month=7
    )

    check_result(
        "Month Comparison",
        result
    )


def test_dimension_analysis():
    result = dimension_analysis_tool(
        year=2014,
        month=7,
        dimension="region",
        metric="sales"
    )

    check_result(
        "Dimension Analysis",
        result
    )


def test_operational_analysis():
    result = operational_analysis_tool(
        year=2014,
        month=7
    )

    check_result(
        "Operational Analysis",
        result
    )


def test_business_document_search():
    result = business_document_search_tool(
        query="discount policy and discount rules",
        top_k=5
    )

    check_result(
        "Business Document Search / RAG",
        result
    )


def main():

    print("\n")
    print("=" * 70)
    print("BUSINESS INTELLIGENCE LOCAL TOOL TEST SUITE")
    print("=" * 70)
    print("Gemini API calls: 0")
    print("Testing PostgreSQL analytics + RAG only")
    print("=" * 70)

    tests = [
        ("Monthly Trend", test_monthly_trend),
        ("Month Comparison", test_month_comparison),
        ("Dimension Analysis", test_dimension_analysis),
        ("Operational Analysis", test_operational_analysis),
        ("Business Document Search", test_business_document_search),
    ]

    passed = 0
    failed = 0

    for name, test_function in tests:

        try:
            test_function()
            passed += 1

        except Exception as error:
            failed += 1

            print("\n" + "!" * 70)
            print(f"FAIL: {name}")
            print("!" * 70)
            print(f"Error: {error}")

    print("\n")
    print("=" * 70)
    print("FINAL TEST SUMMARY")
    print("=" * 70)

    print(f"Total tests : {len(tests)}")
    print(f"Passed      : {passed}")
    print(f"Failed      : {failed}")
    print("=" * 70)

    if failed == 0:
        print("ALL LOCAL INVESTIGATION TOOLS PASSED")
        print("Gemini API calls used: 0")
    else:
        print("SOME TESTS FAILED")
        print("Fix the failed local tool before testing Gemini.")


if __name__ == "__main__":
    main()