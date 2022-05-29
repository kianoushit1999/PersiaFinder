'use strict';
AOS.init();
const inputSearch = document.querySelector('#input-search');
const btnSearch = document.querySelector('#btn-search');
const btnDelete = document.querySelector('#btn-delete');
const gearBtn = document.querySelector('.gear-btn');
const gearBtnIcon = document.querySelectorAll('.gear-btn-icon');
const hourglassIcon = document.querySelector('#hourglass');
const engineTime = document.querySelector('#engine-time');
const totalResult = document.querySelector('.summary');
const numberOne = document.querySelector('#number--1');
const numberTwo = document.querySelector('#number--2');
const numberThree = document.querySelector('#number--3');
const numberFour = document.querySelector('#number--4');
const numberFive = document.querySelector('#number--5');
const contentList = document.querySelector('#content-list');

let indexList = []

const manipulateDom = (objectList) => {
    contentList.innerHTML = ""
    objectList.map((value, index, array) => {
        contentList.innerHTML += `
        <div class="col-6 offset-6" data-aos="fade-up-left">
          <article class="custom-card">
            <header><a href="https://google.com">${value["doc_url"]}</a></header>
            <h1 style="font-size: 2rem" >${value["doc_title"]}</h1>
            <div style="font-size: 1.5rem">
              ${value["doc_body"].substring(0, 150)} ...
            </div>
          </article>
        </div>
        `
    })
}


const fetch_page_content = (list) => {
    fetch('http://127.0.0.1:5000/fetch-page', {
        method: 'POST',
        headers: {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json'
        }, body: JSON.stringify({
            "listContent": list
        })
    })
        .then(response => response.json())
        .then((data) => {
            manipulateDom(data.content)
        });
}


btnSearch.addEventListener('click', () => {
    console.log('click');
    const tic = new Date().getTime()
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
            indexList = data.list;
            let content = data.content;
            let toc = new Date().getTime();
            console.log(content)
            console.log(indexList);
            totalResult.textContent = `Time : (${parseFloat((toc - tic))}ms)`;
            manipulateDom(content)
            console.log(indexList.slice(0, 10));
        });
});

btnDelete.addEventListener('click', () => {
    console.log('delete');
    inputSearch.value = "";
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
numberOne.addEventListener('click', () => {
    numberOne.textContent = +numberOne.textContent - 1;
    numberTwo.textContent = +numberOne.textContent + 1;
    numberThree.textContent = +numberTwo.textContent + 1;
    numberFour.textContent = +numberThree.textContent + 1;
    numberFive.textContent = +numberFour.textContent + 1;
    console.log(numberOne.textContent)
    let startNumber = (+numberOne.textContent - 1) * 10
    let newList = indexList.slice(startNumber, startNumber + 10)
    fetch_page_content(newList);
});

numberTwo.addEventListener('click', () => {
    numberOne.textContent = numberTwo.textContent;
    numberTwo.textContent = numberThree.textContent;
    numberThree.textContent = numberFour.textContent;
    numberFour.textContent = numberFive.textContent;
    numberFive.textContent = +numberFive.textContent + 1;
    let startNumber = (+numberOne.textContent - 1) * 10
    let newList = indexList.slice(startNumber, startNumber + 10)
    console.log(newList)
    fetch_page_content(newList);
});

numberThree.addEventListener('click', () => {
    numberOne.textContent = numberThree.textContent;
    numberTwo.textContent = numberFour.textContent;
    numberThree.textContent = numberFive.textContent;
    numberFour.textContent = +numberFive.textContent + 1;
    numberFive.textContent = +numberFive.textContent + 2;
    console.log(numberOne.textContent)
    let startNumber = (+numberOne.textContent - 1) * 10
    let newList = indexList.slice(startNumber, startNumber + 10)
    console.log(newList)
    fetch_page_content(newList);
});

numberFour.addEventListener('click', () => {
    numberOne.textContent = numberFour.textContent;
    numberTwo.textContent = numberFive.textContent;
    numberThree.textContent = +numberFive.textContent + 1;
    numberFour.textContent = +numberFive.textContent + 2;
    numberFive.textContent = +numberFive.textContent + 3;
    console.log(numberOne.textContent)
    let startNumber = (+numberOne.textContent - 1) * 10
    let newList = indexList.slice(startNumber, startNumber + 10)
    console.log(newList)
    fetch_page_content(newList);
});
numberFive.addEventListener('click', () => {
    numberOne.textContent = numberFive.textContent;
    numberTwo.textContent = +numberFive.textContent + 1;
    numberThree.textContent = +numberFive.textContent + 2;
    numberFour.textContent = +numberFive.textContent + 3;
    numberFive.textContent = +numberFive.textContent + 4;
    console.log(numberOne.textContent)
    let startNumber = (+numberOne.textContent - 1) * 10
    let newList = indexList.slice(startNumber, startNumber + 10)
    console.log(newList)
    fetch_page_content(newList);
});
