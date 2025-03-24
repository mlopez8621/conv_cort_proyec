let currentStep = 1;
const totalSteps = 5;

function showStep(step) {
    let steps = document.querySelectorAll(".form-step");
    if (steps.length === 0) {
        console.warn("No se encontraron elementos con la clase 'form-step'.");
        return;
    }

    steps.forEach((el) => el.classList.remove("active"));

    let stepElement = document.getElementById("step" + step);
    if (stepElement) {
        stepElement.classList.add("active");
        updateProgressBar(step);
    } else {
        console.warn(`Elemento no encontrado: step${step}`);
    }
}

function nextStep() {
    const activeStep = document.querySelector(".form-step.active");
    if (!activeStep) return;

    const requiredFields = activeStep.querySelectorAll("input[required], textarea[required], select[required]");
    let valid = true;

    requiredFields.forEach((input) => {
        if (!input.value.trim()) {
            input.classList.add("is-invalid");
            valid = false;
        } else {
            input.classList.remove("is-invalid");
        }

        // Validación de correo
        if (input.type === "email" && !/^\S+@\S+\.\S+$/.test(input.value)) {
            input.classList.add("is-invalid");
            valid = false;
            alert("Por favor, ingrese un correo válido.");
        }

        // Validación de URL (Vimeo / YouTube)
        if (input.id === "id_enlace_vimeo") {
            const vimeoPattern = /^https?:\/\/(www\.)?vimeo\.com\/\d+/;
            const youtubePattern = /^https?:\/\/(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)[\w-]+/;
            if (!vimeoPattern.test(input.value) && !youtubePattern.test(input.value)) {
                input.classList.add("is-invalid");
                valid = false;
                alert("Debe ingresar un enlace válido de Vimeo o YouTube.");
            } else {
                input.classList.remove("is-invalid");
            }
        }

        // Validación de números
        if (input.type === "number" && isNaN(Number(input.value))) {
            input.classList.add("is-invalid");
            valid = false;
        }
    });

    // Validar duración (HH:MM)
    const duracionField = document.getElementById("id_duracion");
    if (duracionField) {
        const pattern = /^([0-9]{1,2}):([0-5][0-9])$/;
        if (!pattern.test(duracionField.value)) {
            duracionField.classList.add("is-invalid");
            valid = false;
        } else {
            duracionField.classList.remove("is-invalid");
        }
    }

    // Validar año (YYYY entre 1900 y el año actual)
    const anioField = document.getElementById("id_anio_fdc");
    if (anioField && anioField.value.trim() !== "") {
        const currentYear = new Date().getFullYear();
        const anioIngresado = Number(anioField.value);
        if (!/^\d{4}$/.test(anioField.value) || anioIngresado < 1900 || anioIngresado > currentYear) {
            anioField.classList.add("is-invalid");
            valid = false;
            alert(`El año debe estar entre 1900 y ${currentYear}`);
        } else {
            anioField.classList.remove("is-invalid");
        }
    }

    if (!valid) {
        alert("Corrige los campos resaltados antes de continuar.");
        return;
    }

    if (currentStep < totalSteps) {
        currentStep++;
        showStep(currentStep);
    }
}

function prevStep() {
    if (currentStep > 1) {
        currentStep--;
        showStep(currentStep);
    }
}

function updateProgressBar(step) {
    let progressBar = document.getElementById("progressBar");
    if (progressBar) {
        const progress = (step / totalSteps) * 100;
        progressBar.style.width = progress + "%";
        progressBar.setAttribute("aria-valuenow", progress);
    }
}

// Ejecutar showStep solo si existen pasos en la página
document.addEventListener("DOMContentLoaded", function () {
    if (document.querySelector(".form-step")) {
        showStep(currentStep);
    }
});

// Convertir título en mayúsculas si existe
document.addEventListener("DOMContentLoaded", function () {
    let tituloInput = document.getElementById("id_titulo");
    if (tituloInput) {
        tituloInput.addEventListener("input", function () {
            this.value = this.value.toUpperCase();
        });
    }
});

