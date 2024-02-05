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

function addBookmark() {
    const form = document.getElementById('bookmarkForm');
    form.submit();
    alert('Recipe already sent to your email')
}





