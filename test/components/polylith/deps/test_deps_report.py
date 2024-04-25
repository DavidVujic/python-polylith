from polylith.deps.report import create_rows

bases_in_workspace = {"x"}
components_in_workspace = {"a", "b"}


def test_to_row_returns_columns_for_all_bricks():
    expected_length = len(bases_in_workspace) + len(components_in_workspace)

    # the base x imports the component a
    # the component a imports the component b
    # the component b imports nothing
    collected_import_data = {"x": {"a"}, "a": {"b"}}
    flattened_imports = set().union(*collected_import_data.values())

    rows = create_rows(
        bases_in_workspace,
        components_in_workspace,
        collected_import_data,
        flattened_imports,
    )

    assert len(rows) == expected_length

    for columns in rows:
        assert len(columns) == expected_length