// Validación de campos dependientes (Beneficiario FDC)
document.addEventListener("DOMContentLoaded", function () {
    const radioButtons = document.querySelectorAll("input[name='beneficiario_fdc']");
    const inputAnio = document.getElementById("id_anio_fdc");
    const inputFile = document.getElementById("id_certificacion_fdc");

    if (inputAnio && inputFile) {
        inputAnio.disabled = true;
        inputFile.disabled = true;

        radioButtons.forEach(radio => {
            radio.addEventListener("change", function () {
                if (this.value === "si") {
                    inputAnio.disabled = false;
                    inputFile.disabled = false;
                } else {
                    inputAnio.disabled = true;
                    inputFile.disabled = true;
                    inputAnio.value = "";
                    inputFile.value = "";
                }
            });
        });
    }
});

// Mostrar/Ocultar contraseña (si el botón existe)
document.addEventListener("DOMContentLoaded", function () {
    let togglePassword = document.getElementById("togglePassword");
    if (togglePassword) {
        let passwordField = document.getElementById("id_contrasena_vimeo");
        togglePassword.addEventListener("click", function () {
            if (passwordField) {
                passwordField.type = passwordField.type === "password" ? "text" : "password";
            }
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {
    // 🔹 Asegurar que seleccionamos el formulario correcto
    let form = document.querySelector("form:not([action='/accounts/logout/'])"); // Excluye el formulario de logout
    let comentarioInput = document.getElementById("id_comentario");
    let recomendacionInput = document.getElementById("id_recomendacion");

    console.log("Formulario seleccionado:", form);  // 🔥 Verificar si selecciona el correcto
    console.log("Campo comentario:", comentarioInput);  // 🔥 Verificar si selecciona correctamente el campo
    console.log("Campo recomendación:", recomendacionInput);  // 🔥 Verificar si selecciona correctamente el campo

    if (form && comentarioInput && recomendacionInput) {
        console.log("✅ Entró al if correctamente"); // 🔥 Debug

        // 🔹 Crear mensajes de error si no existen
        let errorComentario = document.createElement("div");
        errorComentario.classList.add("invalid-feedback");
        comentarioInput.parentNode.appendChild(errorComentario);

        let errorRecomendacion = document.createElement("div");
        errorRecomendacion.classList.add("invalid-feedback");
        recomendacionInput.parentNode.appendChild(errorRecomendacion);

        form.addEventListener("submit", function (event) {
            let comentarioTexto = comentarioInput.value.trim();
            let recomendacionTexto = recomendacionInput.value.trim();
            let valid = true;

            // 🔴 Validar Comentario
            if (!comentarioTexto) {  
                errorComentario.textContent = "❌ El comentario no puede estar vacío.";
                comentarioInput.classList.add("is-invalid");
                valid = false;
            } else if (comentarioTexto.length < 50) {  
                errorComentario.textContent = "⚠️ El comentario debe tener al menos 50 caracteres.";
                comentarioInput.classList.add("is-invalid");
                valid = false;
            } else {  
                comentarioInput.classList.remove("is-invalid");
                errorComentario.textContent = "";
            }

            // 🔴 Validar Recomendación
            if (!recomendacionTexto) {  
                errorRecomendacion.textContent = "❌ Debe seleccionar una recomendación.";
                recomendacionInput.classList.add("is-invalid");
                valid = false;
            } else {  
                recomendacionInput.classList.remove("is-invalid");
                errorRecomendacion.textContent = "";
            }

            // 🔹 Evitar envío si hay errores
            if (!valid) {
                event.preventDefault();
            }
        });
    } else {
        console.warn("⚠️ No se encontró el formulario correcto o algún campo necesario");
    }
});


// Validar aceptación de términos antes de enviar formulario
document.addEventListener("DOMContentLoaded", function () {
    const submitButton = document.querySelector("button[type='submit']");
    const radioSi = document.querySelector("input[name='acepta_tyc'][value='si']");
    const radioNo = document.querySelector("input[name='acepta_tyc'][value='no']");

    if (submitButton && radioSi && radioNo) {
        submitButton.addEventListener("click", function (event) {
            if (!radioSi.checked) {
                alert("Debe aceptar los términos y condiciones para enviar la postulación.");
                event.preventDefault();
            }
        });

        radioNo.addEventListener("change", function () {
            submitButton.disabled = true;
        });

        radioSi.addEventListener("change", function () {
            submitButton.disabled = false;
        });

        if (radioNo.checked) {
            submitButton.disabled = true;
        }
    }
});
