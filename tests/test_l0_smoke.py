"""L0 scaffold: packages import and expose version.

Traceability: foundation for EPIC-DG-01 / EPIC-DG-02 (IMPLEMENTATION_PLAN §2.4 L0).
Add ``@pytest.mark.req("AC-DG-…")`` when a dedicated L0 acceptance criterion is filed.
"""

import pytest


@pytest.mark.unit
def test_packages_import() -> None:
    import deepguard_api
    import deepguard_core
    import deepguard_graph
    import deepguard_worker

    for mod in (deepguard_core, deepguard_graph, deepguard_api, deepguard_worker):
        assert hasattr(mod, "__version__")
        assert mod.__version__ == "0.1.0"
