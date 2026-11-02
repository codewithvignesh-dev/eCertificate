document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.querySelector("[data-certificate-file]");
    const fileName = document.querySelector("[data-file-name]");
    const fileSize = document.querySelector("[data-file-size]");
    const dropzone = document.querySelector("[data-upload-dropzone]");
    const description = document.querySelector("[data-certificate-description]");
    const variableButtons = document.querySelectorAll("[data-insert-variable]");
    const characterCount = document.querySelector("[data-description-count]");

    const formatFileSize = (bytes) => {
        if (!bytes) {
            return "0 Bytes";
        }

        const units = ["Bytes", "KB", "MB", "GB"];
        const index = Math.min(
            Math.floor(Math.log(bytes) / Math.log(1024)),
            units.length - 1
        );

        return `${(bytes / Math.pow(1024, index)).toFixed(index ? 2 : 0)} ${units[index]}`;
    };

    const updateFile = (file) => {
        if (!file) {
            return;
        }

        if (fileName) {
            fileName.textContent = file.name;
        }

        if (fileSize) {
            fileSize.textContent = formatFileSize(file.size);
        }
    };

    fileInput?.addEventListener("change", () => {
        updateFile(fileInput.files?.[0]);
    });

    ["dragenter", "dragover"].forEach((eventName) => {
        dropzone?.addEventListener(eventName, (event) => {
            event.preventDefault();
            dropzone.classList.add("is-dragging");
        });
    });

    ["dragleave", "drop"].forEach((eventName) => {
        dropzone?.addEventListener(eventName, (event) => {
            event.preventDefault();
            dropzone.classList.remove("is-dragging");
        });
    });

    dropzone?.addEventListener("drop", (event) => {
        const file = event.dataTransfer?.files?.[0];

        if (!file || !fileInput) {
            return;
        }

        const transfer = new DataTransfer();
        transfer.items.add(file);
        fileInput.files = transfer.files;
        updateFile(file);
    });

    variableButtons.forEach((button) => {
        button.addEventListener("click", () => {
            if (!description) {
                return;
            }

            const variable = button.dataset.insertVariable;
            const start = description.selectionStart;
            const end = description.selectionEnd;

            description.value =
                description.value.substring(0, start) +
                variable +
                description.value.substring(end);

            description.focus();

            const position = start + variable.length;
            description.setSelectionRange(position, position);

            description.dispatchEvent(new Event("input"));
        });
    });

    const updateCharacterCount = () => {
        if (!description || !characterCount) {
            return;
        }

        characterCount.textContent = `${description.value.length} / ${description.maxLength || 5000}`;
    };

    description?.addEventListener("input", updateCharacterCount);
    updateCharacterCount();
});