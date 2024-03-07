document.addEventListener("DOMContentLoaded", function () {
  const qtyMinusBtn = document.querySelector("[data-qty-minus]");
  const qtyPlusBtn = document.querySelector("[data-qty-plus]");
  const qtyDisplay = document.querySelector("[data-qty]");

  // Función para aumentar la cantidad del producto
  qtyPlusBtn.addEventListener("click", function () {
    let qty = parseInt(qtyDisplay.textContent);
    qty++;
    qtyDisplay.textContent = qty;
  });

  // Función para disminuir la cantidad del producto
  qtyMinusBtn.addEventListener("click", function () {
    let qty = parseInt(qtyDisplay.textContent);
    if (qty > 1) {
      qty--;
      qtyDisplay.textContent = qty;
    }
  });
});
