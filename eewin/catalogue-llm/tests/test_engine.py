import pytest

from dre_estimation.engine import Assembly, Component, Product, UnitError, count_unit, price_assembly, price_product
from dre_estimation.raw import load_units
from dre_estimation.search import terms, where_score

U = load_units()


def test_unit_ratios():
    assert U.ratio("U", "C") == pytest.approx(0.01)
    assert U.ratio("C", "U") == pytest.approx(100)
    assert U.ratio("F", "KM") == pytest.approx(0.0003048, rel=1e-3)
    assert U.ratio("CF", "F") == pytest.approx(100)
    assert U.ratio("P", "F") == 1.0  # French code for foot


def test_incompatible_units_raise():
    with pytest.raises(UnitError):
        U.ratio("U", "F")


def test_count_unit():
    assert count_unit("C") == "U" and count_unit("KM") == "M" and count_unit("CF") == "F" and count_unit("U") == "U"


def test_product_priced_per_hundred():
    box = Product("B", "box", 697.49, "C", 0.2, "U")
    ln = price_product(box, 3, "U", U)
    assert ln.material == pytest.approx(3 * 6.9749)
    assert ln.hours == pytest.approx(0.6)
    assert ln.warnings == []


def test_cable_per_km_in_feet():
    cable = Product("W", "cable", 6980.95, "KM", 0.03, "F")
    ln = price_product(cable, 25, "F", U)
    assert ln.material == pytest.approx(53.19, abs=0.01)
    assert ln.hours == pytest.approx(0.75)


def test_missing_price_and_labor_are_flagged_not_zeroed_silently():
    ln = price_product(Product("X", "x", 0, "U", 0, "U"), 5, "U", U)
    assert ln.material == 0 and "NO PRICE" in ln.warnings and "NO LABOR TIME" in ln.warnings


def test_bad_unit_is_a_warning():
    ln = price_product(Product("X", "x", 10, "U", 1, "U"), 5, "F", U)
    assert ln.material == 0 and any("price unit" in w for w in ln.warnings)


def test_assembly_30a_receptacle():
    prods = {
        "box": Product("box", "box", 697.49, "C", 0.2, "U"),
        "conn": Product("conn", "conn", 78.07, "C", 0.0, "U"),
        "cable": Product("cable", "cable", 6980.95, "KM", 0.03, "F"),
        "rec": Product("rec", "rec", 0.0, "U", 0.4, "U"),
        "plate": Product("plate", "plate", 5.79, "U", 0.05, "U"),
    }
    comps = [Component("box", 1, "U", "L"), Component("conn", 2, "U", "L"), Component("cable", 25, "F", "L"),
             Component("rec", 1, "U", "L"), Component("plate", 1, "U", "L")]
    a = Assembly("A", "prise 30A", "U", 1.4, "U", 0.0, comps)
    ln = price_assembly(a, 2, "U", 0, prods, U)
    assert ln.material == pytest.approx(2 * 67.52, abs=0.02)
    assert ln.hours == pytest.approx(2.8)
    assert ln.warnings == ["rec no price"]


def test_assembly_ignores_estimated_labor_on_components():
    p = Product("c", "c", 1.0, "U", 0.5, "U", labor_source="past quotes")
    a = Assembly("A", "a", "U", 0, "U", 0, [Component("c", 1, "U", "L")])
    assert price_assembly(a, 1, "U", 0, {"c": p}, U).hours == 0


def test_section_components_and_section_hours():
    p = Product("c", "c", 2.0, "U", 0.0, "U")
    a = Assembly("A", "a", "F", 0, "F", 0.5, [Component("c", 2, "U", "S")])
    ln = price_assembly(a, 100, "F", 3, {"c": p}, U)
    assert ln.material == pytest.approx(12.0) and ln.hours == pytest.approx(1.5)


def test_search_terms_and_short_tokens():
    t = terms("prise 30A 1/2 po")
    assert any("RECEPT" in alts for alts in t)
    _, params, n = where_score("1G plaque")
    assert n == 2 and "% 1G%" in params


def test_assembly_uses_stored_labor_time():
    p = Product("c", "c", 1.0, "U", 0.3, "U")
    a = Assembly("A", "a", "U", 1.225, "U", 0.0, [Component("c", 1, "U", "L")])
    assert price_assembly(a, 4, "U", 0, {"c": p}, U).hours == pytest.approx(4.9)


def test_assembly_surfaces_component_unit_warnings():
    p = Product("c", "c", 10.0, "U", 1.0, "U")
    a = Assembly("A", "a", "U", 1.0, "U", 0.0, [Component("c", 1, "F", "L"), Component("c", 2, "F", "L")])
    ln = price_assembly(a, 2, "U", 0, {"c": p}, U)
    assert ln.material == 0 and ln.hours == pytest.approx(2.0)
    assert ln.warnings == ["c price unit: no conversion from 'F' to 'U'"]  # stored labor: child hours are not used


def test_assembly_no_price_warning_only_for_non_zero_quantity():
    p = Product("c", "c", 0.0, "U", 0.0, "U")
    a = Assembly("A", "a", "U", 1.0, "U", 0.0, [Component("c", 0, "U", "L")])
    assert price_assembly(a, 2, "U", 0, {"c": p}, U).warnings == []


def test_healthy_assembly_has_no_warnings():
    p = Product("c", "c", 10.0, "U", 0.3, "U")
    a = Assembly("A", "a", "U", 1.0, "U", 0.0, [Component("c", 1, "U", "L")])
    ln = price_assembly(a, 2, "U", 0, {"c": p}, U)
    assert ln.material == pytest.approx(20.0) and ln.hours == pytest.approx(2.0) and ln.warnings == []


