function isAmazonProductPage() {
  return window.location.hostname === "www.amazon.com" && window.location.pathname.includes("/dp/");
}

if (isAmazonProductPage()) {
  chrome.runtime.sendMessage({ action: "openPopup" });
}