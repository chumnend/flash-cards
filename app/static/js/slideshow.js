var slideIndex = 1;
changeSlide(0);

function changeSlide(n) {
    showSlides(slideIndex += n);
    
    let e = document.getElementById("slideIndex")
    e.innerHTML = slideIndex;
}

function showSlides(n) {
    var i;
    var slides = document.getElementsByClassName("card");

    if (n > slides.length) {
        slideIndex = 1
    }

    if (n < 1) {
        slideIndex = slides.length
    }

    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }

    slides[slideIndex-1].style.display = "block"; 
} 

// CARD =====================================================
var cards = document.getElementsByClassName('card-frame');
for(let i=0; i<cards.length; i++) {
    cards[i].addEventListener("click", function() {
        this.classList.toggle('flipped');
    });
}
