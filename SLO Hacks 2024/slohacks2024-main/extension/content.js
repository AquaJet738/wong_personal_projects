// Check if it's an Amazon product page
function isAmazonProductPage() {
    return window.location.pathname.includes("/dp/");
}
const tailwindLink = document.createElement('link');
tailwindLink.href = 'https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css';
tailwindLink.rel = 'stylesheet';
document.head.appendChild(tailwindLink);
// Global variable to store recommendations
let recommendations = [];

// Only run this script if it's an Amazon product page
if (isAmazonProductPage()) {
    console.log('Content script has loaded on an Amazon product page.');

    // Inject CSS for styling
    const link = document.createElement('link');
    link.href = chrome.runtime.getURL('styles.css');
    link.type = 'text/css';
    link.rel = 'stylesheet';
    document.head.appendChild(link);

    // Create the initial small button
    const button = document.createElement('button');
    button.textContent = "Get eco-friendly recommendations";
    button.id = "my-extension-button";
    button.style.cssText = `
      position: fixed; right: 10px; bottom: 10px;
      transform: translateY(-50%); background-color: green;
      color: white; padding: 10px; font-size: 16px;
      cursor: pointer; z-index: 10000; border: none;
      border-right: 5px solid darkgreen;
    `;
    document.body.appendChild(button);

    // Fetch recommendations when the page is loaded
    fetchRecommendations();

    // Toggle UI display on button click
    button.addEventListener('click', function() {
        if (!button.classList.contains('expanded')) {
            displayRecommendations(button);
            button.classList.add('expanded');
        } else {
            collapseUI(button);
            button.classList.remove('expanded');
        }
    });
}

// Assuming this is the correct function name and implementation you intended to use:
async function fetchImageDetailsForTopRecommendation(topRecommendation) {
    const response = await fetch('http://127.0.0.1:5000/getimage', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_url: topRecommendation.url })
    });
    if (!response.ok) throw new Error('Failed to fetch image details');
    return await response.json();
}

// Then in fetchRecommendations, replace fetchImageUrlForTopRecommendation with fetchImageDetailsForTopRecommendation:
async function fetchRecommendations() {
    try {
        const productURL = window.location.pathname;
        console.log(`Fetching details for product URL: ${productURL}`);

        const productDetails = await getProductDetails(productURL);
        const ecoFriendlyQuery = await generateEcoFriendlyQuery(productDetails.name);
        const initialRecommendations = await getRecommendations(ecoFriendlyQuery);
        
        if (initialRecommendations.length > 0) {
            const topRecommendation = initialRecommendations[6];  // Take the first item
            const imageDetails = await fetchImageDetailsForTopRecommendation(topRecommendation);  // Correct function call
            const detailedRecommendation = {
                ...topRecommendation,
                image_url: imageDetails.image_url  // Use image URL from the fetched data
            };
            recommendations = [detailedRecommendation]; // Update global recommendations
            console.log('Detailed recommendation:', detailedRecommendation);
        } else {
            recommendations = [];
        }
    } catch (error) {
        console.error('Failed to fetch recommendations:', error);
    }
}

function displayRecommendations(button) {
    button.style.width = "300px";
    button.style.height = "auto";
    button.style.backgroundColor = "#ccc";

    const container = document.createElement('div');
    if (recommendations.length > 0) {
        const product = recommendations[0];  // Display only the first recommendation
        const productDiv = document.createElement('div');
        productDiv.classList.add('product');

productDiv.innerHTML = `
            <div class="p-4 bg-white rounded-lg shadow-lg">
                <div class="flex justify-between items-center mb-4">
                    <h2 class="text-lg font-semibold text-green-700">Eco-friendly results:</h2>
                    <button class="text-black text-xl" onclick="collapseUI(button)">×</button>
                </div>
                <h3 class="text-md mb-2 text-gray-800">Here is your sustainable product alternative:</h3>
                <div class="flex items-center border-b pb-4 mb-4">
                    <img class="w-24 h-24 mr-4 rounded" src="${product.image_url}" alt="${product.title}">
                    <div class="flex-grow">
                        <h4 class="font-semibold text-green-600">${product.title}</h4>
                        <p class="text-gray-700">${product.price}</p>
                        <a class="mt-2 inline-block px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition-colors" href="https://www.amazon.com${product.url}" target="_blank">View Product</a>
                    </div>
                </div>
            </div>
        `;



        container.appendChild(productDiv);
    } else {
        container.innerHTML += '<p>No eco-friendly products found.</p>';
    }
    if (button.lastChild.tagName === 'DIV') {
        button.replaceChild(container, button.lastChild);
    } else {
        button.appendChild(container);
    }
}

function collapseUI(button) {
    button.textContent = "Click me";
    button.style.width = "auto";
    button.style.height = "auto";
    button.style.backgroundColor = "green";
    if (button.lastChild.tagName === 'DIV') {
        button.removeChild(button.lastChild);
    }
}

async function getProductDetails(productURL) {
    console.log(`Making API call to get product details for: ${productURL}`);
    const response = await fetch('http://127.0.0.1:5000/getimage', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({product_url: productURL})
    });
    return await response.json();
}

async function generateEcoFriendlyQuery(productName) {
    console.log(`Generating eco-friendly query for product: ${productName}`);
    const response = await fetch('http://127.0.0.1:5000/query', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({inputs: productName})
    });
    const data = await response.json();
    return `eco friendly and sustainable ${data[0].generated_text}`;
}

async function getRecommendations(query) {
    try {
        console.log(`Fetching recommendations for query: ${query}`);
        const response = await fetch('http://127.0.0.1:5000/scrape', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({keywords: query})
        });
        console.log('Response:', response);
        if (!response.ok) throw new Error('Failed to fetch recommendations');
        return await response.json();
    } catch (error) {
        console.error('Error fetching recommendations:', error);
        return [];  // Return an empty array to handle errors gracefully
    }
}
