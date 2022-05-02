window.onload = function () {
    const apiForm = document.getElementById('apiForm');

    apiForm.onsubmit = async (e) => {
        e.preventDefault();
        const resp = await fetch("/api/submit", {
            method: 'POST',
            body: new FormData(apiForm)
            }
        );
        if (resp.status !== 200) {
            // const responseJson =
            alert((await resp.json()).error)
        } else {
            apiForm.reset()
        }
    }
};