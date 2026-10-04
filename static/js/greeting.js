(() => {
  const greeting = document.querySelector('[data-time-greeting]');
  const updateGreeting = () => {
    if (!greeting) return;
    const hour = new Date().getHours();
    greeting.textContent = hour >= 12 && hour < 17
      ? 'Good Afternoon'
      : hour >= 17 || hour < 4
        ? 'Good Evening'
        : 'Good Morning';
  };

  document.querySelectorAll('time[data-local-datetime]').forEach((element) => {
    const date = new Date(element.dateTime);
    if (!Number.isNaN(date.getTime())) {
      element.textContent = new Intl.DateTimeFormat(undefined, {
        day: '2-digit', month: 'short', year: element.dateTime.length > 16 ? 'numeric' : undefined,
        hour: '2-digit', minute: '2-digit', hour12: false,
      }).format(date);
      element.title = date.toLocaleString();
    }
  });

  updateGreeting();
  if (greeting) window.setInterval(updateGreeting, 60_000);
})();
