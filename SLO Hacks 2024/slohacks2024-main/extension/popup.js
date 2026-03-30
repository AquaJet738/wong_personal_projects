document.addEventListener("DOMContentLoaded", () => {
  fetch("http://127.0.0.1:5000/scrape")
    .then(response => response.json())
    .then(data => {
      const productList = document.getElementById("product-list");
      data.forEach(product => {
        let productElement = document.createElement('div');
        productElement.className = 'product';
        productElement.innerHTML = `
          <img class="product-image" src="${product.image}" />
          <div class="product-info">
            <h3 class="product-name">${product.name}</h3>
            <div class="product-details">
              <p class="product-price">${product.price}</p>
              <p class="product-rating">${product.rating}/5</p>
            </div>
          </div>
        `;
        productList.appendChild(productElement);
      });
    })
    .catch(error => console.error('Error:', error));
});

