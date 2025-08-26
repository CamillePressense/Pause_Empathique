document.addEventListener('DOMContentLoaded', function() {
    const toggleButtons = document.querySelectorAll('.toggle-password');
    
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const passwordField = this.parentElement.querySelector('input[type="password"], input[type="text"]');
            const eyeIcon = this.querySelector('.eye-icon');
            
            if (passwordField.type === 'password') {
                passwordField.type = 'text';
                eyeIcon.textContent = '🙈';
                this.setAttribute('aria-label', 'Masquer le mot de passe');
            } else {
                passwordField.type = 'password';
                eyeIcon.textContent = '👁️';
                this.setAttribute('aria-label', 'Afficher le mot de passe');
            }
        });
    });
});