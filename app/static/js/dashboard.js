document.addEventListener("DOMContentLoaded", () => {
    const refreshButtons = document.querySelectorAll("[data-dashboard-refresh]");
    const autoRefresh = document.querySelector("[data-dashboard-auto-refresh]");
    const refreshInterval = Number(
        autoRefresh?.dataset.dashboardAutoRefresh || 0
    );

    refreshButtons.forEach((button) => {
        button.addEventListener("click", () => {
            button.disabled = true;
            window.location.reload();
        });
    });

    if (refreshInterval > 0) {
        window.setInterval(() => {
            if (document.visibilityState === "visible") {
                window.location.reload();
            }
        }, refreshInterval);
    }

    document.querySelectorAll("[data-stat-value]").forEach((element) => {
        const target = Number(element.dataset.statValue);

        if (!Number.isFinite(target) || target < 0) {
            return;
        }

        const duration = 500;
        const start = performance.now();

        const animate = (currentTime) => {
            const progress = Math.min(
                (currentTime - start) / duration,
                1
            );

            const value = Math.floor(target * progress);
            element.textContent = value.toLocaleString();

            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };

        requestAnimationFrame(animate);
    });
});