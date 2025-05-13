document.addEventListener("DOMContentLoaded", function () {
    const input = document.querySelector('input[type="file"]');
    if (!input) return;

    // Create wrapper box
    const box = document.createElement('div');
    box.classList.add('custom-upload-box');
    box.textContent = 'Drop or click to upload image';

    input.parentNode.insertBefore(box, input);
    input.style.display = 'none';

    box.addEventListener('click', () => input.click());

    input.addEventListener('change', () => {
        const file = input.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = () => {
                box.style.backgroundImage = `url(${reader.result})`;
                box.textContent = '';
            };
            reader.readAsDataURL(file);
        }
    });

    box.addEventListener('dragover', (e) => {
        e.preventDefault();
        box.classList.add('drag-over');
    });

    box.addEventListener('dragleave', () => {
        box.classList.remove('drag-over');
    });

    box.addEventListener('drop', (e) => {
        e.preventDefault();
        input.files = e.dataTransfer.files;
        input.dispatchEvent(new Event('change'));
        box.classList.remove('drag-over');
    });
});
