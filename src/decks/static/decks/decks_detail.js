let slideIndex = 1;

(function() {
  changeSlide(0);
  
  const cards = document.getElementsByClassName('card-frame');
  for(let i=0; i<cards.length; i++) {
    cards[i].addEventListener("click", function() {
      this.classList.toggle('flipped');
    });
  }
})();

/* FUNCTIONS */
function changeSlide(n) {
  showSlides(slideIndex += n);
  let e = document.getElementById('slideIndex');
  e.innerHTML = slideIndex;
}

function showSlides(n) {
  const slides = document.getElementsByClassName("card");
  if(n < 0) slideIndex = slides.length;
  if(n > slides.length) slideIndex = 1;
  
  for (let i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  slides[slideIndex-1].style.display = "block";
}
