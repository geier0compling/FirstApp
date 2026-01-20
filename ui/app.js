// Store flashcards globally for CSV export
let currentFlashcards = [];

// Handle "Generate Flashcards" button click
document.getElementById("generateBtn").addEventListener("click", async () => {
    console.log("Generate button clicked");

    const text = document.getElementById("inputText").value.trim();
    const container = document.getElementById("flashcardContainer");
    container.innerHTML = "";

    if (!text) {
        alert("Please enter some German text first.");
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/api/flashcards", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: text })
        });

        if (!response.ok) {
            const body = await response.text();
            console.error("Response error:", response.status, body);
            alert("Server error: " + response.status);
            return;
        }

        const data = await response.json();

        if (!data.flashcards || !data.flashcards.length) {
            container.innerHTML = "<p>No flashcards generated.</p>";
            return;
        }

        // Render flashcards
        data.flashcards.forEach(card => {
            const div = document.createElement("div");
            div.className = "flashcard";

            div.innerHTML = `
                <h3>${card.display_word || card.word}</h3>
                <div class="detail"><strong>Meaning:</strong> ${card.translation}</div>
                <div class="detail"><strong>CEFR:</strong> ${card.cefr}</div>
                <div class="detail">
                    ${card.display_details ? card.display_details.replace(/\n/g, "<br>") : ""}
                </div>
                <div class="detail"><strong>Example:</strong><br>${card.example_sentence || ""}</div>
            `;

            container.appendChild(div);
        });

        // Save flashcards globally
        currentFlashcards = data.flashcards;

        // Show Download button
        document.getElementById("downloadBtn").style.display = "inline-block";

    } catch (err) {
        console.error("Fetch failed:", err);
        alert("Could not contact API. See console for details.");
    }
});


// Download CSV (Quizlet-ready)
function downloadCSV() {
    console.log("Download CSV clicked");

    if (!currentFlashcards.length) return;

    let csv = "Term,Definition\n";

    currentFlashcards.forEach(card => {
        let term = card.display_word || card.word;

        // Noun plural formatting → "die Chance | die Chancen"
        if (card.pos === "NOUN" && card.plural) {
            term = `${term} | die ${card.plural}`;
        }

        // Verb conjugations → "kämpfen (kämpft / kämpfte / gekämpft)"
        if (card.pos === "VERB" && card.conjugations) {
            const c = card.conjugations;
            const parts = [
                c["3sg"] || null,
                c["preterite"] || null,
                c["participle"] || null
            ].filter(Boolean);

            if (parts.length > 0) {
                term = `${term} (${parts.join(" / ")})`;
            }
        }

        // Remove commas from English side only (safe for CSV)
        const definition = card.translation.replace(/,/g, "");

        // Remove commas from TERM completely (CSV safety)
        term = term.replace(/,/g, "");

        csv += `${term},${definition}\n`;
    });

    // Create CSV & trigger download
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = "flashcards.csv";
    link.click();

    URL.revokeObjectURL(url);
}

// Attach Download button behavior
document.getElementById("downloadBtn").addEventListener("click", downloadCSV);
