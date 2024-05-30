let dataFile = []
let currentItemIdx = undefined
const reviewLabels = {
    1: "Переделать полностью",
    2: "Пойдёт, если поправить",
    3: "Хорошо"
}

function initUploader() {
    const uploaderTemplate = document.getElementById('uploader');

    const uploader = document.importNode(uploaderTemplate.content, true);

    uploader.querySelector("#start-btn").addEventListener("click", readJSON)

    document.body.appendChild(uploader);
}

function readJSON() {
            const fileInput = document.getElementById('dataFile');
            const file = fileInput.files[0];

            if (file) {
                const reader = new FileReader();

                reader.onload = (event) => {
                    try {
                        const jsonObject = JSON.parse(event.target.result);
                        dataFile = jsonObject
                        currentItemIdx = 0
                        renderMainLayout()
                    } catch (e) {
                        console.error("Ошибка при чтении JSON:", e);
                    }
                };
                reader.readAsText(file);
            } else {
                console.error("Файл не выбран.");
            }
        }

function exportToJsonFile(data, filename) {
    const jsonData = JSON.stringify(data, null, 2);

    const blob = new Blob([jsonData], { type: 'application/json' });

    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = filename || 'data.json'; // Имя файла по умолчанию - data.json

    document.body.appendChild(a);
    a.click();

    document.body.removeChild(a);
}

function renderMainLayout() {
        const uploadLayout = document.querySelector('body > #upload-layout')
        if(uploadLayout) document.body.removeChild(uploadLayout);

        const editorLayout = document.querySelector('body > #editor-layout')
        if(editorLayout) document.body.removeChild(editorLayout);

        const controlsTemplate = document.getElementById('main-controls');
        const controls = document.importNode(controlsTemplate.content, true);
        document.body.appendChild(controls);

        const {character, meaning, mnemonic, status} =  dataFile[currentItemIdx]

        const mainControls = document.querySelector("#editor-layout")

        
        // LABEL
        const labelTag = mainControls.querySelector(".label")
        if (status) {
            labelTag.textContent =  reviewLabels[status.toString()]
            labelTag.setAttribute('data-value', status);
        } else {
            mainControls.removeChild(labelTag)
        }

        // CHARACTER
        const characterTag = mainControls.querySelector(".character")
        const characterImageTag = mainControls.querySelector(".character.image")

        if(character.length > 1) {
            characterImageTag.src = character
            mainControls.removeChild(characterTag)
        } else {
            characterTag.textContent = character
            mainControls.removeChild(characterImageTag)
        }


        // TRANSLATION
        const translationTag = mainControls.querySelector(".translation")
        translationTag.value = meaning

        translationTag.addEventListener("input", (e) => {
            dataFile[currentItemIdx].meaning = e.target.value
        })


        // MNEMONIC
        const mnemonicTag = mainControls.querySelector(".mnemonic")
        mnemonicTag.value = mnemonic

        mnemonicTag.addEventListener("input", (e) => {
            dataFile[currentItemIdx].mnemonic = e.target.value
        })


        // REVIEW CONTROLS
        const reviewControls = mainControls.querySelectorAll(".controls > button")
        reviewControls.forEach(button => {
            button.addEventListener("click", (e) => {
                dataFile[currentItemIdx].status = Number(e.target.value)
                renderMainLayout()
            })
        })

        // NAVIGATION CONTROLS
        const backBtn = mainControls.querySelector("#back")
        const forwardBtn = mainControls.querySelector("#forward")
        const jumpBtn = mainControls.querySelector("#jump")

        backBtn.addEventListener("click", () => {
            currentItemIdx = Math.max(0, currentItemIdx - 1)
            renderMainLayout()
        })

        forwardBtn.addEventListener("click", () => {
            currentItemIdx = Math.min(dataFile.length-1, currentItemIdx + 1)
            renderMainLayout()
        })

        itemNumberInput = mainControls.querySelector(".jump > input")
        itemNumberInput.value = currentItemIdx

        itemNumberInput.addEventListener("input", (e) => {
            if(e.target.value > dataFile.length-1) {
                itemNumberInput.value = dataFile.length-1
            } else if (e.target.value < 0) {
                itemNumberInput.value = 0
            } else {
                itemNumberInput.value = e.target.value
            }
        })

        jumpBtn.addEventListener("click", () => {
            currentItemIdx = itemNumberInput.value
            renderMainLayout()
        })


        // EXPORT CONTROLS
        const exportBtn = mainControls.querySelector("#export")
        exportBtn.addEventListener("click", () => {
            exportToJsonFile(dataFile, "radicals_out.json")
        })

}

initUploader()