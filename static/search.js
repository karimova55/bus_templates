document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("searchInput");
    const rows = document.querySelectorAll("#timetable tbody tr");

    input.addEventListener("keyup", function () {
        const filter = input.value.toLowerCase();
        rows.forEach(row => {
            const subject = row.cells[2].textContent.toLowerCase();
            row.style.display = subject.includes(filter) ? "" : "none";
        });
    });
});