window.onload = function () {
const apiForm = document.getElementById('apiForm');

apiForm.onsubmit = async (e) => {
    e.preventDefault();
    await fetch("/api/submit", {
        method: 'POST',
        body: new FormData(apiForm)
        }
    );
}
};