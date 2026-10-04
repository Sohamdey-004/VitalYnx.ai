(() => {
  const expectedConnected = document.body.dataset.deviceConnected === 'true';
  const check = async () => {
    try {
      const response = await fetch('/api/device-status', {
        cache: 'no-store',
        headers: { Accept: 'application/json' },
      });
      if (!response.ok) return;
      const status = await response.json();
      if (status.connected !== expectedConnected) window.location.reload();
    } catch (_) {
      // Keep the current page when the network is temporarily unavailable.
    }
  };

  check();
  window.setInterval(check, 5000);
})();
