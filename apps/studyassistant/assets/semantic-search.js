(function () {
    "use strict";

    var input = document.getElementById("semantic-q");
    var button = document.getElementById("semantic-search-btn");
    var statusBox = document.getElementById("semantic-search-status");
    var resultsList = document.getElementById("semantic-search-results");

    if (!input || !button || !statusBox || !resultsList) {
        return;
    }

    function setStatus(text, isError) {
        if (!text) {
            statusBox.hidden = true;
            statusBox.textContent = "";
            return;
        }
        statusBox.hidden = false;
        statusBox.textContent = text;
        statusBox.classList.toggle("is-error", Boolean(isError));
    }

    function clearResults() {
        resultsList.innerHTML = "";
    }

    function renderResults(results) {
        clearResults();

        if (!results || results.length === 0) {
            setStatus("Sin resultados para esa búsqueda.", false);
            return;
        }

        setStatus("", false);

        results.forEach(function (result) {
            var item = document.createElement("li");
            item.className = "semantic-result-item";

            var link = document.createElement("a");
            link.href = result.url;
            link.className = "semantic-result-title";
            link.textContent = result.note_title + (result.heading ? " — " + result.heading : "");
            item.appendChild(link);

            var score = document.createElement("span");
            score.className = "semantic-result-score";
            score.textContent = "relevancia " + Math.round(result.score * 100) + "%";
            item.appendChild(score);

            if (result.text_preview) {
                var preview = document.createElement("p");
                preview.className = "semantic-result-preview";
                preview.textContent = result.text_preview;
                item.appendChild(preview);
            }

            resultsList.appendChild(item);
        });
    }

    function runSearch() {
        var query = input.value.trim();
        if (!query) {
            setStatus("Escribe algo para buscar.", true);
            return;
        }

        clearResults();
        setStatus("Buscando...", false);
        button.disabled = true;

        fetch("search.php?q=" + encodeURIComponent(query) + "&top_k=8")
            .then(function (response) {
                return response.json().then(function (data) {
                    return { ok: response.ok, data: data };
                });
            })
            .then(function (result) {
                if (!result.ok) {
                    setStatus(result.data.error || "Ha ocurrido un error en la búsqueda.", true);
                    return;
                }
                if (result.data.warning) {
                    setStatus(result.data.warning, true);
                    return;
                }
                renderResults(result.data.results);
            })
            .catch(function () {
                setStatus("No se ha podido conectar con el servidor.", true);
            })
            .finally(function () {
                button.disabled = false;
            });
    }

    button.addEventListener("click", runSearch);
    input.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();
            runSearch();
        }
    });
})();
