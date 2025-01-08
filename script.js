let currentIndex = 0;

function showSlide(index) {
    const slides = document.querySelectorAll('.carousel-images img');
    if (index >= slides.length) {
        currentIndex = 0;
    } else if (index < 0) {
        currentIndex = slides.length - 1;
    } else {
        currentIndex = index;
    }

    slides.forEach((slide, i) => {
        slide.classList.remove('active');
        if (i === currentIndex) {
            slide.classList.add('active');
        }
    });
}

function moveSlide(direction) {
    showSlide(currentIndex + direction);
}

// Initialize the first slide
showSlide(currentIndex);

// Automatic slide change every 5 seconds
setInterval(() => {
    moveSlide(1); // Move to the next slide
}, 3000); // 2000 milliseconds = 2 seconds