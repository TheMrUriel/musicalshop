var calcSubTotal = function (element) {
  var itemPrice = $(element).find(".price").text().substring(1);
  var itemQuantity = parseFloat($(element).find(".quantity input").val());
  if (isNaN(itemQuantity)) {
    itemQuantity = 0;
  }
  var subTotal = itemPrice * itemQuantity;
  return subTotal;
};
var updateSubTotal = function (element) {
  var prices = [];
  $("tbody tr").each(function (index, element) {
    var subTotal = parseFloat(calcSubTotal(element));
    prices.push(subTotal);
    $(element)
      .children(".subTotal")
      .html("$" + subTotal.toFixed(2));
  });
  console.log(prices);
  return prices;
};
var sum = function (total, num) {
  return total + num;
};
const updateCartTotal = () => {
  const subTotal = updateSubTotal();
  const cartTotal = subTotal.reduce((acc, val) => acc + val, 0).toFixed(2);
  $("#cartTotal").html(cartTotal);
};
$(document).ready(function () {
  updateCartTotal();
  var timeout;

  $(document).on("input", "tr input", function () {
    clearTimeout(timeout);
    timeout = setTimeout(function () {
      updateCartTotal();
    }, 800);
  });

  $(document).on("click", ".btn.remove", function (event) {
    $(this).closest("tr").remove();
    updateCartTotal();
  });

  // Change the selector to use the class "add-to" for the click event
  $(document).on("click", ".add-to", function (event) {
    // Use the correct form selector
    var item = $("#addItem [name=itemName]").val();
    var price = parseFloat($("#addItem [name=price]").val()).toFixed(2);

    $("tbody").append(
      `<tr>
                <td class="item font-weight-bold">${item}</td>
               	<td class="price text-center">$${price}</td>
               			<td class="quantity">
                    <input
												class="effect text-center"
												type="number"
												value="0"
												min="0"
											/>
											<span class="focus-border"> </span>
										</td>
              		<td class="subTotal text-center"></td>
										<td>
											<button class="btn btn-sm remove">
												Remove <i class="fa fa-trash mb-1 p-4 text-danger"></i>
											</button>
										</td>`
    );

    updateCartTotal();
    $("#addItem [name=itemName]").val("");
    $("#addItem [name=price]").val("");
  });
});
