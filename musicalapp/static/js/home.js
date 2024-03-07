document.addEventListener("DOMContentLoaded", function () {
  let currentIndex = 0;
  const items = document.querySelectorAll(".carousel-item");

  function showItem(index) {
    const carouselInner = document.querySelector(".carousel-inner");
    const itemWidth = items[0].offsetWidth; // Ancho de un elemento
    carouselInner.style.transform = `translateX(-${index * itemWidth}px)`;
  }

  function nextItem() {
    currentIndex++;
    if (currentIndex >= items.length) {
      currentIndex = 0;
    }
    showItem(currentIndex);
  }

  setInterval(nextItem, 3000); // Cambia de imagen cada 3 segundos
});
