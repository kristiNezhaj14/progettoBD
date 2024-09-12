document.addEventListener('DOMContentLoaded', () => {

    function showWelcomeMessage(userName) {
        userNameSpan.textContent = userName;
        loginForm.style.display = 'none';
        welcomeMessage.style.display = 'block';
    }

    let currentIndex = 0;
    const items = document.querySelectorAll('.carousel-item');
    const totalItems = items.length;

    document.querySelector('.next').addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % totalItems;
        updateCarousel();
    });

    document.querySelector('.prev').addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + totalItems) % totalItems;
        updateCarousel();
    });

    function updateCarousel() {
        const newTransform = `translateX(-${currentIndex * 100}%)`;
        document.querySelector('.carousel-inner').style.transform = newTransform;
    }
});