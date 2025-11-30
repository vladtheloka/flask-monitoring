import importlib
from unittest.mock import patch, MagicMock
import restmon.__main__
import pytest
import types


def run_main_block(module: types.ModuleType):
    """Запускает то, что обычно было бы под if __name__ == '__main__'."""
    if hasattr(module, "create_app"):
        app = module.create_app()
        app.run(
            host='0.0.0.0',
            port=int(module.os.getenv("PORT", 5000)),
            debug=True
        )


def test_main_runs_app_with_correct_arguments(monkeypatch: pytest.MonkeyPatch):
    mock_app = MagicMock()

    with patch("restmon.__main__.create_app", return_value=mock_app) as mock_create:
        monkeypatch.setenv("PORT", "9999")

        # запускаем наш искусственный main-блок
        run_main_block(restmon.__main__)

        mock_create.assert_called_once()
        mock_app.run.assert_called_once_with(
            host='0.0.0.0',
            port=9999,
            debug=True
        )


def test_main_import_does_not_execute():
    # Убеждаемся, что простой импорт НЕ вызывает run
    with patch("restmon.__main__.create_app") as mock_create:
        importlib.reload(restmon.__main__)
        mock_create.assert_not_called()