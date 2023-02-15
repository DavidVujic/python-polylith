from pathlib import Path

create_base_params = [
    (
        "1. Creates expected directories and files",
        set(["bases", "test"]),
        set(
            [
                Path("test/temp/bases/test_namespace/test_package/core.py"),
                Path("test/temp/test/bases/test_namespace/test_package/test_core.py"),
            ]
        ),
    )
]
create_base_ids = [x[0] for x in create_base_params]
