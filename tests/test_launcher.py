import pytest
from unittest.mock import MagicMock, AsyncMock, patch
from subprocess import Popen


# ─────────────────────────────────────────────
# AppLauncher — open_app
# ─────────────────────────────────────────────

class TestAppLauncherOpenApp:
    def _make_launcher(self):
        from modules.app_launcher import AppLauncher
        wc = MagicMock()
        with patch("modules.app_launcher.BrowserController"):
            launcher = AppLauncher(wc)
        return launcher

    def test_opens_browser_by_alias(self):
        launcher = self._make_launcher()
        with patch("modules.app_launcher.subprocess.Popen") as mock_popen:
            result = launcher.open_app("open browser")
        assert result
        mock_popen.assert_called_once()

    def test_opens_app_by_partial_alias(self):
        launcher = self._make_launcher()
        with patch("modules.app_launcher.subprocess.Popen") as mock_popen:
            result = launcher.open_app("launch pycharm please")
        assert result
        mock_popen.assert_called_once()

    def test_unknown_command_returns_false(self):
        launcher = self._make_launcher()
        result = launcher.open_app("do something random")
        assert result is False

    def test_sets_current_app_on_launch(self):
        launcher = self._make_launcher()
        with patch("subprocess.Popen"):
            launcher.open_app("open browser")
        assert launcher.current_app == "browser"

    def test_launch_failure_returns_false(self):
        launcher = self._make_launcher()
        with patch("modules.app_launcher.subprocess.Popen", side_effect=Exception("not found")):
            result = launcher.open_app("open browser")
        assert result is False

# ─────────────────────────────────────────────
# AppLauncher — handle_command routing
# ─────────────────────────────────────────────

class TestAppLauncherHandleCommand:
    def _make_launcher(self):
        from modules.app_launcher import AppLauncher
        wc = MagicMock()
        with patch("modules.app_launcher.BrowserController"):
            launcher = AppLauncher(wc)
        launcher.browser_controller = AsyncMock()
        launcher.browser_controller.handle_command = AsyncMock(return_value=False)
        return launcher

    @pytest.mark.asyncio
    async def test_routes_to_open_app(self):
        launcher = self._make_launcher()
        with patch("subprocess.Popen"):
            result = await launcher.handle_command("open browser")
        assert result is True

    @pytest.mark.asyncio
    async def test_routes_to_browser_controller(self):
        launcher = self._make_launcher()
        launcher.browser_controller.handle_command = AsyncMock(return_value=True)
        result = await launcher.handle_command("search for cats")
        assert result is True

    @pytest.mark.asyncio
    async def test_unknown_command_returns_false(self):
        launcher = self._make_launcher()
        result = await launcher.handle_command("do nothing")
        assert result is False

    @pytest.mark.asyncio
    async def test_command_is_lowercased(self):
        launcher = self._make_launcher()
        with patch("subprocess.Popen"):
            result = await launcher.handle_command("OPEN BROWSER")
        assert result is True


# ─────────────────────────────────────────────
# BrowserController — page alive check
# ─────────────────────────────────────────────

class TestBrowserControllerPageAlive:
    def _make_browser(self):
        from modules.browser_controller import BrowserController
        return BrowserController()

    @pytest.mark.asyncio
    async def test_returns_false_when_page_is_none(self):
        bc = self._make_browser()
        bc.page = None
        result = await bc._ensure_page_alive()
        assert result is False

    @pytest.mark.asyncio
    async def test_returns_true_when_page_alive(self):
        bc = self._make_browser()
        bc.page = AsyncMock()
        bc.page.title = AsyncMock(return_value="Google")
        result = await bc._ensure_page_alive()
        assert result is True

    @pytest.mark.asyncio
    async def test_resets_state_when_page_dead(self):
        bc = self._make_browser()
        bc.page = AsyncMock()
        bc.page.title = AsyncMock(side_effect=Exception("Target closed"))
        bc.browser = MagicMock()
        bc.context = MagicMock()

        result = await bc._ensure_page_alive()
        assert result is False
        assert bc.page is None
        assert bc.browser is None
        assert bc.context is None


# ─────────────────────────────────────────────
# BrowserController — handle_command routing
# ─────────────────────────────────────────────

class TestBrowserControllerHandleCommand:
    def _make_browser(self):
        from modules.browser_controller import BrowserController
        bc = BrowserController()
        bc.google_search = AsyncMock(return_value=True)
        bc._ensure_page_alive = AsyncMock(return_value=True)
        bc.page = AsyncMock()
        return bc

    @pytest.mark.asyncio
    async def test_routes_search_for_to_google(self):
        bc = self._make_browser()
        await bc.handle_command("search for python tutorials")
        bc.google_search.assert_called_once()

    @pytest.mark.asyncio
    async def test_routes_google_prefix_to_google(self):
        bc = self._make_browser()
        await bc.handle_command("google the weather today")
        bc.google_search.assert_called_once()

    @pytest.mark.asyncio
    async def test_scroll_down(self):
        bc = self._make_browser()
        result = await bc.handle_command("scroll down")
        bc.page.mouse.wheel.assert_called_once_with(0, 900)
        assert result is True

    @pytest.mark.asyncio
    async def test_scroll_up(self):
        bc = self._make_browser()
        result = await bc.handle_command("scroll up")
        bc.page.mouse.wheel.assert_called_once_with(0, -900)
        assert result is True

    @pytest.mark.asyncio
    async def test_zoom_in(self):
        bc = self._make_browser()
        result = await bc.handle_command("zoom in")
        bc.page.evaluate.assert_called_once()
        assert result is True

    @pytest.mark.asyncio
    async def test_does_not_false_match_open_browser_as_zoom(self):
        """'open browser' contains 'in' — must not trigger zoom."""
        bc = self._make_browser()
        bc._ensure_page_alive = AsyncMock(return_value=False)
        result = await bc.handle_command("open browser")
        bc.page.evaluate.assert_not_called()

    @pytest.mark.asyncio
    async def test_returns_false_when_page_dead(self):
        bc = self._make_browser()
        bc._ensure_page_alive = AsyncMock(return_value=False)
        result = await bc.handle_command("scroll down")
        assert result is False

    @pytest.mark.asyncio
    async def test_unknown_command_returns_false(self):
        bc = self._make_browser()
        result = await bc.handle_command("do something weird")
        assert result is False
