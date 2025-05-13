document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('input[type="file"]').forEach(function (input) {
        const wrapper = document.createElement('div');
        wrapper.classList.add('drag-wrapper');
        input.parentNode.insertBefore(wrapper, input);
        wrapper.appendChild(input);

        wrapper.addEventListener('dragover', (e) => {
            e.preventDefault();
            wrapper.classList.add('drag-over');
        });

        wrapper.addEventListener('dragleave', () => {
            wrapper.classList.remove('drag-over');
        });

        wrapper.addEventListener('drop', (e) => {
            e.preventDefault();
            wrapper.classList.remove('drag-over');

            if (e.dataTransfer.files.length > 0) {
                input.files = e.dataTransfer.files;
                input.dispatchEvent(new Event('change'));
            }
        });

        wrapper.addEventListener('click', () => input.click());
    });
});
