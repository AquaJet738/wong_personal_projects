// Check if it's an Amazon product page
function isAmazonProductPage() {
  return window.location.pathname.includes("/dp/");
}

// Only run this script if it's an Amazon product page
if (isAmazonProductPage()) {
  console.log('Content script has loaded.');

  // Inject CSS for styling
  var link = document.createElement('link');
  link.href = chrome.runtime.getURL('styles.css');
  link.type = 'text/css';
  link.rel = 'stylesheet';
  document.head.appendChild(link);

  // Create the initial small button
  var button = document.createElement('button');
  button.textContent = "Click me";
  button.id = "my-extension-button";
  button.style.cssText = `
    position: fixed; right: 10px; bottom: 10px;
    transform: translateY(-50%); background-color: green;
    color: white; padding: 10px; font-size: 16px;
    cursor: pointer; z-index: 10000; border: none;
    border-right: 5px solid darkgreen;
  `;

  // Placeholder data - simulate an API response
  const products = [
    {
      name: "PURA D'OR Original Gold Label Anti-Thinning Biotin Shampoo",
      price: "$28.49",
      rating: "4.3/5",
      image: "https://m.media-amazon.com/images/I/71cFWxqUicL._SY355_.jpg"
    },
    {
      name: "Mielle Organics Rosemary Mint Strengthening Shampoo",
      price: "$9.97",
      rating: "4.5/5",
      image: "https://m.media-amazon.com/images/I/61YSg1spuxL._SX466_.jpg"
    }
  ];

  // Add event listener for click to expand/collapse the UI directly
  let isExpanded = false;
  button.addEventListener('click', function() {
    if (!isExpanded) {
      // Expand to show detailed UI
      button.textContent = "Close";
      button.style.width = "300px"; // Expanded width
      button.style.height = "auto"; // Adjust height as needed
      button.style.backgroundColor = "#ccc"; // Change color when expanded
      button.innerHTML = `<strong>Ecofriendly results for xxxxxx</strong>`;
      products.forEach(product => {
        button.innerHTML += `
          <div class="product">
            <img class="product-image" src="${product.image}" style="width:50px; height:50px;">
            <div class="product-info">
              <p class="product-name">${product.name}</p>
              <p class="product-price">${product.price}</p>
              <p class="product-rating">${product.rating}</p>
            </div>
          </div>
        `;
      });
      button.innerHTML += '<button onclick="this.parentElement.style.display=\'none\';">See More Results</button>';
      isExpanded = true;
    } else {
      // Collapse to original small button
      button.textContent = "Click me";
      button.style.width = "auto";
      button.style.height = "auto";
      button.style.backgroundColor = "green";
      isExpanded = false;
    }
  });

  document.body.appendChild(button);
  console.log('Button injected');
}
