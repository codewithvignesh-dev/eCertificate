document.addEventListener("DOMContentLoaded", () => {
    const shell = document.querySelector(".app-shell");
    const sidebar = document.querySelector("[data-sidebar]");
    const sidebarToggle = document.querySelector("[data-sidebar-toggle]");
    const sidebarClose = document.querySelector("[data-sidebar-close]");
    const sidebarOverlay = document.querySelector("[data-sidebar-overlay]");

    const isOpen = () => sidebar?.classList.contains("is-open");

    const openSidebar = () => {
        if (!sidebar || !shell) return;

        sidebar.classList.add("is-open");
        sidebarOverlay?.classList.add("is-open");
        shell.classList.add("is-sidebar-open");
        sidebarToggle?.setAttribute("aria-expanded", "true");
        document.body.classList.add("overflow-hidden");
    };

    const closeSidebar = () => {
        if (!sidebar || !shell) return;

        sidebar.classList.remove("is-open");
        sidebarOverlay?.classList.remove("is-open");
        shell.classList.remove("is-sidebar-open");
        sidebarToggle?.setAttribute("aria-expanded", "false");
        document.body.classList.remove("overflow-hidden");
    };

    const toggleSidebar = () => {
        if (isOpen()) {
            closeSidebar();
        } else {
            openSidebar();
        }
    };

    closeSidebar();

    sidebarToggle?.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        toggleSidebar();
    });

    sidebarClose?.addEventListener("click", (event) => {
        event.preventDefault();
        closeSidebar();
    });

    sidebarOverlay?.addEventListener("click", closeSidebar);

    document.querySelectorAll("[data-sidebar] a").forEach((link) => {
        link.addEventListener("click", () => {
            closeSidebar();
        });
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && isOpen()) {
            closeSidebar();
        }
    });

    document.querySelectorAll("[data-dismiss]").forEach((element) => {
        element.addEventListener("click", () => {
            element.closest("[data-dismissible]")?.remove();
        });
    });

    document.querySelectorAll("[data-auto-dismiss]").forEach((element) => {
        const delay = Number(element.dataset.autoDismiss) || 5000;

        setTimeout(() => {
            element.classList.add("is-hidden");

            setTimeout(() => {
                element.remove();
            }, 300);
        }, delay);
    });

    document.querySelectorAll("form[data-confirm]").forEach((form) => {
        form.addEventListener("submit", (event) => {
            const message = form.dataset.confirm || "Are you sure you want to continue?";

            if (!window.confirm(message)) {
                event.preventDefault();
            }
        });
    });

    document.querySelectorAll("[data-password-toggle]").forEach((button) => {
        button.addEventListener("click", () => {
            const targetId = button.dataset.passwordToggle;
            const input = document.getElementById(targetId);

            if (!input) return;

            input.type = input.type === "password" ? "text" : "password";

            button.setAttribute(
                "aria-label",
                input.type === "password" ? "Show password" : "Hide password"
            );
        });
    });

    document.documentElement.classList.add("ui-ready");

    document.querySelectorAll(
        'a[class*="bg-"],button[class*="bg-"],input[type="submit"]'
    ).forEach((element) => {
        element.addEventListener("pointerdown", () => {
            element.classList.add("ui-pressed");

            window.setTimeout(() => {
                element.classList.remove("ui-pressed");
            }, 180);
        });
    });

    const revealItems = document.querySelectorAll(
        "main .rounded-2xl, main .rounded-3xl, main section"
    );

    if ("IntersectionObserver" in window && revealItems.length) {
        const observer = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("ui-visible");
                        observer.unobserve(entry.target);
                    }
                });
            },
            {
                threshold: 0.08
            }
        );

        revealItems.forEach((element) => {
            element.classList.add("ui-reveal");
            observer.observe(element);
        });
    }
});