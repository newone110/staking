//Get ETH Input box
const eth_input = document.getElementById("amount");
//Get BEC Input box
eth_result = document.getElementById("result");
//Add event listener to check for value change
eth_input.addEventListener("input", function () {
  // Do math to display converted value
  eth_result.value = eth_input.value * 511756;
});
