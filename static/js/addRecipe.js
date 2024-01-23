function previewImage(event) {
    const input = event.target;
        const preview = document.getElementById('imagePreview');

        if (input.files && input.files[0]) {
            const reader = new FileReader();

            reader.onload = function (e) {
                preview.src = e.target.result;
            };

        reader.readAsDataURL(input.files[0]);
        } else {
            preview.src = '';
    }
}

function characterCount() {
    let maxCount = 100;
    let descInput = document.getElementById('desc');
    let charCount = document.getElementById('charCount');

    let remainingCharacter = maxCount - descInput.value.length;
    charCount.textContent = remainingCharacter + " / " + maxCount; 
}

function addIngredient() {
    const container = document.getElementById('ingredientContainer');
    const newInput = document.createElement('input');
    newInput.type = 'text';
    newInput.name = 'newInputs[]';
    newInput.placeholder = 'Add Ingredients';
    newInput.maxLength = 100;

    container.appendChild(newInput);
    container.appendChild(document.createElement('br'));
}

function addInstruction() {
    const container = document.querySelector('.instructionContainer');

    // new div for each step
    const newStepDiv = document.createElement('div');

    // new label
    const newLabel = document.createElement('span');
    newLabel.style.fontSize = '18px';
    newLabel.innerHTML = 'Step ' + (container.children.length + 1) + ':';

    // new input
    const newInput = document.createElement('input');
    newInput.type = 'text';
    newInput.name = 'newInputs[]';
    newInput.placeholder = 'Add Instruction';

    // append label and input to new div
    newStepDiv.appendChild(newLabel);
    newStepDiv.appendChild(newInput);

    // append new div to container
    container.appendChild(newStepDiv);
}



function browseButton() {
    document.getElementById('browseButton').addEventListener('click', function () {
            document.getElementById('addImage').click();
        });
}