const searchInput = document.getElementById('searchInput');
const resultsContainer = document.getElementById('resultsContainer');
const recentTags = document.querySelectorAll('.recent-tag');

// Function to fetch suggestions from the API
async function fetchSuggestions(query) {
    try {
        const response = await fetch(`http://localhost:8000/v1/autocomplete?query=${query}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching suggestions:", error);
        return [];
    }
}

async function renderResults(query) {
    // Clear previous results
    resultsContainer.innerHTML = '';
    
    if (query.length === 0) {
        resultsContainer.classList.remove('active');
        return;
    }
    
    resultsContainer.classList.add('active');
    
    try {
        // Get suggestions from backend
        const suggestions = await fetchSuggestions(query);
        
        if (suggestions.length === 0) {
            // Show no results message
            const noResults = document.createElement('div');
            noResults.className = 'result-item';
            noResults.innerHTML = `
                <div class="result-text">
                    <div class="result-title">No results found for "${query}"</div>
                    <div class="result-desc">Try different keywords or browse suggestions</div>
                </div>
            `;
            resultsContainer.appendChild(noResults);
            return;
        }
        
        // Generate result items
        suggestions.forEach((suggestion, index) => {
            const resultItem = document.createElement('div');
            resultItem.className = 'result-item';
            
            resultItem.innerHTML = `
                <div class="result-icon">${index + 1}</div>
                <div class="result-text">
                    <div class="result-title">${highlightMatch(suggestion.title, query)}</div>
                    <div class="result-desc">${suggestion.desc}</div>
                </div>
            `;
            
            resultItem.addEventListener('click', () => {
                searchInput.value = suggestion.title;
                resultsContainer.classList.remove('active');
            });
            
            resultsContainer.appendChild(resultItem);
        });
    } catch (error) {
        console.error("Error rendering results:", error);
        
        // Fallback to hardcoded suggestions if API fails
        const fallbackSuggestions = [
            { title: 'Beautiful landscapes photography', desc: 'Discover stunning nature photography techniques' },
            { title: 'Web design inspiration 2025', desc: 'Latest trends in modern web design' },
            { title: 'Aesthetic minimalist home decor', desc: 'Simple and elegant home decoration ideas' },
            { title: 'Digital art tutorials for beginners', desc: 'Start your journey in digital illustration' },
            { title: 'Modern UI/UX design principles', desc: 'Create beautiful and functional interfaces' }
        ];
        
        // Filter fallback suggestions based on query
        const filteredSuggestions = fallbackSuggestions.filter(suggestion => 
            suggestion.title.toLowerCase().includes(query.toLowerCase())
        );
        
        // Generate result items from fallback
        filteredSuggestions.forEach((suggestion, index) => {
            const resultItem = document.createElement('div');
            resultItem.className = 'result-item';
            
            resultItem.innerHTML = `
                <div class="result-icon">${index + 1}</div>
                <div class="result-text">
                    <div class="result-title">${highlightMatch(suggestion.title, query)}</div>
                    <div class="result-desc">${suggestion.desc}</div>
                </div>
            `;
            
            resultItem.addEventListener('click', () => {
                searchInput.value = suggestion.title;
                resultsContainer.classList.remove('active');
            });
            
            resultsContainer.appendChild(resultItem);
        });
    }
}

function highlightMatch(text, query) {
    if (!query) return text;
    const regex = new RegExp(`(${query})`, 'gi');
    return text.replace(regex, '<span style="color: var(--primary-color); font-weight: 600;">$1</span>');
}

// Add debounce to avoid excessive API calls
function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

// Use debounced version of renderResults
const debouncedRenderResults = debounce(renderResults, 300);

// Event listeners
searchInput.addEventListener('input', (e) => {
    debouncedRenderResults(e.target.value);
});

searchInput.addEventListener('focus', () => {
    if (searchInput.value.length > 0) {
        renderResults(searchInput.value);
    }
});

document.addEventListener('click', (e) => {
    if (!searchInput.contains(e.target) && !resultsContainer.contains(e.target)) {
        resultsContainer.classList.remove('active');
    }
});

// Recent tags functionality
recentTags.forEach(tag => {
    tag.addEventListener('click', () => {
        searchInput.value = tag.textContent;
        renderResults(tag.textContent);
        searchInput.focus();
    });
});