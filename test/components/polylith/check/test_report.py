from pathlib import Path

from polylith.check import report


class TestPrintExternalImports:
    """Unit tests for the print_external_models_imports function."""

    def test_print_external_models_imports(self, capsys):
        """Should print the external models imports."""
        file_name = "test/components/oiq/comment_db/interface.py"
        expected_output = (
            f"Illegal import of oiq.auth_db.models at line 4 in file {file_name}.",
            f"Illegal import of oiq.auth_db.core._generate_secret_key at line 6 in file {file_name}.",
            f"Illegal import of oiq.email_db.models at line 7 in file {file_name}.",
            f"Illegal import of oiq.user_db.models.User at line 10 in file {file_name}.",
            f"Illegal call to apps.get_model(...) at line 12 in file {file_name}. Use a _get_<model-name>_model() function from an `interface` ",  # noqa: E501
            "module instead.",
            "🤔 Found imports of internal modules from external apps. Use a function from an `interface` module instead.",  # noqa: E501
        )
        # Call the function that processes the directory files
        test_dir = "test/components/oiq/comment_db/"
        passed_check = report.print_external_imports(Path(test_dir))
        assert passed_check is False

        std_out = capsys.readouterr().out.splitlines()
        assert len(std_out) == len(expected_output)
        for line, expected in zip(std_out, expected_output):
            assert line == expected

    def test_only_internal_imports(self, capsys):
        test_dir = "test/components/oiq/walkthrough_db"
        passed_check = report.print_external_imports(Path(test_dir))
        std_out = capsys.readouterr().out
        assert std_out == ""
        assert passed_check is True
