// print PDF
function printPDF() {
    const printAsPDF = document.body;
    html2pdf(printAsPDF);
    alert('You download this page');
}

// copy URL
function copyURL() {
    const getURL = document.location.href;

    const urlInput = document.createElement('input');
    urlInput.value = getURL;
    document.body.appendChild(urlInput);

    urlInput.select();
    urlInput.setSelectionRange(0, 99999);

    document.execCommand("copy");
    document.body.removeChild(urlInput);

    alert('URL copied to clipboard: ' + getURL);
}

// add to favorite
function addBookmark() {
    const icon = document.getElementById('heartIcon');

    if (icon.classList.contains('fa-regular')) {
        icon.classList.remove('fa-regular');
        icon.classList.add('fa-solid');
        alert('You added to bookmark');
    } else {
        icon.classList.remove('fa-solid');
        icon.classList.add('fa-regular');
        alert('You remove from bookmark')
    }
}