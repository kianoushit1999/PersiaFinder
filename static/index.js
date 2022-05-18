'use strict';
AOS.init();
const inputSearch = document.querySelector('#input-search');
const btnSearch = document.querySelector('#btn-search');
const btnDelete = document.querySelector('#btn-delete');
const gearBtn = document.querySelector('.gear-btn');
const gearBtnIcon = document.querySelectorAll('.gear-btn-icon');
const hourglassIcon = document.querySelector('#hourglass');
const engineTime = document.querySelector('#engine-time');

btnSearch.addEventListener('click', () => {
    console.log('click');
    const token = inputSearch.value.split("AND").map((value) => {
        return value.trim()
    }).join(" ");
    fetch('http://127.0.0.1:5000/fetch-related-data', {
        method: 'POST',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
        }, body: JSON.stringify({
            "sentence": token
        })
    })
        .then(response => response.json())
        .then((data) => {
            console.log(data);
        })
})

btnDelete.addEventListener('click', () => {
    console.log('delete');
    inuptSearch.value = "";
})

gearBtn.addEventListener('click', () => {
    const tic = new Date().getTime()
    const interval = setInterval(() => {
        let toc = new Date().getTime();
        engineTime.textContent = `${parseFloat((toc - tic) / 1000).toFixed(0)}`
    }, 1000);
    console.log('gear');
    for (const obj of gearBtnIcon) {
        obj.classList.add("gear-animation");
    }
    hourglassIcon.classList.add("hourglass-animation");
    fetch("http://127.0.0.1:5000/start-engine")
        .then(response => response.json())
        .then((data) => {
            const {response} = data;
            if (response == "success") {
                for (const obj of gearBtnIcon) {
                    obj.classList.remove("gear-animation");
                }
                hourglassIcon.classList.remove("hourglass-animation");
                clearInterval(interval);
            }
        });
})
