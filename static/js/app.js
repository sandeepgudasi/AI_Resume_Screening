document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const resumeInput = document.getElementById('resume-input');
    const fileNameDisplay = document.getElementById('file-name');
    const analyzeBtn = document.getElementById('analyze-btn');
    const jdInput = document.getElementById('jd-input');
    const resultsSection = document.getElementById('results-section');
    const loader = document.getElementById('loader');

    let chart = null;

    dropZone.addEventListener('click', () => resumeInput.click());
    resumeInput.addEventListener('change', () => {
        if (resumeInput.files.length > 0) fileNameDisplay.textContent = `Selected: ${resumeInput.files[0].name}`;
    });

    analyzeBtn.addEventListener('click', async () => {
        const jd = jdInput.value.trim();
        const resumeFile = resumeInput.files[0];
        if (!jd || !resumeFile) { alert('Please provide JD and Resume.'); return; }

        const formData = new FormData();
        formData.append('jd', jd);
        formData.append('resume', resumeFile);

        loader.classList.remove('hidden');
        resultsSection.classList.add('hidden');

        try {
            const response = await fetch('/analyze', { method: 'POST', body: formData });
            const data = await response.json();
            if (data.error) alert(data.error); else displayResults(data);
        } catch (error) { console.error(error); alert('An error occurred.'); } finally { loader.classList.add('hidden'); }
    });

    function displayResults(data) {
        resultsSection.classList.remove('hidden');
        document.getElementById('score-value').textContent = `${data.score}%`;
        document.getElementById('explanation-text').textContent = data.explanation;

        const statusBadge = document.getElementById('status-badge');
        statusBadge.textContent = data.status === 'THINKING' ? 'Under Review' : data.status;
        statusBadge.className = 'status-badge ' + data.status.toLowerCase();

        document.getElementById('matched-skills').innerHTML = data.matched_skills.map(s => `<span class="skill-tag">${s}</span>`).join('');
        document.getElementById('missing-skills').innerHTML = data.missing_skills.map(s => `<span class="skill-tag missing">${s}</span>`).join('');
        document.getElementById('suggestions-list').innerHTML = data.suggestions.map(s => `<li>${s}</li>`).join('');

        updateChart(data.score);
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    function updateChart(score) {
        const ctx = document.getElementById('scoreChart').getContext('2d');
        if (chart) chart.destroy();
        chart = new Chart(ctx, {
            type: 'doughnut',
            data: { datasets: [{ data: [score, 100 - score], backgroundColor: ['#6366f1', '#1e293b'], borderWidth: 0 }] },
            options: { cutout: '80%', plugins: { legend: { display: false } } }
        });
    }
});
