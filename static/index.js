'use strict';
AOS.init();
const inuptSearch = document.querySelector('#input-search');
const btnSelect = document.querySelector('#btn-search');
const btnDelete = document.querySelector('#btn-delete');
const gearBtn = document.querySelector('.gear-btn');
const gearBtnIcon = document.querySelectorAll('.gear-btn-icon');
const hourglassIcon = document.querySelector('#hourglass');

btnSelect.addEventListener('click', ()=>{
    console.log('click');
})

btnDelete.addEventListener('click', ()=>{
    console.log('delete');
    inuptSearch.value = "";
})

gearBtn.addEventListener('click', ()=>{
    console.log('gear');
    for (const obj of gearBtnIcon) {
        obj.classList.toggle("gear-animation")
    }
    hourglassIcon.classList.toggle("hourglass-animation")
})
