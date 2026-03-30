document.addEventListener("DOMContentLoaded", () => {
  fetch("http://127.0.0.1:5000/scrape")
    .then(response => response.json())
    .then(data => {
      document.getElementById("test").innerText = JSON.stringify(data, null, 2);
    })
    .catch(error => console.error('Error:', error));
});