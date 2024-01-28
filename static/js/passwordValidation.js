document.addEventListener('DOMContentLoaded', function () {
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm-password');
    const passwordError = document.getElementById('password-error');

    confirmPasswordInput.addEventListener('input', function () {
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;

        if (password !== confirmPassword) {
            passwordError.textContent = 'Password does not match';
            passwordError.style.color = 'red';
        } else {
            passwordError.textContent = 'Password match';
            passwordError.style.color = 'green';
        }
        
    });

    const form = document.querySelector('form');
    form.addEventListener('submit', function (event) {
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;

        if (password !== confirmPassword) {
            passwordError.textContent = 'Password does not match';
            passwordError.style.color = 'red';
            event.preventDefault();
        } else {
            passwordError.textContent = 'Password match';
            passwordError.style.color = 'green';
            alert('You successfully created an account. Please log in');
        }
    });
});
