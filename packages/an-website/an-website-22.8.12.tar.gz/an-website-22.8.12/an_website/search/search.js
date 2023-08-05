// @license magnet:?xt=urn:btih:0b31508aeb0634b347b8270c7bee4d411b5d4109&dn=agpl-3.0.txt GNU-AGPL-3.0-or-later
"use strict";
(() => {
    const resultsList = elById("search-results");
    const searchForm = elById("search-form");
    const searchInput = elById("search-input");

    function displayResults(results) {
        resultsList.innerHTML = "";
        for (const result of results) {
            const resultElement = d.createElement("li");
            resultElement.setAttribute(
                "score", String(result["score"])
            );
            resultElement.innerHTML = (
                `<a href='${fixHref(result.url)}'>`
                + `${result.title}</a> ${result.description}`
            );
            resultsList.appendChild(resultElement);
        }
    }

    w.PopStateHandlers["search"] = (event) => {
        searchInput.value = event.state["query"];
        displayResults(event.state["results"]);
    }

    searchForm.onsubmit = (e) => {
        e.preventDefault();
        get(
            "/api/suche",
            "q=" + searchInput.value,
            (data) => {
                displayResults(data);
                setURLParam(
                    "q",
                    searchInput.value,
                    {
                        "query": searchInput.value,
                        "results": data
                    },
                    "search",
                    true
                );
            }
        );
    }
})();
// @license-end
