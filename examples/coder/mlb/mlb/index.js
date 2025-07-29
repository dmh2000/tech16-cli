let gameData = [];
let refreshInterval;

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    fetchGames();
    startAutoRefresh();
}

function startAutoRefresh() {
    refreshInterval = setInterval(() => {
        fetchGames();
    }, 30000);
}

function stopAutoRefresh() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }
}

async function fetchGames() {
    const loadingElement = document.getElementById('loading');
    const gamesContainer = document.getElementById('gamesContainer');
    const errorMessage = document.getElementById('errorMessage');
    const lastUpdated = document.getElementById('lastUpdated');
    
    try {
        showLoading(true);
        hideError();
        
        const response = await fetch('http://localhost:8001/mlb.csv', {
            method: 'GET',
            headers: {
                'Accept': 'text/csv',
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const csvData = await response.text();
        gameData = parseCSV(csvData);
        
        renderGames();
        updateLastUpdatedTime();
        showLoading(false);
        
    } catch (error) {
        console.error('Error fetching games:', error);
        showError();
        showLoading(false);
    }
}

function parseCSV(csvText) {
    const lines = csvText.trim().split('\n');
    const games = [];
    
    for (let i = 1; i < lines.length; i++) {
        const line = lines[i].trim();
        if (line) {
            const columns = line.split(',');
            if (columns.length >= 5) {
                games.push({
                    visitor: columns[0].trim(),
                    home: columns[1].trim(),
                    visitorScore: columns[2].trim(),
                    homeScore: columns[3].trim(),
                    status: columns[4].trim()
                });
            }
        }
    }
    
    return games;
}

function renderGames() {
    const gamesContainer = document.getElementById('gamesContainer');
    
    if (gameData.length === 0) {
        gamesContainer.innerHTML = '<div class="no-games">No games scheduled today</div>';
        return;
    }
    
    const gamesHTML = gameData.map(game => createGameCard(game)).join('');
    gamesContainer.innerHTML = gamesHTML;
}

function createGameCard(game) {
    const statusClass = getStatusClass(game.status);
    
    return `
        <div class="game-card">
            <div class="teams-container">
                <div class="team">
                    <div class="visitor-label">Visitor</div>
                    <div class="team-name">${game.visitor}</div>
                    <div class="team-score">${game.visitorScore}</div>
                </div>
                <div class="vs-divider">
                    <span>VS</span>
                </div>
                <div class="team">
                    <div class="home-label">Home</div>
                    <div class="team-name">${game.home}</div>
                    <div class="team-score">${game.homeScore}</div>
                </div>
            </div>
            <div class="game-status ${statusClass}">
                ${formatStatus(game.status)}
            </div>
        </div>
    `;
}

function getStatusClass(status) {
    const statusLower = status.toLowerCase();
    
    if (statusLower.includes('final') || statusLower.includes('f/')) {
        return 'status-final';
    } else if (statusLower.includes('inning') || statusLower.includes('top') || statusLower.includes('bot') || 
               statusLower.includes('middle') || /^\d+$/.test(statusLower)) {
        return 'status-live';
    } else {
        return 'status-upcoming';
    }
}

function formatStatus(status) {
    if (status.includes('PM ET') || status.includes('AM ET')) {
        return `Game Time: ${status}`;
    } else if (status.toLowerCase().includes('final')) {
        return 'Final';
    } else if (status.toLowerCase().includes('inning')) {
        return status;
    } else {
        return status;
    }
}

function showLoading(show) {
    const loadingElement = document.getElementById('loading');
    if (show) {
        loadingElement.style.display = 'block';
    } else {
        loadingElement.style.display = 'none';
    }
}

function showError() {
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.style.display = 'block';
}

function hideError() {
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.style.display = 'none';
}

function updateLastUpdatedTime() {
    const lastUpdated = document.getElementById('lastUpdated');
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
    lastUpdated.textContent = timeString;
}

window.addEventListener('beforeunload', function() {
    stopAutoRefresh();
});