def test_assembly_without_labor_is_flagged():
    p = Product("c", "c", 1.0, "U", 0.5, "U", labor_source="past quotes")
    a = Assembly("A", "a", "U", 0, "U", 0, [Component("c", 1, "U", "L")])
    ln = price_assembly(a, 1, "U", 0, {"c": p}, U)
    assert ln.hours == 0 and ln.material == pytest.approx(1.0) and ln.warnings == ["NO LABOR TIME"]


def test_assembly_with_labor_or_zero_quantity_has_no_labor_warning():
    p = Product("c", "c", 1.0, "U", 0.0, "U")
    stored = Assembly("A", "a", "U", 1.0, "U", 0, [Component("c", 1, "U", "L")])
    fallback = Assembly("B", "b", "U", 0, "U", 0, [Component("k", 1, "U", "L")])
    section = Assembly("C", "c", "F", 0, "F", 0.5, [Component("c", 2, "U", "S")])
    none = Assembly("D", "d", "U", 0, "U", 0, [Component("c", 1, "U", "L")])
    prods = {"c": p, "k": Product("k", "k", 1.0, "U", 0.3, "U")}
    assert "NO LABOR TIME" not in price_assembly(stored, 2, "U", 0, prods, U).warnings
    assert "NO LABOR TIME" not in price_assembly(fallback, 2, "U", 0, prods, U).warnings
    assert "NO LABOR TIME" not in price_assembly(section, 100, "F", 3, prods, U).warnings
    assert "NO LABOR TIME" not in price_assembly(none, 0, "U", 0, prods, U).warnings


def test_section_only_labor_with_zero_sections_is_not_flagged():  # E1
    p = Product("c", "c", 2.0, "U", 0.0, "U")
    a = Assembly("A", "a", "F", 0, "F", 0.5, [Component("c", 2, "U", "S")])
    ln = price_assembly(a, 100, "F", 0, {"c": p}, U)
    assert ln.material == 0 and ln.hours == 0 and ln.warnings == []


def test_child_labor_unit_warning_only_when_component_hours_are_used():  # E2
    prods = {"w": Product("w", "w", 5.0, "F", 0.3, "U")}
    comps = [Component("w", 10, "F", "L")]
    msg = "w labor unit: no conversion from 'F' to 'U'"
    stored = price_assembly(Assembly("A", "a", "U", 1.0, "U", 0, comps), 2, "U", 0, prods, U)
    assert stored.material == pytest.approx(100.0) and stored.hours == pytest.approx(2.0) and stored.warnings == []
    fallback = price_assembly(Assembly("A", "a", "U", 0, "U", 0, comps), 2, "U", 0, prods, U)
    assert fallback.hours == 0 and fallback.warnings == [msg, "NO LABOR TIME"]
    failed = price_assembly(Assembly("A", "a", "U", 1.0, "F", 0, comps), 2, "U", 0, prods, U)
    assert failed.hours == 0 and failed.warnings == ["assembly labor unit: no conversion from 'U' to 'F'", msg]


def test_zero_quantity_component_contributes_no_warning():  # E3
    prods = {"c": Product("c", "c", 10.0, "U", 1.0, "U")}
    comps = [Component("c", 0, "F", "L"), Component("c", 1, "F", "S"), Component("c", 0, "U", "L", 1.0, "F"),
             Component("z", 0, "U", "L")]
    ln = price_assembly(Assembly("A", "a", "U", 0, "U", 0.5, comps), 2, "U", 0, prods, U)
    assert ln.material == 0 and ln.hours == 0 and ln.warnings == [] and len(ln.children) == 2
    used = price_assembly(Assembly("A", "a", "U", 1.0, "U", 0, [Component("c", 1, "F", "L")]), 2, "U", 0, prods, U)
    assert used.warnings == ["c price unit: no conversion from 'F' to 'U'"]


def test_sections_without_quantity_still_flag_missing_labor():  # E4
    prods = {"c": Product("c", "c", 2.0, "U", 0.0, "U")}
    a = Assembly("A", "a", "U", 0, "U", 0, [Component("c", 2, "U", "S")])
    ln = price_assembly(a, 0, "U", 3, prods, U)
    assert ln.material == pytest.approx(12.0) and ln.hours == 0 and ln.warnings == ["NO LABOR TIME"]
    assert price_assembly(a, 0, "U", 0, prods, U).warnings == []
    timed = Assembly("A", "a", "U", 0, "U", 0.5, [Component("c", 2, "U", "S")])
    ln = price_assembly(timed, 0, "U", 3, prods, U)
    assert ln.hours == pytest.approx(1.5) and ln.warnings == []


def test_assembly_warnings_are_deduplicated_in_order():  # E5
    prods = {"c": Product("c", "c", 1.0, "U", 0.0, "U")}
    missing = Assembly("A", "a", "U", 1.0, "U", 0, [Component("z", 1, "U", "L"), Component("c", 1, "U", "L", 1.0, "F"),
                                                    Component("z", 2, "U", "L"), Component("c", 2, "U", "L", 1.0, "F")])
    ln = price_assembly(missing, 2, "U", 0, prods, U)
    assert ln.hours == pytest.approx(2.0)
    assert ln.warnings == ["missing component z", "c: no conversion from 'U' to 'F'"]


def test_failed_assembly_labor_conversion_is_not_reported_as_no_labor_time():  # E6
    prods = {"c": Product("c", "c", 1.0, "U", 0.0, "U")}
    a = Assembly("A", "a", "U", 1.0, "F", 0, [Component("c", 1, "U", "L")])
    ln = price_assembly(a, 2, "U", 0, prods, U)
    assert ln.material == pytest.approx(2.0) and ln.hours == 0
    assert ln.warnings == ["assembly labor unit: no conversion from 'U' to 'F'"]
