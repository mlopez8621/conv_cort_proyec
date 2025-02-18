document.addEventListener("DOMContentLoaded", function () {
    function validarFormulario() {
        const selectEvaluadores = document.getElementById("evaluadores");

        if (!selectEvaluadores) {
            console.error("⚠️ No se encontró el elemento <select> de evaluadores.");
            return false;
        }

        const seleccionados = Array.from(selectEvaluadores.selectedOptions).map(option => option.value);

        if (seleccionados.length === 0) {
            alert("❌ Debes seleccionar al menos un evaluador antes de asignarlos.");
            return false; // Evita que el formulario se envíe
        }

        return true; // Permite el envío si al menos un evaluador está seleccionado
    }

    // Exponer la función al scope global para que el HTML pueda llamarla
    window.validarFormulario = validarFormulario;
});
