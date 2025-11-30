import importlib
from unittest.mock import patch, MagicMock
import pytest

import restmon

def test_main_runs_app_with_correct_arguments(monkeypatch: pytest.MonkeyPatch):
    mock_app = MagicMock()
    
    # mock create_app
    with patch("restmon.__main__.create_app", return_value=mock_app) as mock_create:
        # подменяем __name__ чтобы код внутри if "__main__" выполнился
        monkeypatch.setattr(restmon.__main__, "__name__", "__main__") # type: ignore
        
        # подменяем env
        monkeypatch.setenv("PORT", "9999")

        # повторно импортируем модуль — тогда код выполнится
        importlib.reload(restmon.__main__) # type: ignore

        mock_create.assert_called_once()
        mock_app.run.assert_called_once_with(
            host='0.0.0.0',
            port=9999,
            debug=True
        )


def test_main_import_does_not_run():
    # тест что при обычном импорте run не вызовется
    with patch("restmon.__main__.create_app") as mock_create:
        importlib.reload(restmon.__main__) # type: ignore

        # не должен вызываться, т.к. __name__ != "__main__"
        mock_create.assert_not_called()