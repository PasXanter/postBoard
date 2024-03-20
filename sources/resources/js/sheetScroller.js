function scrollSheet(offset = 0) {
    const sheetIndex = Number(localStorage.getItem("sheetIndex")) ?? 0,
    sheets = document.querySelectorAll("main > section > ol > li");

    offset = Number(offset);

    if(0 <= sheetIndex + offset && sheetIndex + offset < sheets.length) {
        sheets[sheetIndex].style.display = "none";
        sheets[sheetIndex + offset].style.display = "inline-flex";

        localStorage.setItem("sheetIndex", String(sheetIndex + offset));
    };
};

window.addEventListener("load", (event) => {
    scrollSheet();

    document.querySelectorAll("main > section > aside > nav > button").forEach((element, index) => {
        element.addEventListener("click", (event) => {
            scrollSheet(element.value);
        });
    });
});