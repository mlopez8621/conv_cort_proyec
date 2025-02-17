let currentStep = 1;
        const totalSteps = 5;

        function showStep(step) {
            document.querySelectorAll(".form-step").forEach((el) => el.classList.remove("active"));
            document.getElementById("step" + step).classList.add("active");
            updateProgressBar(step);
        }

        function nextStep() {
            const activeStep = document.querySelector(".form-step.active"); // Obtiene el paso actual
            const requiredFields = activeStep.querySelectorAll("input[required], textarea[required], select[required]");
            let valid = true;

            requiredFields.forEach((input) => {
                if (!input.value.trim()) {
                    input.classList.add("is-invalid"); // Marca campo como inválido
                    valid = false;
                } else {
                    input.classList.remove("is-invalid"); // Quita error si está bien
                }

                // Validación de correo electrónico
                if (input.type === "email" && !/^\S+@\S+\.\S+$/.test(input.value)) {
                    input.classList.add("is-invalid");
                    valid = false;
                    alert("Por favor, ingrese un correo válido.");
                }

                // Validación de URL solo para enlaces de Vimeo o YouTube
                if (input.id === "id_enlace_vimeo") {
                    const vimeoPattern = /^https?:\/\/(www\.)?vimeo\.com\/\d+/; // URLs de Vimeo
                    const youtubePattern = /^https?:\/\/(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)[\w-]+/; // URLs de YouTube

                    if (!vimeoPattern.test(input.value) && !youtubePattern.test(input.value)) {
                        input.classList.add("is-invalid");
                        valid = false;
                        alert("Debe ingresar un enlace válido de Vimeo o YouTube.");
                    } else {
                        input.classList.remove("is-invalid");
                    }
                }


                // Validación de solo números
                if (input.type === "number" && isNaN(input.value)) {
                    input.classList.add("is-invalid");
                    valid = false;
                }
                // Validar específicamente el campo de duración
                const duracionField = document.getElementById("id_duracion");
                const pattern = /^([0-9]{1,2}):([0-5][0-9])$/; // Formato HH:MM
                if (duracionField && !pattern.test(duracionField.value)) {
                    duracionField.classList.add("is-invalid");
                    valid = false;
                    firstErrorField = duracionField;
                } else if (duracionField) {
                    duracionField.classList.remove("is-invalid");
                }
            });

             // Validar específicamente el campo de año
            const anioField = document.getElementById("id_anio_fdc");
            if (anioField && anioField.value.trim() !== "") {
                const currentYear = new Date().getFullYear();
                if (!/^\d{4}$/.test(anioField.value) || anioField.value < 1900 || anioField.value > currentYear) {
                    anioField.classList.add("is-invalid");
                    valid = false;
                    alert("El año debe estar en formato YYYY y estar entre 1900 y " + currentYear);
                } else {
                    anioField.classList.remove("is-invalid");
                }
            }

            if (!valid) {
                alert("Corrige los campos resaltados antes de continuar.");
                return; // Detiene el avance si hay errores
            }

            // Si todo está validado, avanza al siguiente paso
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
            const progress = (step / totalSteps) * 100;
            document.getElementById("progressBar").style.width = progress + "%";
            document.getElementById("progressBar").setAttribute("aria-valuenow", progress);
        }

        document.addEventListener("DOMContentLoaded", () => showStep(currentStep));
        document.addEventListener("DOMContentLoaded", function() {
        let tituloInput = document.getElementById("id_titulo");
        tituloInput.addEventListener("input", function() {
            this.value = this.value.toUpperCase();
        });
    });
    document.addEventListener("DOMContentLoaded", function () {
        const radioButtons = document.querySelectorAll("input[name='beneficiario_fdc']");
        const inputAnio = document.getElementById("id_anio_fdc");
        const inputFile = document.getElementById("id_certificacion_fdc");

        // Inicialmente deshabilitados y sin required
        inputAnio.disabled = true;
        inputFile.disabled = true;
        inputAnio.removeAttribute("required");
        inputFile.removeAttribute("required");

        radioButtons.forEach(radio => {
            radio.addEventListener("change", function () {
                if (this.value === "si") {
                    inputAnio.disabled = false;
                    inputFile.disabled = false;
                    inputAnio.setAttribute("required", "required");
                    inputFile.setAttribute("required", "required");
                } else {
                    inputAnio.disabled = true;
                    inputFile.disabled = true;
                    inputAnio.removeAttribute("required");
                    inputFile.removeAttribute("required");
                    inputAnio.value = "";
                    inputFile.value = "";
                    inputAnio.classList.remove("is-invalid");
                    inputFile.classList.remove("is-invalid");
                }
            });
        });

        // Validar el año ingresado (debe ser 4 dígitos)
        inputAnio.addEventListener("input", function () {
            const currentYear = new Date().getFullYear();
            const minYear = 1900; // Definir un año mínimo aceptable
            const yearPattern = /^[0-9]{4}$/; // Debe ser exactamente 4 dígitos

            if (!yearPattern.test(this.value) || this.value < minYear || this.value > currentYear) {
                this.setCustomValidity("Ingrese un año válido entre " + minYear + " y " + currentYear);
                this.classList.add("is-invalid");
            } else {
                this.setCustomValidity("");
                this.classList.remove("is-invalid");
            }
        });
    });


    document.addEventListener("DOMContentLoaded", function () {
        const radioButtons = document.querySelectorAll("input[name='plataformas_exhibicion']");
        const inputSiPlataforma = document.getElementById("id_si_plataforma");

        // Deshabilitar y quitar required inicialmente
        inputSiPlataforma.disabled = true;
        inputSiPlataforma.removeAttribute("required");

        radioButtons.forEach(radio => {
            radio.addEventListener("change", function () {
                if (this.value === "si") {
                    inputSiPlataforma.disabled = false;
                    inputSiPlataforma.setAttribute("required", "required"); // Hacerlo obligatorio
                } else {
                    inputSiPlataforma.disabled = true;
                    inputSiPlataforma.removeAttribute("required"); // Quitar requerido
                    inputSiPlataforma.value = ""; // Limpiar el campo
                }
            });
        });
    });

    document.getElementById("togglePassword").addEventListener("click", function () {
        let passwordField = document.getElementById("id_contrasena_vimeo");
        if (passwordField.type === "password") {
            passwordField.type = "text";  // Mostrar contraseña
        } else {
            passwordField.type = "password";  // Ocultar contraseña
        }
    });
    document.addEventListener("DOMContentLoaded", function () {
        const form = document.querySelector("form");

        form.addEventListener("submit", function (event) {
            let errores = [];
            let primerError = null;

            // Obtener todos los campos que deben ser validados
            const requiredFields = document.querySelectorAll("input[required], textarea[required], select[required]");

            requiredFields.forEach(field => {
                if (!field.value.trim()) { // Verifica si está vacío
                    errores.push(`El campo "${field.name}" es obligatorio.`);
                    field.classList.add("is-invalid"); // Agrega clase de Bootstrap para mostrar error
                    if (!primerError) primerError = field;
                } else {
                    field.classList.remove("is-invalid"); // Si está bien, elimina la clase de error
                }
            });

            // Validar números
            const numberFields = document.querySelectorAll("input[type='number']");
            numberFields.forEach(field => {
                if (field.value && isNaN(field.value)) {
                    errores.push(`El campo "${field.name}" debe ser un número válido.`);
                    field.classList.add("is-invalid");
                    if (!primerError) primerError = field;
                } else {
                    field.classList.remove("is-invalid");
                }
            });

            // Mostrar alertas si hay errores
            if (errores.length > 0) {
                event.preventDefault(); // Evita que el formulario se envíe
                alert("Corrige los siguientes errores antes de enviar:\n\n" + errores.join("\n"));
                primerError.focus(); // Enfocar el primer campo con error
            }
        });
    });
    document.addEventListener("DOMContentLoaded", function () {
        const duracionField = document.getElementById("id_duracion");

        if (duracionField) { // Verifica que el campo existe
            // Crear un pequeño mensaje de error debajo del campo
            const errorMessage = document.createElement("div");
            errorMessage.classList.add("invalid-feedback");
            errorMessage.textContent = "Ingrese la duración en formato HH:MM (ej. 08:30)";
            duracionField.parentNode.appendChild(errorMessage);

            duracionField.addEventListener("input", function () {
                const pattern = /^([0-9]{1,2}):([0-5][0-9])$/; // Formato HH:MM
                if (!pattern.test(this.value)) {
                    this.setCustomValidity("Formato incorrecto");
                    this.classList.add("is-invalid");
                    errorMessage.style.display = "block"; // Muestra el mensaje
                } else {
                    this.setCustomValidity("");
                    this.classList.remove("is-invalid");
                    errorMessage.style.display = "none"; // Oculta el mensaje
                }
            });
        }
    });
    document.addEventListener("DOMContentLoaded", function () {
        const submitButton = document.querySelector("button[type='submit']");
        const radioSi = document.querySelector("input[name='acepta_tyc'][value='si']");
        const radioNo = document.querySelector("input[name='acepta_tyc'][value='no']");
    
        function validarTyc() {
            if (!radioSi.checked) {
                alert("Debe aceptar los términos y condiciones para enviar la postulación.");
                return false;
            }
            return true;
        }
    
        submitButton.addEventListener("click", function (event) {
            if (!validarTyc()) {
                event.preventDefault(); // Evita que el formulario se envíe
            }
        });
    
        // Deshabilitar el botón de envío si "No" está seleccionado
            radioNo.addEventListener("change", function () {
                submitButton.disabled = true;
            });
        
            // Habilitar el botón de envío si "Sí" está seleccionado
            radioSi.addEventListener("change", function () {
                submitButton.disabled = false;
            });
        
            // Al cargar la página, asegurarse de que el botón esté correctamente habilitado o deshabilitado
            if (radioNo.checked) {
                submitButton.disabled = true;
            }
        });
    document.addEventListener("DOMContentLoaded", function () {
        // Seleccionar todos los radios del subgénero
        let subgeneroRadios = document.querySelectorAll("input[name='subgenero_cortrometraje']");
        let otroSubgeneroField = document.querySelector("#id_otro_subgenero_cortrometraje"); // ID del campo "Otro subgénero"

        // Deshabilitar el campo al inicio
        otroSubgeneroField.disabled = true;

        subgeneroRadios.forEach(radio => {
            radio.addEventListener("change", function () {
                // Si se selecciona "Otros", habilitar el campo
                if (this.value.toLowerCase() === "otro") {
                    otroSubgeneroField.disabled = false;
                } else {
                    otroSubgeneroField.disabled = true;
                    otroSubgeneroField.value = ""; // Limpiar campo si se deshabilita
                }
            });
        });
    });    
    