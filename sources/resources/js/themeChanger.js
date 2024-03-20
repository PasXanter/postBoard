function changeTheme(themeColor = localStorage.getItem("themeColor") ?? "system") {
    document.documentElement.setAttribute("data-themeColor", themeColor == "system" ? (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light") : themeColor);

    localStorage.setItem("themeColor", themeColor);
};

window.addEventListener("load", (event) => {
    changeTheme();

    const selector = document.querySelector("header > section > select[name = 'theme']");

    selector.addEventListener("change", (event) => {
        changeTheme(selector.value);
    });
});

window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (event) => {
    changeTheme();
});