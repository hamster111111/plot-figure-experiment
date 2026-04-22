(() => {
  const selectors = ".img-single img, .img-compare img";
  const images = Array.from(document.querySelectorAll(selectors));

  if (!images.length) {
    return;
  }

  const overlay = document.createElement("div");
  overlay.className = "image-lightbox";
  overlay.setAttribute("aria-hidden", "true");
  overlay.innerHTML = `
    <button class="image-lightbox-close" type="button" aria-label="Close image viewer">×</button>
    <div class="image-lightbox-inner">
      <img alt="">
      <div class="image-lightbox-caption"></div>
    </div>
  `;
  document.body.appendChild(overlay);

  const overlayImage = overlay.querySelector("img");
  const overlayCaption = overlay.querySelector(".image-lightbox-caption");
  const closeButton = overlay.querySelector(".image-lightbox-close");

  function getCaption(image) {
    const container = image.closest(".img-single, .img-compare > div, .trace-card, .card");
    const label = container?.querySelector(".img-label");
    if (label?.textContent?.trim()) {
      return label.textContent.trim();
    }
    if (image.alt?.trim()) {
      return image.alt.trim();
    }
    return "Chart preview";
  }

  function openLightbox(image) {
    overlayImage.src = image.currentSrc || image.src;
    overlayImage.alt = image.alt || "";
    overlayCaption.textContent = getCaption(image);
    overlay.classList.add("open");
    overlay.setAttribute("aria-hidden", "false");
    document.body.classList.add("lightbox-open");
  }

  function closeLightbox() {
    overlay.classList.remove("open");
    overlay.setAttribute("aria-hidden", "true");
    overlayImage.removeAttribute("src");
    document.body.classList.remove("lightbox-open");
  }

  for (const image of images) {
    image.loading = "lazy";
    image.decoding = "async";
    image.classList.add("zoomable-image");
    image.title = "Click to enlarge";
    image.addEventListener("click", () => openLightbox(image));
  }

  overlay.addEventListener("click", (event) => {
    if (event.target === overlay || event.target === closeButton) {
      closeLightbox();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && overlay.classList.contains("open")) {
      closeLightbox();
    }
  });
})();
