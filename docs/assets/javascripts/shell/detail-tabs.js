(function () {
  const shell = (window.bijuxShell = window.bijuxShell || {});

  function syncDetailStripPresence() {
    const header = document.querySelector("[data-md-component='header']");
    if (!header) {
      return;
    }
    const hasVisibleDetailStrip = document.querySelector("[data-bijux-detail-strip]");
    header.setAttribute(
      "data-bijux-detail-visible",
      hasVisibleDetailStrip ? "true" : "false"
    );
  }

  function syncDetailStripActiveState() {
    const navState = shell.navState;
    if (!navState) {
      return;
    }

    const currentPath = navState.normalizePath(window.location.pathname);
    const strips = document.querySelectorAll("[data-bijux-detail-strip]");

    for (const strip of strips) {
      const authoredActiveLink = strip.querySelector(
        "a[data-bijux-detail-path][aria-current='page'], .bijux-tabs__item--active a[data-bijux-detail-path]"
      );

      for (const item of strip.querySelectorAll(".bijux-tabs__item")) {
        item.classList.remove("bijux-tabs__item--active");
      }

      for (const link of strip.querySelectorAll("a[data-bijux-detail-path]")) {
        link.removeAttribute("aria-current");
      }

      const matchedLink = navState.bestMatchingLink(
        strip,
        "data-bijux-detail-path",
        currentPath,
        "a[data-bijux-detail-path]"
      );

      let activeLink = matchedLink;

      if (!activeLink && authoredActiveLink) {
        activeLink = {
          path: navState.normalizePath(
            authoredActiveLink.getAttribute("data-bijux-detail-path") || "/"
          ),
          node: authoredActiveLink,
        };
      }

      if (!activeLink) {
        const parentPath = navState.normalizePath(
          strip.getAttribute("data-bijux-detail-root-path") || "/"
        );
        const homeLink = strip.querySelector(
          `a[data-bijux-detail-path="${parentPath}"]`
        );
        if (homeLink) {
          activeLink = {
            path: parentPath,
            node: homeLink,
          };
        }
      }

      if (!activeLink) {
        const firstLink = strip.querySelector("a[data-bijux-detail-path]");
        if (firstLink) {
          activeLink = {
            path: navState.normalizePath(
              firstLink.getAttribute("data-bijux-detail-path") || "/"
            ),
            node: firstLink,
          };
        }
      }

      if (activeLink) {
        activeLink.node
          .closest(".bijux-tabs__item")
          ?.classList.add("bijux-tabs__item--active");
        activeLink.node.setAttribute("aria-current", "page");
      }
    }
  }

  function bindDetailSelectNavigation() {
    for (const select of document.querySelectorAll("[data-bijux-detail-select]")) {
      if (select.dataset.bijuxDetailSelectBound === "true") {
        continue;
      }

      select.dataset.bijuxDetailSelectBound = "true";
      select.addEventListener("change", () => {
        if (!select.value) {
          return;
        }
        window.location.href = select.value;
      });
    }
  }

  function syncDetailSelectState() {
    const navState = shell.navState;
    if (!navState) {
      return;
    }

    const strips = document.querySelectorAll("[data-bijux-detail-strip]");

    for (const strip of strips) {
      const activeLink = strip.querySelector(
        "a[data-bijux-detail-path][aria-current='page']"
      );

      if (!activeLink) {
        continue;
      }

      const activePath = navState.normalizePath(
        activeLink.getAttribute("data-bijux-detail-path") || "/"
      );

      const select = strip.querySelector("[data-bijux-detail-select]");
      if (!select) {
        continue;
      }

      for (const option of select.options) {
        const optionPath = navState.normalizePath(
          option.getAttribute("data-bijux-detail-path") || option.value || "/"
        );
        option.selected = optionPath === activePath;
      }
    }
  }

  function runDetailTabsSync() {
    syncDetailStripPresence();
    syncDetailStripActiveState();
    syncDetailSelectState();
    bindDetailSelectNavigation();
  }

  shell.detailTabs = {
    syncDetailStripPresence,
    syncDetailStripActiveState,
    syncDetailSelectState,
    bindDetailSelectNavigation,
    runDetailTabsSync,
  };
})();
